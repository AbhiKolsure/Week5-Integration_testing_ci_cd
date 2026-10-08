"""Measure the number of SQL statements each load scenario sends to the database.

Locust measures wall-clock behaviour over real HTTP; this script measures the other
half of the picture - the deterministic query count per endpoint. It reuses the same
deterministic dataset and SQLAlchemy's ``before_cursor_execute`` event, exactly like
``benchmarks/benchmark_list_tasks.py`` and ``tests/test_performance.py``, so the numbers
are comparable with the Week 3 evidence.

Usage::

    python scripts/performance/measure_query_counts.py --tasks 1000
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections.abc import Iterator
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from auth_harness import authenticate_test_client  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from seed_dataset import DEFAULT_COMMENTS_PER_TASK, DEFAULT_TASKS, expected_search_matches, seed_engine  # noqa: E402
from sqlalchemy import create_engine, event  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.database import get_db  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402

# (label, path, query params) - mirrors the Locust scenarios one-for-one.
SCENARIOS: list[tuple[str, str, dict[str, object]]] = [
    ("GET /tasks?limit=50", "/tasks", {"limit": 50}),
    ("GET /tasks?limit=200", "/tasks", {"limit": 200}),
    ("GET /tasks?status=pending", "/tasks", {"status": "pending", "limit": 50}),
    ("GET /tasks?priority=high", "/tasks", {"priority": "high", "limit": 50}),
    ("GET /tasks?q=burndown", "/tasks", {"q": "burndown", "limit": 50}),
    ("GET /tasks?status=&priority=", "/tasks", {"status": "pending", "priority": "high", "limit": 50}),
    ("GET /tasks/stats", "/tasks/stats", {}),
    ("GET /tasks/1", "/tasks/1", {}),
    ("GET /tasks/1/comments", "/tasks/1/comments", {}),
]


def build_client(task_count: int, comments_per_task: int, log: list[dict[str, object]]) -> tuple[object, TestClient]:
    """Return ``(engine, client)`` backed by a seeded in-memory database.

    Every statement is recorded together with its execution time, which turns this
    script into the slow-query measurement as well as the statement counter.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    seed_engine(engine, task_count, comments_per_task, reset=False)

    starts: dict[int, float] = {}

    def _before(_conn, _cursor, _statement, _parameters, context, _executemany) -> None:
        starts[id(context)] = time.perf_counter()

    def _after(_conn, _cursor, statement, _parameters, context, _executemany) -> None:
        began = starts.pop(id(context), None)
        if began is not None:
            log.append({"statement": statement, "seconds": time.perf_counter() - began})

    event.listen(engine, "before_cursor_execute", _before)
    event.listen(engine, "after_cursor_execute", _after)

    session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def _override_get_db() -> Iterator[Session]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    fastapi_app.dependency_overrides[get_db] = _override_get_db
    client = TestClient(fastapi_app, raise_server_exceptions=False)
    authenticate_test_client(client, session_factory)
    return engine, client


def measure(
    client: TestClient,
    log: list[dict[str, object]],
    path: str,
    params: dict[str, object],
) -> dict[str, object]:
    """Warm up once, then record the statements (and timings) of a single request."""
    client.get(path, params=params or None)  # warm-up: opens the connection and caches SQL
    log.clear()
    response = client.get(path, params=params or None)
    recorded = list(log)
    slowest = sorted(recorded, key=lambda item: float(item["seconds"]), reverse=True)
    return {
        "path": path,
        "params": params,
        "status": response.status_code,
        "statements": len(recorded),
        "total_db_ms": round(sum(float(item["seconds"]) for item in recorded) * 1000, 3),
        "slowest_statements": [
            {
                "statement": " ".join(str(item["statement"]).split())[:140],
                "ms": round(float(item["seconds"]) * 1000, 3),
            }
            for item in slowest[:3]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure SQL statements per endpoint.")
    parser.add_argument("--tasks", type=int, default=DEFAULT_TASKS, help="number of seeded tasks (default: 1000)")
    parser.add_argument(
        "--comments-per-task",
        type=int,
        default=DEFAULT_COMMENTS_PER_TASK,
        help="comments per task (default: 1)",
    )
    parser.add_argument("--out", default="", help="optional path for a JSON copy of the result")
    args = parser.parse_args()

    log: list[dict[str, object]] = []
    engine, client = build_client(args.tasks, args.comments_per_task, log)
    try:
        results = [measure(client, log, path, params) for _label, path, params in SCENARIOS]
        for (label, _path, _params), result in zip(SCENARIOS, results, strict=True):
            result["label"] = label

        print("=" * 92)
        print("SQL statement counts and per-request DB time per load scenario")
        print(f"dataset: {args.tasks} tasks x {args.comments_per_task} comment(s), in-memory SQLite")
        print(f"q=burndown matches: {expected_search_matches(args.tasks)}")
        print("=" * 92)
        header = f"{'scenario':<28}{'status':>8}{'SQL stmts':>12}{'DB ms':>10}"
        print(header)
        print("-" * len(header))
        for result in results:
            print(
                f"{result['label']:<28}{int(result['status']):>8}"
                f"{int(result['statements']):>12}{float(result['total_db_ms']):>10.3f}"
            )
        print("-" * len(header))
        print("Statement counts are exact and deterministic; DB ms is a single-request")
        print("measurement of the SQL time only (no HTTP or serialisation overhead).")
        print()
        print("slowest statements per scenario")
        print("-" * 92)
        for result in results:
            for slow in result["slowest_statements"][:1]:
                print(f"{result['label']:<28}{float(slow['ms']):>9.3f} ms  {slow['statement'][:70]}")

        if args.out:
            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "dataset": {"tasks": args.tasks, "comments_per_task": args.comments_per_task},
                "scenarios": results,
            }
            out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"written: {out_path}")
        return 0
    finally:
        fastapi_app.dependency_overrides.clear()
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
