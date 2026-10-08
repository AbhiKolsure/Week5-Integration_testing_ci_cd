"""Extended API smoke test against the *actual* application over real HTTP (Week 4 Phase 7).

Same mechanics as ``scripts/smoke_check.py`` (child uvicorn process, throw-away SQLite
database, httpx client) but drives the full endpoint contract required by the final
validation: POST/GET/PATCH/PUT/DELETE, pagination, filtering, search, validation errors,
unknown-task 404 handling, comments, statistics and HTTP status semantics::

    python scripts/final_api_smoke.py

Exit code 0 = every check passed, 1 = at least one check failed.
"""

from __future__ import annotations

import os
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STARTUP_TIMEOUT_SECONDS = 40.0

FAILURES: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    """Record one PASS/FAIL line; every failure is listed again at the end."""
    if not condition:
        FAILURES.append(label)
    print(f"[{'PASS' if condition else 'FAIL'}] {label}{f' -> {detail}' if detail else ''}")


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def wait_for_health(client: httpx.Client, base_url: str) -> dict[str, object] | None:
    deadline = time.time() + STARTUP_TIMEOUT_SECONDS
    while time.time() < deadline:
        try:
            response = client.get(f"{base_url}/health")
            if response.status_code == 200:
                return response.json()
        except httpx.HTTPError:
            time.sleep(0.25)
    return None


