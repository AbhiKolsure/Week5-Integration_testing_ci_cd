# Week 4 - Performance Testing and Load Testing

This document explains the load-testing infrastructure added for Week 4. It is built on
top of the existing Week 3 backend **without changing any application behaviour**: no
route, query, schema, model or index was modified. Everything here is additive
(scripts, a locustfile, one test module, documentation, and one dependency).

The load generator is **Locust** (`locustfile` at `benchmarks/locustfile.py`). It was
chosen because it runs cleanly on this environment (Python 3.14.3, Locust 2.46.6,
gevent 26.9.0) and gives request counts, failure rates, RPS and percentile latencies out
of the box.

## 1. What is measured

For every scenario and for the run as a whole:

| Metric | Where it comes from |
| --- | --- |
| request count | Locust |
| successful / failed requests | Locust |
| failure rate | derived from the two counts above |
| requests per second | Locust |
| average / median / p95 / p99 response time | Locust |
| min / max response time, average content size | Locust |
| **database query count** | `scripts/performance/measure_query_counts.py` (exact, via `before_cursor_execute`) |

Locust measures wall-clock latency over **real HTTP**; the query-count script measures
the **deterministic** number of SQL statements per endpoint. Query counts are the metric
that survives machine differences, so both are kept side by side.

## 2. Prerequisites

```powershell
python -m pip install -r requirements.txt   # now includes locust>=2.20
```

Verified versions on the reference machine: Python 3.14.3, Locust 2.46.6, gevent 26.9.0,
FastAPI 0.141.1, SQLAlchemy 2.0.52.

## 3. Directory layout

```
benchmarks/locustfile.py                     # Locust scenarios (the virtual users)
scripts/performance/seed_dataset.py          # deterministic dataset generator
scripts/performance/locust_summary.py        # Locust CSV -> JSON/Markdown summary
scripts/performance/run_load_test.py         # one-command reproducible orchestrator
scripts/performance/measure_query_counts.py  # exact SQL statement counts per scenario
tests/performance/test_performance_infra.py  # pytest smoke tests for the harness
artifacts/performance/                       # every run's evidence (see its README)
```

## 4. Quick start (smoke test)

```powershell
python scripts/performance/run_load_test.py --tasks 200 --users 3 --spawn-rate 3 --run-time 8s --label smoke
```

This seeds 200 tasks, starts `uvicorn` on a free port, runs 3 users for 8 seconds, and
writes the results to `artifacts/performance/smoke/`. It is the check that the whole
pipeline works before a real baseline run.

## 5. The deterministic dataset

`scripts/performance/seed_dataset.py` builds every column value as a pure function of the
row index, so the same arguments always produce the same rows:

```powershell
python scripts/performance/seed_dataset.py --tasks 1000  --comments-per-task 1 --database week4_tasks.db
python scripts/performance/seed_dataset.py --tasks 10000 --comments-per-task 1 --database week4_tasks.db
```

* Data is bulk-inserted (fast even at 10,000 tasks).
* Status/priority cycle deterministically; every 5th task is overdue.
* The token `burndown` appears in every 7th task's description and nowhere else, so the
  `?q=burndown` scenario has a verifiable number of matches:
  `expected_search_matches(n) == (n - 1) // 7 + 1` (143 for 1,000; 1,429 for 10,000).
* The orchestrator seeds a **throw-away** database in the system temp directory; it never
  touches the development database.

## 6. Running the load test (recommended)

```powershell
# 1,000-task baseline
python scripts/performance/run_load_test.py --tasks 1000  --users 20 --run-time 30s --label baseline-1000

# 10,000-task baseline
python scripts/performance/run_load_test.py --tasks 10000 --users 50 --run-time 60s --label baseline-10000
```

Options:

| Option | Default | Meaning |
| --- | --- | --- |
| `--tasks` | 1000 | seeded dataset size |
| `--comments-per-task` | 1 | comments per task |
| `--users` | 10 | concurrent Locust users |
| `--spawn-rate` | 2.0 | users started per second |
| `--run-time` | 30s | duration (`30s`, `2m`, ...) |
| `--page-size` | 50 | default `limit` for the list scenarios |
| `--full-page` | 200 | `limit` for the full-page scenario |
| `--search-term` | burndown | term for the `?q=` scenario |
| `--filter-status` | pending | value for the `?status=` scenario |
| `--filter-priority` | high | value for the `?priority=` scenario |
| `--label` | `dataset-<n>-users-<u>` | artifact sub-directory name |
| `--out-dir` | `artifacts/performance` | artifact root |
| `--locustfile` | `benchmarks/locustfile.py` | scenarios file |
| `--database` | temp file | reuse a specific SQLite path |
| `--keep-database` | off | keep the seeded database file |

## 7. Scenarios (`benchmarks/locustfile.py`)

One virtual user class, `TaskApiUser`, mixes the read endpoints with weights:

| Scenario | Request | Weight |
| --- | --- | --- |
| `list_first_page` | `GET /tasks?limit=50` | 5 |
| `list_full_page` | `GET /tasks?limit=200` | 3 |
| `list_filtered_by_status` | `GET /tasks?status=pending` | 3 |
| `list_filtered_by_priority` | `GET /tasks?priority=high` | 2 |
| `search` | `GET /tasks?q=burndown` | 3 |
| `list_combined_filters` | `GET /tasks?status=&priority=` | 2 |
| `single_task` | `GET /tasks/{id}` | 2 |
| `task_comments` | `GET /tasks/{id}/comments` | 1 |
| `statistics` | `GET /tasks/stats` | 1 |

