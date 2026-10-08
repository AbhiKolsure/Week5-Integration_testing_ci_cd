"""Locust load scenarios for the Week 4 performance tests.

The scenarios exercise the read endpoints that the Phase 1 audit identified as the
load-testing targets: ``GET /tasks`` (paginated), the filtered and search variants,
``GET /tasks/stats`` and the single-resource reads. Every request is given an explicit
``name=`` so the per-endpoint metrics group cleanly in the CSV report.

Recommended (driven by the reproducible orchestrator)::

    python scripts/performance/run_load_test.py --tasks 1000 --users 20 --run-time 30s

Or directly against a server you started yourself::

    $env:LOAD_AUTH_TOKEN = "<valid bearer access token>"
    python -m locust -f benchmarks/locustfile.py --host http://127.0.0.1:8000

The scenario parameters can be overridden with the ``LOAD_*`` environment variables
listed below; the orchestrator sets them explicitly so a run is fully described by its
command line.
"""

from __future__ import annotations

import os

from locust import HttpUser, between, tag, task

DEFAULT_PAGE_SIZE = int(os.getenv("LOAD_PAGE_SIZE", "50"))
FULL_PAGE_SIZE = int(os.getenv("LOAD_FULL_PAGE", "200"))
SEARCH_TERM = os.getenv("LOAD_SEARCH_TERM", "burndown")
FILTER_STATUS = os.getenv("LOAD_FILTER_STATUS", "pending")
FILTER_PRIORITY = os.getenv("LOAD_FILTER_PRIORITY", "high")
SAMPLE_IDS = int(os.getenv("LOAD_SAMPLE_IDS", "25"))
AUTH_TOKEN = os.getenv("LOAD_AUTH_TOKEN", "")
WAIT_MIN = float(os.getenv("LOAD_WAIT_MIN", "0.1"))
WAIT_MAX = float(os.getenv("LOAD_WAIT_MAX", "0.5"))


class TaskApiUser(HttpUser):
    """A read-mostly virtual user that walks the documented GET endpoints."""

    wait_time = between(WAIT_MIN, WAIT_MAX)

    def on_start(self) -> None:
        """Bootstrap: learn a few real task ids for the single-resource scenarios."""
        if not AUTH_TOKEN:
            raise RuntimeError("Set LOAD_AUTH_TOKEN to a valid bearer token before starting Locust")
        self.client.headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        self._cursor = 0
        self.task_ids: list[int] = []
        with self.client.get(
            "/tasks",
            params={"limit": SAMPLE_IDS},
            name="/tasks [bootstrap]",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                self.task_ids = [item["id"] for item in response.json().get("items", [])]
                response.success()
            else:
                response.failure(f"bootstrap answered HTTP {response.status_code}")

    def _next_task_id(self) -> int | None:
        if not self.task_ids:
            return None
        task_id = self.task_ids[self._cursor % len(self.task_ids)]
        self._cursor += 1
        return task_id

    @tag("list50", "primary")
    @task(5)
    def list_first_page(self) -> None:
        self.client.get("/tasks", params={"limit": DEFAULT_PAGE_SIZE}, name="/tasks?limit=50")

    @tag("list200", "primary")
    @task(3)
    def list_full_page(self) -> None:
        self.client.get("/tasks", params={"limit": FULL_PAGE_SIZE}, name="/tasks?limit=200")

    @tag("filters", "primary")
    @task(3)
    def list_filtered_by_status(self) -> None:
        self.client.get(
            "/tasks",
            params={"status": FILTER_STATUS, "limit": DEFAULT_PAGE_SIZE},
            name="/tasks?status=<value>",
        )

    @tag("filters", "primary")
    @task(2)
    def list_filtered_by_priority(self) -> None:
        self.client.get(
            "/tasks",
            params={"priority": FILTER_PRIORITY, "limit": DEFAULT_PAGE_SIZE},
            name="/tasks?priority=<value>",
        )

    @tag("search", "primary")
    @task(3)
    def search(self) -> None:
        self.client.get("/tasks", params={"q": SEARCH_TERM, "limit": DEFAULT_PAGE_SIZE}, name="/tasks?q=<term>")

    @tag("filters", "primary")
    @task(2)
    def list_combined_filters(self) -> None:
        self.client.get(
            "/tasks",
            params={"status": FILTER_STATUS, "priority": FILTER_PRIORITY, "limit": DEFAULT_PAGE_SIZE},
            name="/tasks?status=&priority=",
        )

    @tag("detail")
    @task(2)
    def single_task(self) -> None:
        task_id = self._next_task_id()
        if task_id is not None:
            self.client.get(f"/tasks/{task_id}", name="/tasks/{id}")

    @tag("detail")
    @task(1)
    def task_comments(self) -> None:
        task_id = self._next_task_id()
        if task_id is not None:
            self.client.get(f"/tasks/{task_id}/comments", name="/tasks/{id}/comments")

    @tag("stats")
    @task(1)
    def statistics(self) -> None:
        self.client.get("/tasks/stats", name="/tasks/stats")