def main() -> int:
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"

    with tempfile.TemporaryDirectory() as tmp_dir:
        env = dict(os.environ)
        env["DATABASE_URL"] = f"sqlite:///{Path(tmp_dir, 'final_api_smoke.db').as_posix()}"
        env["AUTH_SECRET_KEY"] = secrets.token_urlsafe(48)
        env["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
        server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port),
             "--log-level", "warning"],
            cwd=PROJECT_ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        try:
            print(f"starting: {sys.executable} -m uvicorn app.main:app --port {port} (temp database)")
            with httpx.Client(timeout=10.0) as client:
                health = wait_for_health(client, base_url)
                check("application starts and /health answers 200", health is not None, f"{base_url}/health")
                if health is None:
                    return 1
                check(
                    "/health payload contract",
                    health == {"status": "ok", "service": "Week3 Backend Debugging API", "version": "1.0.0"},
                    f"{health}",
                )

                anonymous = client.get(f"{base_url}/tasks")
                check("GET /tasks rejects requests without a bearer token", anonymous.status_code == 401,
                      f"HTTP {anonymous.status_code}")
                registration = client.post(
                    f"{base_url}/auth/register",
                    json={"email": "smoke@example.com", "password": "week5-smoke-password"},
                )
                check("POST /auth/register creates an account", registration.status_code == 201,
                      f"HTTP {registration.status_code}")
                login = client.post(
                    f"{base_url}/auth/login",
                    json={"email": "smoke@example.com", "password": "week5-smoke-password"},
                )
                token_body = login.json() if login.status_code == 200 else {}
                check(
                    "POST /auth/login returns an expiring bearer token",
                    login.status_code == 200
                    and token_body.get("token_type") == "bearer"
                    and token_body.get("expires_in", 0) > 0
                    and bool(token_body.get("access_token")),
                    f"HTTP {login.status_code}",
                )
                client.headers["Authorization"] = f"Bearer {token_body.get('access_token', '')}"

                # ------------------------------------------------------ POST /tasks
                created = client.post(
                    f"{base_url}/tasks",
                    json={"title": "  Smoke task  ", "priority": "high", "due_date": "2026-11-01T09:30:00+02:00"},
                )
                body = created.json() if created.status_code == 201 else {}
                check("POST /tasks answers 201", created.status_code == 201, f"HTTP {created.status_code}")
                check(
                    "POST payload: title trimmed, priority stored, due date normalised to UTC",
                    body.get("title") == "Smoke task" and body.get("priority") == "high"
                    and body.get("status") == "pending" and body.get("due_date") == "2026-11-01T07:30:00"
                    and body.get("comment_count") == 0 and isinstance(body.get("id"), int),
                    f"title={body.get('title')!r} due_date={body.get('due_date')!r}",
                )
                task1 = int(body.get("id", 0))

                # -------------------------------------------------- validation errors
                validation_cases = [
                    ("blank title rejected with 422", {"title": "   "}),
                    ("missing title rejected with 422", {}),
                    ("unknown field rejected with 422", {"title": "x", "typo_field": 1}),
                    ("invalid status rejected with 422", {"title": "x", "status": "not_a_status"}),
                    ("invalid priority rejected with 422", {"title": "x", "priority": "urgent"}),
                    ("invalid due_date rejected with 422", {"title": "x", "due_date": "not-a-date"}),
                    ("overlong title rejected with 422", {"title": "x" * 201}),
                    ("overlong description rejected with 422", {"title": "x", "description": "y" * 2001}),
                    ("null title rejected with 422", {"title": None}),
                ]
                for label, payload in validation_cases:
                    response = client.post(f"{base_url}/tasks", json=payload)
                    check(label, response.status_code == 422, f"HTTP {response.status_code}")

                # ------------------------------------------------------ GET pagination
                page = client.get(f"{base_url}/tasks", params={"limit": 2})
                page_body = page.json()
                check(
                    "GET /tasks paginates and reports the full total",
                    page.status_code == 200 and len(page_body["items"]) == 1 and page_body["total"] == 1
                    and page_body["skip"] == 0 and page_body["limit"] == 2,
                    f"HTTP {page.status_code} items={len(page_body.get('items', []))} total={page_body.get('total')}",
                )
                beyond = client.get(f"{base_url}/tasks", params={"skip": 5, "limit": 2})
                check("GET /tasks beyond the last page returns an empty item list", beyond.json()["items"] == [], "")
                bad_paging = [
                    client.get(f"{base_url}/tasks", params={"limit": 0}).status_code,
                    client.get(f"{base_url}/tasks", params={"limit": 201}).status_code,
                    client.get(f"{base_url}/tasks", params={"skip": -1}).status_code,
                ]
                check("invalid paging parameters rejected with 422", all(code == 422 for code in bad_paging), f"{bad_paging}")

                # ------------------------------------------------------------- PATCH
                patched = client.patch(f"{base_url}/tasks/{task1}", json={"status": "in_progress"})
                check(
                    "PATCH /tasks/{id} updates only the supplied field",
                    patched.status_code == 200 and patched.json()["status"] == "in_progress"
                    and patched.json()["title"] == "Smoke task",
                    f"HTTP {patched.status_code}",
                )
                blank_patch = client.patch(f"{base_url}/tasks/{task1}", json={"title": "   "})
                null_patch = client.patch(f"{base_url}/tasks/{task1}", json={"title": None})
                stored_title = client.get(f"{base_url}/tasks/{task1}").json()["title"]
                check(
                    "PATCH cannot blank or null the stored title (422, value untouched)",
                    blank_patch.status_code == 422 and null_patch.status_code == 422
                    and stored_title == "Smoke task",
                    f"blank={blank_patch.status_code} null={null_patch.status_code} title={stored_title!r}",
                )

                # --------------------------------------------------------------- PUT
                replaced = client.put(
                    f"{base_url}/tasks/{task1}",
                    json={"title": "Replaced title", "description": "full replacement"},
                )
                replaced_body = replaced.json()
                check(
                    "PUT /tasks/{id} replaces every writable field (omitted fields reset)",
                    replaced.status_code == 200 and replaced_body["title"] == "Replaced title"
                    and replaced_body["description"] == "full replacement"
                    and replaced_body["status"] == "pending" and replaced_body["priority"] == "medium"
                    and replaced_body["due_date"] is None,
                    f"HTTP {replaced.status_code} status={replaced_body.get('status')!r}",
                )
                put_blank = client.put(f"{base_url}/tasks/{task1}", json={"title": " "})
                check("PUT with a blank title rejected with 422", put_blank.status_code == 422, f"HTTP {put_blank.status_code}")


                # ------------------------------------------------------ 404 handling
                missing = client.get(f"{base_url}/tasks/987654")
                check(
                    "GET unknown task answers 404 with an exact detail payload",
                    missing.status_code == 404 and missing.json() == {"detail": "Task 987654 not found"},
                    f"HTTP {missing.status_code} {missing.text[:60]}",
                )
                check(
                    "error payload does not leak internals",
                    "No row was found" not in missing.text and "sqlalchemy" not in missing.text.lower(),
                    "",
                )
                unknown_codes = [
                    client.patch(f"{base_url}/tasks/987654", json={"title": "x"}).status_code,
                    client.put(f"{base_url}/tasks/987654", json={"title": "x"}).status_code,
                    client.delete(f"{base_url}/tasks/987654").status_code,
                ]
                check("unknown id on PATCH/PUT/DELETE answers 404", all(code == 404 for code in unknown_codes), f"{unknown_codes}")
                non_integer = client.get(f"{base_url}/tasks/abc")
                check("non-integer task id answered 422", non_integer.status_code == 422, f"HTTP {non_integer.status_code}")

                # --------------------------------------------------------- comments
                comment = client.post(f"{base_url}/tasks/{task1}/comments", json={"body": "smoke comment"})
                check("POST comment answers 201", comment.status_code == 201, f"HTTP {comment.status_code}")
                comments = client.get(f"{base_url}/tasks/{task1}/comments")
                check(
                    "GET comments returns the comment associated with the task",
                    comments.status_code == 200 and len(comments.json()) == 1
                    and comments.json()[0]["task_id"] == task1 and comments.json()[0]["body"] == "smoke comment",
                    f"count={len(comments.json())}",
                )
                listed_items = client.get(f"{base_url}/tasks").json()["items"]
                count_of_task1 = next((i["comment_count"] for i in listed_items if i["id"] == task1), None)
                check("comment_count is exposed on the listed task", count_of_task1 == 1, f"count={count_of_task1}")
                comment_errors = [
                    client.post(f"{base_url}/tasks/987654/comments", json={"body": "x"}).status_code,
                    client.post(f"{base_url}/tasks/{task1}/comments", json={"body": ""}).status_code,
                ]
                check(
                    "comment on unknown task / empty body answered 4xx",
                    comment_errors[0] == 404 and comment_errors[1] == 422,
                    f"{comment_errors}",
                )


                # ------------------------------------------------ filter + search fixtures
                client.post(
                    f"{base_url}/tasks",
                    json={
                        "title": "Release report",
                        "description": "prepares the burndown summary",
                        "status": "completed",
                        "priority": "low",
                    },
                )
                client.post(
                    f"{base_url}/tasks",
                    json={"title": "Write BURNDOWN docs", "status": "pending", "priority": "high"},
                )

                combined = client.get(f"{base_url}/tasks", params={"status": "pending", "priority": "high"})
                check(
                    "filters are combined with AND semantics",
                    combined.status_code == 200 and combined.json()["total"] == 1,
                    f"total={combined.json().get('total')}",
                )
                status_only = client.get(f"{base_url}/tasks", params={"status": "pending"})
                check("filter by status alone", status_only.json()["total"] == 2, f"total={status_only.json().get('total')}")
                search = client.get(f"{base_url}/tasks", params={"q": "burndown"})
                check(
                    "search matches title AND description, case-insensitively",
                    search.json()["total"] == 2
                    and {item["title"] for item in search.json()["items"]} == {"Release report", "Write BURNDOWN docs"},
                    f"total={search.json().get('total')}",
                )
                search_and_filter = client.get(f"{base_url}/tasks", params={"q": "burndown", "status": "pending"})
                check(
                    "search combines with filters (AND)",
                    search_and_filter.json()["total"] == 1
                    and search_and_filter.json()["items"][0]["title"] == "Write BURNDOWN docs",
                    f"total={search_and_filter.json().get('total')}",
                )
                no_match = client.get(f"{base_url}/tasks", params={"q": "no-such-token"})
                check("search without matches returns an empty page", no_match.json()["total"] == 0, "")
                bad_filter = client.get(f"{base_url}/tasks", params={"status": "bogus"})
                check("invalid filter value rejected with 422", bad_filter.status_code == 422, f"HTTP {bad_filter.status_code}")

                # --------------------------------------------------------- statistics
                stats = client.get(f"{base_url}/tasks/stats")
                stats_body = stats.json()
                check("GET /tasks/stats answers 200", stats.status_code == 200, f"HTTP {stats.status_code}")
                check(
                    "statistics counters consistent with the data created above",
                    stats_body.get("total") == 3 and stats_body.get("completed") == 1
                    and stats_body.get("by_status") == {"pending": 2, "in_progress": 0, "completed": 1}
                    and stats_body.get("by_priority") == {"low": 1, "medium": 1, "high": 1}
                    and stats_body.get("total_comments") == 1 and stats_body.get("completion_rate") == 0.3333
                    and stats_body.get("average_comments_per_task") == 0.3333 and stats_body.get("overdue") == 0,
                    f"total={stats_body.get('total')} completed={stats_body.get('completed')}",
                )


                # ---------------------------------------------------- DELETE semantics
                task2 = client.get(f"{base_url}/tasks", params={"q": "Release report"}).json()["items"][0]["id"]
                deleted = client.delete(f"{base_url}/tasks/{task2}")
                check(
                    "DELETE /tasks/{id} answers 204 with an empty body",
                    deleted.status_code == 204 and deleted.content == b"",
                    f"HTTP {deleted.status_code} body={deleted.content!r}",
                )
                gone_codes = [
                    client.get(f"{base_url}/tasks/{task2}").status_code,
                    client.delete(f"{base_url}/tasks/{task2}").status_code,
                ]
                check("deleted task answers 404 and double delete answers 404", all(c == 404 for c in gone_codes), f"{gone_codes}")
                after_delete = client.get(f"{base_url}/tasks/stats").json()["total"]
                check("statistics updated after deletion", after_delete == 2, f"total={after_delete}")

                # ------------------------------------------------------ openapi contract
                openapi = client.get(f"{base_url}/openapi.json")
                paths = sorted(openapi.json()["paths"]) if openapi.status_code == 200 else []
                check(
                    "OpenAPI document exposes every route",
                    paths
                    == [
                        "/auth/login",
                        "/auth/register",
                        "/health",
                        "/tasks",
                        "/tasks/stats",
                        "/tasks/{task_id}",
                        "/tasks/{task_id}/comments",
                    ],
                    f"{paths}",
                )
        finally:
            server.terminate()
            try:
                server.wait(timeout=15)
            except subprocess.TimeoutExpired:  # pragma: no cover - defensive
                server.kill()
            output = server.stdout.read() if server.stdout else ""
            if output.strip():
                print("\n--- uvicorn output ---")
                print(output.strip())

    print("-" * 80)
    print(f"checks failed: {len(FAILURES)}")
    for failure in FAILURES:
        print(f"  - {failure}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
