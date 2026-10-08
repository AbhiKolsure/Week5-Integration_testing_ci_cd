"""Smoke tests for the Week 4 load-testing infrastructure.

These verify the *mechanics* of the harness - deterministic data generation, the Locust
scenario definition and the CSV -> summary parsing - so a broken harness fails fast in
the normal test run instead of during a long load test. They do not start a server;
the end-to-end check is ``scripts/performance/run_load_test.py`` (see
``PERFORMANCE_TESTING.md``).

    pytest -m loadtest -v
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PERF_SCRIPTS = PROJECT_ROOT / "scripts" / "performance"
for _candidate in (str(PROJECT_ROOT), str(PERF_SCRIPTS)):
    if _candidate not in sys.path:
        sys.path.insert(0, _candidate)

import seed_dataset  # noqa: E402
from locust_summary import parse_stats_csv, render_markdown  # noqa: E402

pytestmark = pytest.mark.loadtest

STATS_HEADER = (
    "Type,Name,Request Count,Failure Count,Median Response Time,Average Response Time,"
    "Min Response Time,Max Response Time,Average Content Size,Requests/s,Failures/s,"
    "95%,99%"
)


def test_seed_rows_are_deterministic() -> None:
    assert seed_dataset.build_task_rows(250) == seed_dataset.build_task_rows(250)
    assert seed_dataset.build_comment_rows(50, 3) == seed_dataset.build_comment_rows(50, 3)


def test_expected_search_matches_matches_the_generated_rows() -> None:
    for task_count in (0, 1, 6, 7, 1000, 10000):
        rows = seed_dataset.build_task_rows(task_count) if task_count else []
        actual = sum(1 for row in rows if seed_dataset.SEARCH_TOKEN in str(row["description"]))
        assert actual == seed_dataset.expected_search_matches(task_count)


def test_seed_database_writes_the_expected_number_of_rows(tmp_path: Path) -> None:
    db_path = tmp_path / "seed.db"
    stats = seed_dataset.seed_database(db_path, task_count=120, comments_per_task=2, reset=True)

    assert stats == {"tasks": 120, "comments": 240}
    assert db_path.is_file()


def test_locustfile_defines_the_read_scenarios() -> None:
    """Inspect the locustfile statically.

    Importing ``locust`` executes ``gevent.monkey.patch_all()`` at import time, which
    would contaminate the whole pytest process (it runs during collection and breaks the
    threaded TestClient suites). The file is therefore parsed with ``ast`` instead of
    being imported.
    """
    tree = ast.parse((PROJECT_ROOT / "benchmarks" / "locustfile.py").read_text(encoding="utf-8"))
    user_classes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(isinstance(base, ast.Name) and base.id == "HttpUser" for base in node.bases)
    ]
    assert user_classes, "no HttpUser subclass found in the locustfile"

    user_class = user_classes[0]
    methods = {
        node.name
        for node in user_class.body
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    }
    expected = {"list_first_page", "list_full_page", "search", "statistics"}
    assert expected <= methods, "the locustfile no longer defines every read scenario"

    # Each read scenario must be scheduled with a @task(...) decorator.
    task_methods = {
        node.name
        for node in user_class.body
        if isinstance(node, ast.FunctionDef)
        and any(
            isinstance(decorator, ast.Call) and getattr(decorator.func, "id", "") == "task"
            for decorator in node.decorator_list
        )
    }
    assert expected <= task_methods, "read scenarios are not decorated with @task(...)"


def test_stats_csv_parser_extracts_all_metrics(tmp_path: Path) -> None:
    csv_path = tmp_path / "locust_stats.csv"
    csv_path.write_text(
        "\n".join(
            [
                STATS_HEADER,
                "GET,/tasks,100,2,10,12.5,5,40,1000,20.0,0.4,25,35",
                ",Aggregated,100,2,10,12.5,5,40,1000,20.0,0.4,25,35",
            ]
        ),
        encoding="utf-8",
    )

    summary = parse_stats_csv(csv_path)
    aggregated = summary["aggregated"]
    assert aggregated["request_count"] == 100.0
    assert aggregated["failure_count"] == 2.0
    assert aggregated["failure_rate"] == pytest.approx(0.02)
    assert aggregated["p95_ms"] == 25.0
    assert aggregated["p99_ms"] == 35.0
    assert len(summary["endpoints"]) == 1
    assert summary["endpoints"][0]["name"] == "/tasks"


def test_markdown_render_includes_totals_and_endpoints(tmp_path: Path) -> None:
    csv_path = tmp_path / "locust_stats.csv"
    csv_path.write_text("\n".join([STATS_HEADER, "GET,/tasks,10,0,5,6,4,9,100,2.0,0.0,8,9"]), encoding="utf-8")
    summary = parse_stats_csv(csv_path)

    markdown = render_markdown(summary, {"run_label": "unit", "users": 1}, str(csv_path))
    assert "# Load test summary" in markdown
    assert "| run_label | unit |" in markdown
    assert "| Endpoint |" in markdown
    assert "| /tasks |" in markdown
