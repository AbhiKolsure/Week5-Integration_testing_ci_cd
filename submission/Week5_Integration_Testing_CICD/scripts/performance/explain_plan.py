"""Print the SQLite query plan for the statements Phase 5 targets.

Measurement tool only - it changes no application code. It seeds a throw-away database
with the deterministic dataset, prints ``PRAGMA index_list`` and the
``EXPLAIN QUERY PLAN`` of the statements used by ``GET /tasks/stats`` and the list
endpoints, so the Phase 5 before/after plan can be compared exactly.

Usage::

    python scripts/performance/explain_plan.py --tasks 10000 --out plan_before.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
_HERE = Path(__file__).resolve().parent
for _path in (str(PROJECT_ROOT), str(_HERE)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import sqlalchemy as sa  # noqa: E402
from seed_dataset import seed_database, to_url  # noqa: E402

# The exact statement app/crud.py::get_statistics issues for the "overdue" counter.
OVERDUE_SQL = (
    "SELECT count(tasks.id) AS count_1 FROM tasks "
    "WHERE tasks.due_date IS NOT NULL AND tasks.due_date < '2026-06-01' "
    "AND tasks.status != 'completed'"
)
STATS_STATEMENTS = {
    "total": "SELECT count(tasks.id) AS count_1 FROM tasks",
    "completed": "SELECT count(tasks.id) AS count_1 FROM tasks WHERE tasks.status = 'completed'",
    "overdue (target)": OVERDUE_SQL,
    "by_status": "SELECT tasks.status AS tasks_status, count(tasks.id) AS count_1 "
                 "FROM tasks GROUP BY tasks.status",
    "by_priority": "SELECT tasks.priority AS tasks_priority, count(tasks.id) AS count_1 "
                   "FROM tasks GROUP BY tasks.priority",
    "total_comments": "SELECT count(comments.id) AS count_1 FROM comments",
}
LIST_STATEMENTS = {
    "list page limit=50": "SELECT tasks.id FROM tasks ORDER BY tasks.id LIMIT 50",
    "list count": "SELECT count(*) FROM (SELECT tasks.id FROM tasks)",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print SQLite query plans for the Phase 5 targets.")
    parser.add_argument("--tasks", type=int, default=10000, help="rows to seed (default: 10000)")
    parser.add_argument("--comments-per-task", type=int, default=1)
    parser.add_argument("--database", default="", help="SQLite path (default: a temp file)")
    parser.add_argument("--out", default="", help="write the report here as well as stdout")
    args = parser.parse_args(argv)

    database = args.database or str(Path.home() / "AppData" / "Local" / "Temp" / "phase5_explain.db")
    seed_database(database, args.tasks, args.comments_per_task, reset=True)
    engine = sa.create_engine(to_url(database), future=True)
    conn = engine.connect()

    lines: list[str] = []
    lines.append("=" * 100)
    lines.append(f"EXPLAIN QUERY PLAN - {args.tasks} tasks x {args.comments_per_task} comment(s)")
    lines.append("=" * 100)

    lines.append("")
    lines.append("--- indexes present on tasks / comments ---")
    for table in ("tasks", "comments"):
        rows = conn.exec_driver_sql(f"PRAGMA index_list({table})").fetchall()
        for row in rows:
            cols = conn.exec_driver_sql(f"PRAGMA index_info({row[1]})").fetchall()
            col_names = ", ".join(str(c[2]) for c in cols)
            marker = "UNIQUE" if row[2] else "normal"
            lines.append(f"  {table}.{col_names:<16} -> {row[1]}  ({marker})")

    for title, statements in (("STATS ENDPOINT", STATS_STATEMENTS), ("LIST ENDPOINT", LIST_STATEMENTS)):
        lines.append("")
        lines.append(f"--- {title} ---")
        for label, sql in statements.items():
            plan = conn.exec_driver_sql("EXPLAIN QUERY PLAN " + sql).fetchall()
            access = "; ".join(str(r[3]) for r in plan)
            kind = "SCAN" if access.startswith("SCAN") else ("SEARCH" if "SEARCH" in access else access)
            lines.append(f"  {label:<24} [{kind}]")
            for row in plan:
                lines.append(f"      {row[3]}")

    conn.close()
    engine.dispose()

    report = "\n".join(lines)
    print(report)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report + "\n", encoding="utf-8")
        print(f"\nwritten: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
