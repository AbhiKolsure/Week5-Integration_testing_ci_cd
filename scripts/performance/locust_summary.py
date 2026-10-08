"""Parse Locust CSV output into a stable, JSON-serialisable summary.

Locust writes ``<prefix>_stats.csv`` with one row per named request plus an aggregate
row. The column layout has changed slightly between Locust releases, so this module
looks columns up by name instead of by position and tolerates the optional percentile
columns (``95%`` / ``99%``) being absent.

Used by ``scripts/performance/run_load_test.py`` and by
``tests/performance/test_performance_infra.py``.
"""

from __future__ import annotations

import csv
from pathlib import Path

# Metric keys that every summary row carries (numeric, milliseconds where applicable).
METRIC_KEYS = (
    "request_count",
    "failure_count",
    "failure_rate",
    "requests_per_second",
    "average_ms",
    "median_ms",
    "p95_ms",
    "p99_ms",
    "min_ms",
    "max_ms",
    "average_content_size",
)

_COLUMN_ALIASES = {
    "request_count": ("Request Count",),
    "failure_count": ("Failure Count",),
    "requests_per_second": ("Requests/s",),
    "average_ms": ("Average Response Time",),
    "median_ms": ("Median Response Time",),
    "p95_ms": ("95%",),
    "p99_ms": ("99%",),
    "min_ms": ("Min Response Time", "Min"),
    "max_ms": ("Max Response Time", "Max"),
    "average_content_size": ("Average Content Size",),
}


def _to_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def _pick(row: dict[str, str], key: str) -> str | None:
    for column in _COLUMN_ALIASES[key]:
        if column in row:
            return row[column]
    return None


def _row_metrics(row: dict[str, str]) -> dict[str, float]:
    metrics = {key: _to_float(_pick(row, key)) for key in _COLUMN_ALIASES}
    request_count = metrics["request_count"]
    metrics["failure_rate"] = (metrics["failure_count"] / request_count) if request_count else 0.0
    return metrics


def is_aggregate_row(row: dict[str, str]) -> bool:
    """Locust marks the totals row with ``Type``/``Name`` == ``Aggregated``."""
    for column in ("Type", "Name"):
        if (row.get(column) or "").strip().lower() == "aggregated":
            return True
    return False


def parse_stats_csv(path: str | Path) -> dict[str, object]:
    """Parse a Locust ``*_stats.csv`` file into ``{"aggregated": ..., "endpoints": [...]}``."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Locust stats CSV not found: {csv_path}")

    aggregated: dict[str, float] | None = None
    endpoints: list[dict[str, object]] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if not any((value or "").strip() for value in row.values()):
                continue
            if is_aggregate_row(row):
                aggregated = _row_metrics(row)
                continue
            endpoints.append(
                {
                    "name": row.get("Name", ""),
                    "type": row.get("Type", ""),
                    **_row_metrics(row),
                }
            )

    if aggregated is None and endpoints:
        # Defensive: derive the aggregate from the endpoint rows if Locust omitted it.
        aggregated = {key: sum(float(item[key]) for item in endpoints) for key in ("request_count", "failure_count")}
        total = aggregated["request_count"]
        aggregated["failure_rate"] = (aggregated["failure_count"] / total) if total else 0.0

    return {"aggregated": aggregated, "endpoints": endpoints}


def _fmt(value: object) -> str:
    return f"{float(value):.2f}"


def render_markdown(summary: dict[str, object], metadata: dict[str, object], source: str) -> str:
    """Render a human-readable Markdown report for one load-test run."""
    aggregated = summary.get("aggregated") or {}
    lines: list[str] = []
    lines.append("# Load test summary")
    lines.append("")
    lines.append(f"*Source CSV:* `{source}`")
    lines.append("")
    lines.append("## Environment and dataset")
    lines.append("")
    lines.append("| Item | Value |")
    lines.append("| --- | --- |")
    for key, value in metadata.items():
        lines.append(f"| {key} | {value} |")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("| --- | --- |")
    for key in METRIC_KEYS:
        if key in aggregated:
            lines.append(f"| {key} | {_fmt(aggregated[key])} |")
    lines.append("")
    lines.append("## Per endpoint")
    lines.append("")
    header = "| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |"
    lines.append(header)
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for endpoint in summary.get("endpoints", []):
        lines.append(
            f"| {endpoint['name']} | {int(endpoint['request_count'])} | {int(endpoint['failure_count'])} "
            f"| {_fmt(endpoint['failure_rate'])} | {_fmt(endpoint['requests_per_second'])} "
            f"| {_fmt(endpoint['average_ms'])} | {_fmt(endpoint['median_ms'])} "
            f"| {_fmt(endpoint['p95_ms'])} | {_fmt(endpoint['p99_ms'])} |"
        )
    lines.append("")
    return "\n".join(lines)
