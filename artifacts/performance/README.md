# artifacts/performance

Every load-test run writes its evidence into `artifacts/performance/<label>/`.
Nothing here is hand-edited - the files are produced by
`scripts/performance/run_load_test.py`, so a run is only ever compared with another
run that used the same command line.

## Layout

```
artifacts/performance/
└── <label>/                        # e.g. baseline-1000, baseline-10000, smoke
    ├── run_metadata.json           # dataset, users, duration, params, environment, exact command
    ├── summary.json                # machine-readable metrics (totals + per endpoint)
    ├── summary.md                  # human-readable report
    ├── locust_stats.csv            # raw Locust per-endpoint statistics (source of truth)
    ├── locust_failures.csv         # raw Locust failures (empty when failure rate is 0)
    ├── locust_exceptions.csv       # raw Locust exceptions (empty when none)
    ├── locust_stats_history.csv    # raw Locust time series
    ├── locust_stdout.txt           # full Locust console output
    ├── locust_report.html          # self-contained Locust HTML dashboard
    └── uvicorn_stdout.txt          # server log captured during the run (when non-empty)
```

## Metric glossary (`summary.json`)

| Key | Meaning |
| --- | --- |
| `request_count` | Number of completed requests |
| `failure_count` | Requests that answered >= 400 or were marked failed |
| `failure_rate` | `failure_count / request_count` |
| `requests_per_second` | Throughput |
| `average_ms` / `median_ms` | Mean and median response time |
| `p95_ms` / `p99_ms` | 95th / 99th percentile response time |
| `min_ms` / `max_ms` | Fastest / slowest response time |
| `average_content_size` | Average response body size in bytes |

`aggregated` holds the totals; `endpoints` holds one entry per named scenario, so the
`GET /tasks` variants can be compared against each other.

The equivalent **database** view (exact SQL statement counts per scenario, independent
of timing) is written by `scripts/performance/measure_query_counts.py` to
`artifacts/performance/query_counts-<tasks>.json`.
