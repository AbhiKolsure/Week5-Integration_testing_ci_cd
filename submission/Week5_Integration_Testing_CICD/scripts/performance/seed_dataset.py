"""Deterministic test-data generation for the Week 4 load tests.

Every column value is a pure function of the row index, so two runs with the same
arguments insert *exactly* the same rows. That keeps every benchmark reproducible:
the same dataset feeds the Locust load test, the SQL query-count measurement and the
pytest fixtures.

The generator is aware of the ``?q=`` search scenario: the token ``burndown`` appears
in the description of every ``SEARCH_EVERY``-th task and in no other row, so the number
of search matches is deterministic and can be verified (see
:func:`expected_search_matches`).

Usage::

    python scripts/performance/seed_dataset.py --tasks 10000 --comments-per-task 1 \\
        --database week4_perf_tasks.db
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import create_engine, delete  # noqa: E402
from sqlalchemy.engine import Engine  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402

from app import models  # noqa: E402
from app.database import Base  # noqa: E402

DEFAULT_TASKS = 1000
DEFAULT_COMMENTS_PER_TASK = 1

# Fixed wall-clock anchor so ``created_at`` / ``due_date`` are reproducible.
ANCHOR = datetime(2026, 1, 1, 0, 0, 0)

# The substring the ``?q=`` load scenario searches for, and its deterministic cadence.
SEARCH_TOKEN = "burndown"
SEARCH_EVERY = 7

STATUSES = [status.value for status in models.TaskStatus]
PRIORITIES = [priority.value for priority in models.Priority]

ADJECTIVES = ["fix", "review", "refactor", "document", "deploy", "test", "triage", "optimise", "audit", "ship"]
NOUNS = [
    "login flow",
    "search index",
    "report job",
    "cache layer",
    "migration",
    "dashboard",
    "webhook",
    "scheduler",
    "cli",
    "api client",
]


def build_task_rows(task_count: int) -> list[dict[str, object]]:
    """Return the deterministic task rows for ``task_count`` tasks.

    Identifiers are assigned explicitly (1..task_count) so bulk inserts are fast and
    the comment rows can reference them without an extra round trip.
    """
    rows: list[dict[str, object]] = []
    for index in range(task_count):
        overdue = index % 5 == 0
        day_offset = -((index % 30) + 1) if overdue else ((index % 30) + 1)
        description = "plain seed row"
        if index % SEARCH_EVERY == 0:
            description = f"mentions the {SEARCH_TOKEN} chart"
        rows.append(
            {
                "id": index + 1,
                "title": f"Task {index:06d} {ADJECTIVES[index % len(ADJECTIVES)]} the {NOUNS[index % len(NOUNS)]}",
                "description": description,
                "status": STATUSES[index % len(STATUSES)],
                "priority": PRIORITIES[(index // len(STATUSES)) % len(PRIORITIES)],
                "due_date": ANCHOR + timedelta(days=day_offset),
                "created_at": ANCHOR + timedelta(minutes=index),
                "updated_at": ANCHOR + timedelta(minutes=index),
            }
        )
    return rows


def build_comment_rows(task_count: int, comments_per_task: int) -> list[dict[str, object]]:
    """Return the deterministic comment rows (``comments_per_task`` per task)."""
    rows: list[dict[str, object]] = []
    comment_id = 1
    for task_index in range(task_count):
        for comment_index in range(comments_per_task):
            rows.append(
                {
                    "id": comment_id,
                    "task_id": task_index + 1,
                    "author": f"author-{comment_index}",
                    "body": f"comment {comment_index} on task {task_index + 1}",
                    "created_at": ANCHOR + timedelta(minutes=task_index, seconds=comment_index),
                }
            )
            comment_id += 1
    return rows


def expected_search_matches(task_count: int) -> int:
    """Number of tasks whose description contains :data:`SEARCH_TOKEN`."""
    if task_count <= 0:
        return 0
    return (task_count - 1) // SEARCH_EVERY + 1


def to_url(database: str | Path) -> str:
    """Accept either a SQLAlchemy URL or a filesystem path and return a URL."""
    text = str(database)
    if "://" in text:
        return text
    return f"sqlite:///{Path(text).as_posix()}"


def seed_engine(
    engine: Engine,
    task_count: int = DEFAULT_TASKS,
    comments_per_task: int = DEFAULT_COMMENTS_PER_TASK,
    reset: bool = True,
) -> dict[str, int]:
    """Create the schema on ``engine`` and bulk-insert the deterministic dataset."""
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, future=True)
    session: Session = session_factory()
    try:
        if reset:
            session.execute(delete(models.Comment))
            session.execute(delete(models.Task))
            session.commit()
        session.bulk_insert_mappings(models.Task, build_task_rows(task_count))
        session.commit()
        if comments_per_task > 0:
            session.bulk_insert_mappings(models.Comment, build_comment_rows(task_count, comments_per_task))
            session.commit()
    finally:
        session.close()
    return {"tasks": task_count, "comments": task_count * comments_per_task}


def seed_database(
    database: str | Path,
    task_count: int = DEFAULT_TASKS,
    comments_per_task: int = DEFAULT_COMMENTS_PER_TASK,
    reset: bool = True,
) -> dict[str, int]:
    """Seed a standalone database (file path or SQLAlchemy URL)."""
    url = to_url(database)
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, connect_args=connect_args, future=True)
    try:
        return seed_engine(engine, task_count, comments_per_task, reset)
    finally:
        engine.dispose()


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed a deterministic load-test dataset.")
    parser.add_argument("--tasks", type=int, default=DEFAULT_TASKS, help="number of tasks (default: 1000)")
    parser.add_argument(
        "--comments-per-task",
        type=int,
        default=DEFAULT_COMMENTS_PER_TASK,
        help="comments per task (default: 1)",
    )
    parser.add_argument("--database", default="week4_perf_tasks.db", help="SQLite path or SQLAlchemy URL")
    parser.add_argument("--no-reset", action="store_true", help="append instead of clearing the tables first")
    args = parser.parse_args()

    stats = seed_database(
        args.database,
        task_count=args.tasks,
        comments_per_task=args.comments_per_task,
        reset=not args.no_reset,
    )
    print("seeded dataset")
    print(f"  database          : {to_url(args.database)}")
    print(f"  tasks             : {stats['tasks']}")
    print(f"  comments          : {stats['comments']}")
    print(f"  q={SEARCH_TOKEN} matches : {expected_search_matches(args.tasks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