Each request carries a fixed `name=`, so the CSV groups per endpoint. `on_start`
bootstraps real task ids (recorded as `/tasks [bootstrap]`) so the single-resource
scenarios hit existing rows.

## 8. Running Locust directly (manual / web UI)

```powershell
# start the API yourself first, on a seeded database
$env:DATABASE_URL = "sqlite:///./week4_tasks.db"
python scripts/performance/seed_dataset.py --tasks 1000 --database week4_tasks.db
python -m uvicorn app.main:app --port 8000        # terminal 1

python -m locust -f benchmarks/locustfile.py --host http://127.0.0.1:8000   # terminal 2
# web UI at http://127.0.0.1:8089 ; or headless:
python -m locust -f benchmarks/locustfile.py --headless -u 20 -r 2 -t 30s --host http://127.0.0.1:8000
```

Scenario parameters can be overridden with `LOAD_PAGE_SIZE`, `LOAD_FULL_PAGE`,
`LOAD_SEARCH_TERM`, `LOAD_FILTER_STATUS`, `LOAD_FILTER_PRIORITY`, `LOAD_SAMPLE_IDS`,
`LOAD_WAIT_MIN`, `LOAD_WAIT_MAX`.

## 9. Measuring SQL query counts

```powershell
python scripts/performance/measure_query_counts.py --tasks 1000 --out artifacts/performance/query_counts-1000.json
python scripts/performance/measure_query_counts.py --tasks 10000
```

This runs the exact same nine scenarios in-process against an in-memory SQLite database
and prints the deterministic statement count per scenario. It is the reproducible
counterpart to the Locust latency numbers.

## 10. Interpreting the artifacts

Every run writes `artifacts/performance/<label>/`:

* `summary.md` - readable totals + per-endpoint table (with the full environment block).
* `summary.json` - the same numbers, machine-readable.
* `run_metadata.json` - dataset, users, duration, parameters, environment, exact command.
* `locust_stats.csv`, `locust_failures.csv`, `locust_report.html` - raw Locust output.
* `uvicorn_stdout.txt` - server log for the run.

See `artifacts/performance/README.md` for the metric glossary.

## 11. Reproducibility: what is recorded

A run is reproducible when these are held constant, and all of them are captured in
`run_metadata.json`:

* **dataset size** (`dataset_tasks`, `dataset_comments_per_task`, `dataset_search_matches`)
* **concurrency** (`users`, `spawn_rate`)
* **duration** (`run_time`)
* **request parameters** (`page_size`, `full_page_size`, `search_term`, `filter_status`, `filter_priority`)
* **environment** (Python, OS platform, machine, CPU count, FastAPI/Starlette/Pydantic/SQLAlchemy/uvicorn/Locust/gevent versions)
* **database type and URL** (`database_type`, `database_url`)
* **the exact command** (`locust_command`)

Re-running the same command line reproduces the same dataset and the same scenario mix.
Locust latency itself is a timing measurement and therefore only comparable within the
same machine/conditions - query counts are the machine-independent metric.

## 12. Suggested baseline experiments

Run these in order and keep the artifacts:

```powershell
python scripts/performance/run_load_test.py --tasks 200   --users 3  --spawn-rate 3 --run-time 8s  --label smoke
python scripts/performance/run_load_test.py --tasks 1000  --users 20 --run-time 30s --label baseline-1000
python scripts/performance/run_load_test.py --tasks 10000 --users 50 --run-time 60s --label baseline-10000
python scripts/performance/measure_query_counts.py --tasks 1000
python scripts/performance/measure_query_counts.py --tasks 10000
```

Compare `baseline-1000` with `baseline-10000` to see how `GET /tasks` and
`GET /tasks/stats` scale with dataset size, and use the query-count output to confirm
whether the statement count per request stays constant.

## 13. Limitations (stated honestly)

* The server is a **single** `uvicorn` process; FastAPI runs the synchronous endpoints in
  its default threadpool, so concurrency is bounded by that threadpool as well as by
  SQLite.
* SQLite is used in its **default journal mode** (no WAL), so write-heavy mixes serialise
  on a database-level lock. The read-only scenarios here are not affected, but this must
  be kept in mind before interpreting any write-path numbers.
* Latency figures are single-machine observations, not a capacity statement. Run-to-run
  variance is real; report medians/percentiles and repeat runs.
* The `?q=` search uses a leading-wildcard `LIKE` and cannot use an index, so its cost
  grows with the table size by design - this is a property of the existing query, not a
  regression, and it is **not** optimised in Week 4 Phase 2.
* No application behaviour, index, model or query was changed; these tests only measure.

## 14. Week 3 regression guard (unchanged)

The existing suites keep running untouched:

```powershell
python -m pytest -q                       # 102 functional tests
python -m pytest -m performance -v        # SQL statement budgets + latency budget
python -m pytest -m loadtest -v           # the new infrastructure smoke tests
python -m ruff check .
```

The `loadtest` marker was registered in `pyproject.toml`; it does not affect the existing
`performance` marker or the default test run.

## 15. Week 5 authentication compatibility

Week 5 adds bearer-token protection to the task API. The Week 4 in-process benchmark,
defect-reproduction, database-check, and query-count harnesses now seed an isolated
benchmark user and attach a signed token before making task requests. The Locust
orchestrator creates a temporary account through the auth API, logs in before warm-up,
and supplies its token to the Locust process without writing the token to run metadata.
When running Locust directly, set `LOAD_AUTH_TOKEN` to a valid access token first.

The existing Week 4 performance artifacts predate authentication. They are retained as
historical evidence and are not directly comparable to new measurements that include
the authentication lookup. No Week 5 load measurements are claimed by this update.