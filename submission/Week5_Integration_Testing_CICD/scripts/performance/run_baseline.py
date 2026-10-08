"""Baseline matrix runner for Week 4 Phase 3.

Runs a controlled matrix of load tests (dataset size x concurrency x endpoint), writes
the raw Locust evidence for every single run under
``artifacts/performance/<run-label>/`` and consolidates the numbers into

* ``artifacts/performance/baseline_summary.json``
* ``artifacts/performance/baseline_<n>_tasks.txt`` (human readable, per dataset)

Nothing in this phase changes application code; this script only *measures*.

Usage::

    python scripts/performance/run_baseline.py --duration 20s
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
_HERE = Path(__file__).resolve().parent
for _path in (str(PROJECT_ROOT), str(_HERE)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from run_load_test import DEFAULT_LOCUSTFILE, DEFAULT_OUT_DIR, RunConfig, execute_run  # noqa: E402
from seed_dataset import DEFAULT_COMMENTS_PER_TASK, SEARCH_TOKEN  # noqa: E402

# The endpoint under test, selected through the @tag labels in benchmarks/locustfile.py.
# Maps the human label to (locust tag, the request name Locust reports) so the recorded
# numbers are the ones for this endpoint only - the Locust "Aggregated" row also contains
# the per-user bootstrap request, which would otherwise pollute the baseline.
TARGETS: dict[str, tuple[str, str]] = {
    "GET /tasks": ("list50", "/tasks?limit=50"),
    "GET /tasks/stats": ("stats", "/tasks/stats"),
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Week 4 baseline matrix.")
    parser.add_argument("--datasets", default="1000,10000", help="comma separated task counts")
    parser.add_argument("--concurrency", default="10,25,50", help="comma separated user counts")
    parser.add_argument("--duration", default="20s", help="Locust duration per run (default: 20s)")
    parser.add_argument("--repeats", type=int, default=2, help="repeats per configuration (default: 2)")
    parser.add_argument("--comments-per-task", type=int, default=DEFAULT_COMMENTS_PER_TASK)
    parser.add_argument(
        "--warmup",
        type=float,
        default=5.0,
        help="seconds of unmeasured warm-up per run (default: 5)",
    )
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--locustfile", default=str(DEFAULT_LOCUSTFILE))
    parser.add_argument("--only-datasets", default="", help="restrict to these dataset sizes")
    return parser.parse_args(argv)


def _numeric(values: list[float]) -> dict[str, float | None]:
    """Aggregate repeated measurements without inventing precision."""
    if not values:
        return {"min": None, "max": None, "mean": None, "median": None}
    return {
        "min": round(min(values), 2),
        "max": round(max(values), 2),
        "mean": round(statistics.fmean(values), 2),
        "median": round(statistics.median(values), 2),
    }


def build_config(
    label: str,
    tasks: int,
    users: int,
    tags: str,
    duration: str,
    comments_per_task: int,
    out_dir: Path,
    locustfile: Path,
    warmup: float = 5.0,
) -> RunConfig:
    return RunConfig(
        tasks=tasks,
        comments_per_task=comments_per_task,
        users=users,
        # Ramp fast enough that the whole run is at the target concurrency, but not
        # so fast that the process start itself is part of the measurement.
        spawn_rate=max(1.0, users / 5),
        run_time=duration,
        page_size=50,
        full_page=200,
        search_term=SEARCH_TOKEN,
        filter_status="pending",
        filter_priority="high",
        label=label,
        tags=tags,
        out_dir=out_dir,
        locustfile=locustfile,
        warmup_seconds=warmup,
    )


def slug(text: str) -> str:
    """Turn an endpoint label into a filesystem/label friendly token."""
    keep = [character if character.isalnum() else "-" for character in text.lower()]
    return "".join(keep).strip("-").replace("--", "-")


def run_matrix(args: argparse.Namespace) -> dict[str, object]:
    out_dir = Path(args.out_dir)
    datasets = [int(value) for value in args.datasets.split(",") if value.strip()]
    concurrencies = [int(value) for value in args.concurrency.split(",") if value.strip()]
    if args.only_datasets:
        wanted = {int(value) for value in args.only_datasets.split(",") if value.strip()}
        datasets = [value for value in datasets if value in wanted]

    started = datetime.now(UTC)
    records: list[dict[str, object]] = []

    print("=" * 100)
    print("Week 4 Phase 3 - baseline matrix (measurement only, no optimisation)")
    print("=" * 100)
    print(f"datasets    : {datasets}")
    print(f"concurrency : {concurrencies}")
    print(f"duration    : {args.duration} per run, {args.repeats} repeat(s)")
    print(f"targets     : {list(TARGETS)}")
    print()

    total = len(datasets) * len(concurrencies) * args.repeats * len(TARGETS)
    index = 0
    for tasks in datasets:
        for users in concurrencies:
            for target_name, (tags, request_name) in TARGETS.items():
                for repeat in range(1, args.repeats + 1):
                    index += 1
                    label = f"baseline-{tasks}-u{users}-{slug(target_name)}-r{repeat}"
                    print(f"[{index}/{total}] {label} ...")
                    config = build_config(
                        label,
                        tasks,
                        users,
                        tags,
                        args.duration,
                        args.comments_per_task,
                        out_dir,
                        Path(args.locustfile),
                        args.warmup,
                    )
                    result = execute_run(config, verbose=False)
                    if "error" in result:
                        print(f"    FAILED: {result['error']}")
                        records.append(
                            {
                                "label": label,
                                "target": target_name,
                                "dataset_tasks": tasks,
                                "concurrency": users,
                                "repeat": repeat,
                                "error": result["error"],
                            }
                        )
                        continue
                    summary = result["summary"]
                    endpoints = summary.get("endpoints", [])
                    # Use only this endpoint's row; the aggregated row would also contain
                    # the per-user bootstrap request.
                    row = next((item for item in endpoints if item.get("name") == request_name), None)
                    if row is None:
                        print(f"    FAILED: no '{request_name}' row in the Locust report")
                        records.append(
                            {
                                "label": label,
                                "target": target_name,
                                "dataset_tasks": tasks,
                                "concurrency": users,
                                "repeat": repeat,
                                "error": f"no '{request_name}' row in the Locust report",
                            }
                        )
                        continue
                    metadata = result["metadata"]
                    record = {
                        "label": label,
                        "target": target_name,
                        "request_name": request_name,
                        "dataset_tasks": tasks,
                        "concurrency": users,
                        "repeat": repeat,
                        "duration": args.duration,
                        "total_requests": int(row.get("request_count", 0)),
                        "successful_requests": int(row.get("request_count", 0))
                        - int(row.get("failure_count", 0)),
                        "failed_requests": int(row.get("failure_count", 0)),
                        "failure_rate": round(float(row.get("failure_rate", 0.0)), 6),
                        "requests_per_second": round(float(row.get("requests_per_second", 0.0)), 2),
                        "average_ms": round(float(row.get("average_ms", 0.0)), 2),
                        "median_ms": round(float(row.get("median_ms", 0.0)), 2),
                        "p95_ms": round(float(row.get("p95_ms", 0.0)), 2),
                        "p99_ms": round(float(row.get("p99_ms", 0.0)), 2),
                        "min_ms": round(float(row.get("min_ms", 0.0)), 2),
                        "max_ms": round(float(row.get("max_ms", 0.0)), 2),
                        "api_mean_cpu_percent": metadata.get("api_mean_cpu_percent"),
                        "api_max_cpu_percent": metadata.get("api_max_cpu_percent"),
                        "api_mean_rss_mb": metadata.get("api_mean_rss_mb"),
                        "api_max_rss_mb": metadata.get("api_max_rss_mb"),
                        "endpoints": endpoints,
                    }
                    records.append(record)
                    print(
                        f"    req={record['total_requests']} fail={record['failed_requests']} "
                        f"rps={record['requests_per_second']} avg={record['average_ms']}ms "
                        f"p95={record['p95_ms']}ms p99={record['p99_ms']}ms"
                    )

    aggregates = aggregate(records)
    payload = {
        "generated_utc": started.isoformat(timespec="seconds"),
        "finished_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "duration_per_run": args.duration,
        "repeats_per_configuration": args.repeats,
        "datasets": datasets,
        "concurrency_levels": concurrencies,
        "targets": list(TARGETS),
        "records": records,
        "aggregates": aggregates,
    }
    (out_dir / "baseline_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    for tasks in datasets:
        write_dataset_report(out_dir, tasks, records, aggregates, args.duration, args.repeats)
    print()
    print(f"written: {out_dir / 'baseline_summary.json'}")
    for tasks in datasets:
        print(f"written: {out_dir / f'baseline_{tasks}_tasks.txt'}")
    return payload


def aggregate(records: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    """Group repeats per (target, dataset, concurrency) and summarise the distribution."""
    buckets: dict[tuple[str, int, int], list[dict[str, object]]] = {}
    for record in records:
        if "error" in record:
            continue
        key = (str(record["target"]), int(record["dataset_tasks"]), int(record["concurrency"]))
        buckets.setdefault(key, []).append(record)

    result: dict[str, dict[str, object]] = {}
    for (target, tasks, users), rows in sorted(buckets.items()):
        key = f"{target} | tasks={tasks} | users={users}"
        result[key] = {
            "target": target,
            "dataset_tasks": tasks,
            "concurrency": users,
            "runs": len(rows),
            "total_requests": sum(int(row["total_requests"]) for row in rows),
            "failed_requests": sum(int(row["failed_requests"]) for row in rows),
            "failure_rate": round(
                sum(int(row["failed_requests"]) for row in rows)
                / max(1, sum(int(row["total_requests"]) for row in rows)),
                6,
            ),
            "requests_per_second": _numeric([float(row["requests_per_second"]) for row in rows]),
            "average_ms": _numeric([float(row["average_ms"]) for row in rows]),
            "median_ms": _numeric([float(row["median_ms"]) for row in rows]),
            "p95_ms": _numeric([float(row["p95_ms"]) for row in rows]),
            "p99_ms": _numeric([float(row["p99_ms"]) for row in rows]),
            "api_mean_cpu_percent": _numeric(
                [float(row["api_mean_cpu_percent"]) for row in rows if row["api_mean_cpu_percent"] is not None]
            ),
            "api_max_rss_mb": _numeric(
                [float(row["api_max_rss_mb"]) for row in rows if row["api_max_rss_mb"] is not None]
            ),
        }
    return result


def write_dataset_report(
    out_dir: Path,
    tasks: int,
    records: list[dict[str, object]],
    aggregates: dict[str, dict[str, object]],
    duration: str,
    repeats: int,
) -> None:
    """Write the human readable per-dataset baseline table (generated, never hand edited)."""
    lines: list[str] = []
    lines.append("=" * 118)
    lines.append(f"Week 4 Phase 3 baseline - {tasks} tasks (generated, do not edit by hand)")
    lines.append("=" * 118)
    lines.append(f"duration per run: {duration}    repeats per configuration: {repeats}")
    lines.append("database: SQLite file (throw-away per run)    server: single uvicorn process")
    lines.append("")
    header = (
        f"{'target':<22}{'users':>6}{'runs':>6}{'requests':>10}{'failed':>8}{'fail%':>8}"
        f"{'rps':>9}{'avg ms':>9}{'med ms':>9}{'p95 ms':>9}{'p99 ms':>9}{'cpu%':>8}"
    )
    lines.append(header)
    lines.append("-" * len(header))
    for _key, row in aggregates.items():
        if int(row["dataset_tasks"]) != tasks:
            continue
        rps = row["requests_per_second"]
        avg = row["average_ms"]
        med = row["median_ms"]
        p95 = row["p95_ms"]
        p99 = row["p99_ms"]
        cpu = row["api_mean_cpu_percent"]
        lines.append(
            f"{str(row['target']):<22}{int(row['concurrency']):>6}{int(row['runs']):>6}"
            f"{int(row['total_requests']):>10}{int(row['failed_requests']):>8}"
            f"{float(row['failure_rate']) * 100:>8.3f}"
            f"{rps['mean']:>9}{avg['mean']:>9}{med['mean']:>9}{p95['mean']:>9}{p99['mean']:>9}"
            f"{(cpu['mean'] if cpu['mean'] is not None else 0):>8.1f}"
        )
    lines.append("")
    lines.append("rps/avg/med/p95/p99/cpu are the MEAN over the repeated runs of that configuration.")
    lines.append("")
    lines.append("individual runs (raw values as measured)")
    lines.append("-" * 118)
    lines.append(
        f"{'run label':<52}{'requests':>10}{'failed':>8}{'rps':>9}{'avg ms':>9}{'med ms':>9}{'p95 ms':>9}{'p99 ms':>9}"
    )
    for record in records:
        if int(record.get("dataset_tasks", -1)) != tasks:
            continue
        if "error" in record:
            lines.append(f"{str(record['label']):<52}  FAILED: {record['error']}")
            continue
        lines.append(
            f"{str(record['label']):<52}{int(record['total_requests']):>10}"
            f"{int(record['failed_requests']):>8}{float(record['requests_per_second']):>9}"
            f"{float(record['average_ms']):>9}{float(record['median_ms']):>9}"
            f"{float(record['p95_ms']):>9}{float(record['p99_ms']):>9}"
        )
    lines.append("")
    (out_dir / f"baseline_{tasks}_tasks.txt").write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_matrix(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
