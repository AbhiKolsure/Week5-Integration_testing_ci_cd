"""Database integrity and query-behaviour validation (Week 4 Phase 7).

Seeds a throw-away file-based SQLite database with the deterministic dataset, then
verifies through the real application (TestClient) and direct SQLite introspection that:

* task records, comment associations and statistics are correct after mutations,
* the database passes SQLite's own integrity / foreign-key checks,
* the read endpoints still send the validated optimised number of SQL statements
  (no N+1 reintroduction), measured with ``before_cursor_execute``.

    python scripts/final_db_check.py

Exit code 0 = every check passed, 1 = at least one check failed.
"""

from __future__ import annotations

import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
_PERF = PROJECT_ROOT / "scripts" / "performance"
if str(_PERF) not in sys.path:
    sys.path.insert(0, str(_PERF))

from auth_harness import authenticate_test_client  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from seed_dataset import expected_search_matches, seed_database  # noqa: E402
from sqlalchemy import create_engine, event, text  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.database import get_db  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402

FAILURES: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    """Record one PASS/FAIL line; every failure is listed again at the end."""
    if not condition:
        FAILURES.append(label)
    print(f"[{'PASS' if condition else 'FAIL'}] {label}{f' -> {detail}' if detail else ''}")


def build_client(db_path: Path, statements: list[str]) -> tuple[object, TestClient]:
    """Return ``(engine, client)`` backed by the seeded file database."""
    engine = create_engine(
        f"sqlite:///{db_path.as_posix()}",
        connect_args={"check_same_thread": False},
        future=True,
    )

    def _record(_conn, _cursor, statement, _parameters, context, _executemany) -> None:
        statements.append(statement)

    event.listen(engine, "before_cursor_execute", _record)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    def _override_get_db() -> Iterator[object]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    fastapi_app.dependency_overrides[get_db] = _override_get_db
    client = TestClient(fastapi_app, raise_server_exceptions=False)
    authenticate_test_client(client, session_factory)
    return engine, client


def scalar(engine, query: str) -> object:
    """Run one scalar SQL statement against the database file."""
    with engine.connect() as connection:
        return connection.execute(text(query)).scalar()


def main() -> int:
    seeded_tasks = 500
    seeded_comments = seeded_tasks  # 1 comment per task
    statements: list[str] = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir, "db_check.db")
        stats = seed_database(db_path, seeded_tasks, 1, reset=True)
        print("=" * 92)
        print("Week 4 Phase 7 - database / query validation")
        print(f"database: {db_path.name} (throw-away file), seeded via seed_dataset.py")
        print("=" * 92)
        check(
            "seed_database wrote the expected row counts",
            stats == {"tasks": seeded_tasks, "comments": seeded_comments},
            f"{stats}",
        )

        engine, client = build_client(db_path, statements)
        try:
            # ---------------------------------------------- read correctness
            page = client.get("/tasks", params={"limit": 50})
            check(
                "GET /tasks returns the seeded total and a full page",
                page.status_code == 200
                and page.json()["total"] == seeded_tasks
                and len(page.json()["items"]) == 50,
                f"total={page.json().get('total')} items={len(page.json().get('items', []))}",
            )
            check(
                "every listed task carries the correct comment_count (1)",
                all(item["comment_count"] == 1 for item in page.json()["items"]),
                "",
            )
            detail = client.get("/tasks/1")
            check(
                "GET /tasks/1 reports comment_count=1",
                detail.status_code == 200 and detail.json()["comment_count"] == 1,
                f"comment_count={detail.json().get('comment_count') if detail.status_code == 200 else '?'}",
            )



            # ---------------------------------------------- statistics vs direct SQL
            stats_response = client.get("/tasks/stats")
            api_stats = stats_response.json()
            sql_total = scalar(engine, "SELECT COUNT(*) FROM tasks")
            sql_completed = scalar(engine, "SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
            sql_comments = scalar(engine, "SELECT COUNT(*) FROM comments")
            check(
                "GET /tasks/stats matches direct SQL counts",
                stats_response.status_code == 200
                and api_stats["total"] == sql_total
                and api_stats["completed"] == sql_completed
                and api_stats["total_comments"] == sql_comments
                and sum(api_stats["by_status"].values()) == sql_total
                and sum(api_stats["by_priority"].values()) == sql_total,
                f"api total={api_stats['total']} sql total={sql_total} "
                f"api comments={api_stats['total_comments']} sql comments={sql_comments}",
            )

            # ---------------------------------------------- mutation + association
            created = client.post("/tasks", json={"title": "Integrity probe", "priority": "high"})
            probe_id = created.json()["id"]
            client.post(f"/tasks/{probe_id}/comments", json={"body": "probe note"})
            check(
                "created task and comment are associated in the database",
                scalar(engine, f"SELECT COUNT(*) FROM comments WHERE task_id = {probe_id}") == 1,
                f"probe_id={probe_id}",
            )
            patched = client.patch(f"/tasks/{probe_id}", json={"status": "completed"})
            check(
                "update persisted to the database file",
                patched.status_code == 200
                and scalar(engine, f"SELECT status FROM tasks WHERE id = {probe_id}") == "completed",
                f"status={scalar(engine, f'SELECT status FROM tasks WHERE id = {probe_id}')}",
            )
            deleted = client.delete(f"/tasks/{probe_id}")
            orphan_comments = scalar(engine, "SELECT COUNT(*) FROM comments WHERE task_id NOT IN (SELECT id FROM tasks)")
            check(
                "delete removed the task AND its comment (no orphans)",
                deleted.status_code == 204
                and scalar(engine, f"SELECT COUNT(*) FROM tasks WHERE id = {probe_id}") == 0
                and orphan_comments == 0,
                f"orphan comments={orphan_comments}",
            )

            # ---------------------------------------------- SQLite integrity
            integrity = scalar(engine, "PRAGMA integrity_check")
            fk_violations = 0
            with engine.connect() as connection:
                fk_violations = len(connection.execute(text("PRAGMA foreign_key_check")).fetchall())
            check("PRAGMA integrity_check reports ok", integrity == "ok", f"{integrity}")
            check("PRAGMA foreign_key_check reports no violations", fk_violations == 0, f"violations={fk_violations}")

            # ---------------------------------------------- search correctness
            search = client.get("/tasks", params={"q": "burndown"})
            check(
                "seeded search token matches the expected number of rows",
                search.status_code == 200
                and search.json()["total"] == expected_search_matches(seeded_tasks),
                f"total={search.json().get('total')} "
                f"expected={expected_search_matches(seeded_tasks)}",
            )


            # ------------------------------------------- N+1 guard (query counts)
            # Measured exactly like tests/test_performance.py: count the statements
            # the application sends for one request, at two different page sizes.
            statements.clear()
            client.get("/tasks", params={"limit": 1})  # warm-up not counted
            statements.clear()
            client.get("/tasks", params={"limit": 1})
            list_1 = len(statements)

            statements.clear()
            client.get("/tasks", params={"limit": 50})
            list_50 = len(statements)

            statements.clear()
            client.get("/tasks/stats")
            stats_statements = len(statements)

            statements.clear()
            client.get("/tasks/1")
            detail_statements = len(statements)

            print("-" * 92)
            print("measured SQL statements per request (this run):")
            print(f"  GET /tasks?limit=1  -> {list_1} statements")
            print(f"  GET /tasks?limit=50 -> {list_50} statements")
            print(f"  GET /tasks/stats    -> {stats_statements} statements")
            print(f"  GET /tasks/1        -> {detail_statements} statements")
            print("-" * 92)
            check(
                "list statement count is constant across page sizes (no N+1)",
                list_1 == list_50 and list_50 <= 6,
                f"limit=1 -> {list_1}, limit=50 -> {list_50}",
            )
            check(
                "statistics statement count within the validated budget",
                stats_statements <= 8,
                f"{stats_statements} statements",
            )
            check(
                "single task lookup within the validated budget",
                detail_statements <= 4,
                f"{detail_statements} statements",
            )
        finally:
            fastapi_app.dependency_overrides.clear()
            engine.dispose()

    print("-" * 80)
    print(f"checks failed: {len(FAILURES)}")
    for failure in FAILURES:
        print(f"  - {failure}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
