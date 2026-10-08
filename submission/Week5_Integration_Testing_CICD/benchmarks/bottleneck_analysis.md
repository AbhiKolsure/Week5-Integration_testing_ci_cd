# Week 4 Phase 4 - Bottleneck Analysis

**No application code was changed in this phase.** This document analyses only evidence
already generated in this project, plus two structural probes (SQLite query plans and
engine introspection) that read the real configuration.

Sources of evidence:

| Artifact | What it provides |
| --- | --- |
| `artifacts/performance/baseline_1000_tasks.txt`, `baseline_10000_tasks.txt` | 24 Locust runs: 2 datasets x 3 concurrency levels x 2 endpoints x 2 repeats |
| `artifacts/performance/baseline_summary.json` | per-run records and aggregates |
| `artifacts/performance/query_counts-1000.json`, `query_counts-10000.json` | exact statement counts + per-statement DB ms |
| SQLite `EXPLAIN QUERY PLAN` on the seeded 10,000-row database | structural access paths |
| `app.database.engine` introspection | pool class / size / overflow / timeout |
| `artifacts/performance/*-invalid-contaminated/` | rejected probe runs (see B4) |

---

## 0. Reliability of the evidence (read this first)

Two measurements that are stable, and one that is not:

* **Statement counts are deterministic.** Repeated runs at 1,000 and 10,000 rows return
  exactly `3` statements for every `GET /tasks` variant and `6` for `GET /tasks/stats`,
  every time. These are exact and are asserted by `tests/test_performance.py`.
* **Access paths are deterministic.** `EXPLAIN QUERY PLAN` returns the same plan on every
  execution; these are structural facts.
* **Timings are NOT stable on this machine.** Re-running
  `measure_query_counts.py --tasks 1000` gave `GET /tasks/stats` = **0.813 ms** in the
  recorded artifact and **0.376 ms** on re-run (2.2x apart), and `?q=burndown` = 1.431 ms
  vs 0.566 ms (2.5x apart). `GET /tasks?limit=50` was stable (0.120 vs 0.125 ms).

Every conclusion below is therefore argued from **order-of-magnitude gaps far larger than
the observed noise**, from **counts/plans** (noise-free), or is explicitly labelled
*suspected*.

---

## 1. CONFIRMED BOTTLENECKS

### B1 - For `GET /tasks` the database is NOT the bottleneck; the cost is in the ASGI/Python layer

1. **Observed symptom** - latency rises ~15x while throughput rises only 3.4x as users go
   10 -> 50; average latency goes 9.87 -> 25.37 -> **152.96 ms** at 1,000 tasks.
2. **Exact measurement** - per-request SQL time for `GET /tasks?limit=50` is
   **0.120 ms @1k** and **0.245 ms @10k**, against measured HTTP averages of
   **9.87 ms** and **13.21 ms** (10 users) and **167.19 ms** (50 users, 10k).
   Database share: **~1.2 % / ~1.9 % / ~0.15 %** - a gap of 2-3 orders of magnitude that
   survives the 2-4x timing noise.
3. **Endpoint** - `GET /tasks` (all variants).
4. **Source** - `app/routes/tasks.py::list_tasks` -> `app/crud.py::list_tasks` and
   `app/crud.py::to_task_reads`; response assembly via `app/schemas.py::TaskRead` /
   `TaskList`.
5. **Root cause** - only ~0.25 ms of a 13-167 ms request is SQL. The remainder is ASGI
   dispatch, threadpool hand-off (the handlers are `def`, so they run in a worker thread),
   Pydantic validation and JSON encoding of a ~12.3 kB body.
6. **Why it matters** - **no index, query rewrite or SQL-level cache can recover the
   measured latency.** The lever must lie outside the database.
7. **Candidate optimization** - reduce per-request Python work in response construction
   (see S2) or cache the rendered response.
8. **Trade-offs** - touching `TaskRead` risks the response contract pinned by 102 tests.
9. **Validation** - `GET /tasks?limit=50` avg / p95 ms and API CPU % at the Phase 3
   configurations, compared against `baseline_1000_tasks.txt`.

### B2 - `GET /tasks/stats` performs a full table scan on the unindexed `due_date` column

1. **Symptom** - `/tasks/stats` is the only endpoint whose cost is dominated by the
   database (~19 % of the request at 10,000 tasks / 10 users).
2. **Exact measurement** - `query_counts-10000.json`: the slowest single statement in the
   entire project is
   `SELECT count(tasks.id) FROM tasks WHERE due_date IS NOT NULL AND due_date < ? AND status != ?`
   at **2.726 ms**, out of a **4.054 ms** endpoint total (67 % of it).
   `EXPLAIN QUERY PLAN` for that statement returns **`SCAN tasks`** - no index.
3. **Endpoint** - `GET /tasks/stats`.
4. **Source** - `app/crud.py::get_statistics` (the `overdue` count); the column is
   `app/models.py::Task.due_date` (`mapped_column(DateTime, nullable=True)`, **no
   `index=True`**).
5. **Root cause** - the overdue predicate filters on `due_date` and `status`, and there is
   no index on `due_date`, so SQLite scans every row. The other five stats statements use
   covering index scans (`ix_tasks_id`, `ix_tasks_status`) and cost 0.32-0.39 ms combined.
6. **Why it matters** - it is a whole-table scan whose cost grows linearly with rows, so it
   degrades as the backlog grows, unlike the rest of the read path.
7. **Candidate optimization** - index `due_date`, and/or fold the overdue count into the
   same pass as the other aggregates.
8. **Trade-offs** - an index costs write throughput and storage; SQLite may still prefer a
   scan for a selective predicate, so the plan must be re-checked, not assumed.
9. **Validation** - `EXPLAIN QUERY PLAN` must change from `SCAN tasks` to
   `SEARCH tasks USING INDEX ...`, and `measure_query_counts.py --tasks 10000` must show
   the stats total dropping from **4.054 ms**.
### B3 - Search (`?q=`) forces a full table scan

1. **Symptom** - `?q=burndown` is by far the most expensive list query.
2. **Exact measurement** - **6.604 ms @10k** vs **0.245 ms** for the unfiltered list at the
   same size (27x); at 1,000 rows 1.431 ms vs 0.120 ms. `EXPLAIN QUERY PLAN` returns
   **`SCAN tasks`**.
3. **Endpoint** - `GET /tasks?q=...`.
4. **Source** - `app/crud.py::_build_filter` ->
   `or_(Task.title.ilike('%q%'), Task.description.ilike('%q%'))`.
5. **Root cause** - a leading wildcard can never use a B-tree index. `ix_tasks_title`
   exists but is unusable for this predicate, and `description` has no index at all.
6. **Why it matters** - cost is linear in table size; it breaks first as the dataset grows.
7. **Candidate optimization** - an FTS5 index, or a prefix-only indexing strategy, or an
   explicit cap on scanned rows.
8. **Trade-offs** - FTS5 changes matching semantics (tokenisation) and requires a schema
   migration plus a rebuild of any existing `week3_tasks.db`.
9. **Validation** - `measure_query_counts.py --tasks 10000` `?q=burndown`
   **6.604 ms -> < 1 ms** *and* an identical match count (1429 at 10k) before and after.

### B4 - The measurement environment is itself a bottleneck (affects every number)

1. **Symptom** - identical configurations produce wildly different results across sessions.
2. **Exact measurement** - `GET /tasks?limit=50`, 1,000 tasks, 25 users, 20 s, spawn 5:
   **68.75 rps / 25.37 ms** (Phase 3) vs **~30 rps / 244 ms** (probe 1) vs
   **~6.8-13.0 rps / 1,334-2,889 ms** (probe 2). `/tasks/stats` DB time varied
   0.813 -> 0.376 ms between identical runs. Background processes during the probes:
   **OneDrive 7,483 s cumulative CPU**, **OneDrive.Sync.Service 3,465 s**, several VS Code
   processes, with only **2,814 MB of 16,088 MB** RAM free.
3. **Endpoint** - all.
4. **Source** - host environment, not the repository.
5. **Root cause** - unsynchronised background CPU/IO consumers on a shared desktop. The
   artifact directory had reached 63.7 MB, a plausible sync trigger.
6. **Why it matters** - **timings measured now are not comparable with timings measured
   earlier.** Any before/after claim here without controlling background load is unsafe.
   This is why the Phase 4 page-size experiment was discarded.
7. **Candidate optimization** - pause OneDrive during runs; measure on an idle machine;
   record background CPU alongside each run.
8. **Trade-offs** - requires host control the project does not have.
9. **Validation** - repeat one baseline configuration 5x and require a small spread in rps
   and p95 before accepting any optimization result.

---

## 2. SUSPECTED BOTTLENECKS (plausible, not proven)

### S1 - The DB connection pool allows only 15 concurrent connections

* **Observed symptom** - unexplained latency step under higher concurrency.
* **Exact measurement (structural fact)** - `app.database.engine.pool` is **`QueuePool`**,
  `size() = 5`, `max_overflow = 10`, `timeout = 30.0` -> **15 connections maximum**.
* **Source** - `app/database.py` (module-level `create_engine(...)` with no `pool_*`
  arguments); `app/database.py::get_db` yields a `Session` for the whole request, so the
  checked-out connection is not released until dependency teardown. On FastAPI >= 0.106
  (installed 0.141.1) teardown runs *after* the response is produced, so the connection is
  held during Pydantic/JSON serialisation too.
* **Root cause** - default pool sizing, unsized for a concurrent read workload.
* **Why it might matter** - with 50 concurrent users, Little's law on the Phase 3 numbers
  gives average in-flight requests = 97.35 rps x 0.15296 s = **14.9**, strikingly close to
  the 15-connection ceiling. (`/tasks/stats` at 50 users gives 113.75 x 0.08651 = 9.8, so
  the coincidence is not uniform.)
* **Why it is only SUSPECTED** - `pool.checkedout()` was never measured, and the `stats`
  figure above contradicts a hard cap at 15.
* **Candidate optimization** - size the pool for the expected concurrency, or release the
  connection before serialisation.
* **Trade-offs** - more connections against a SQLite file increase lock contention; the
  measured `journal_mode=delete` makes writers worse, not readers.
* **Validation** - instrument `engine.pool.checkedout()` at 0.5 s intervals during a
  50-user run. If it pins at 15, S1 is confirmed; if it never approaches 15, S1 is
  **rejected**.

### S2 - Per-row response construction is a large share of the non-DB cost

* **Source** - `app/crud.py::to_task_reads` runs `schemas.TaskRead.model_validate(task)`
  **and** `.model_copy(update=...)` for **every row**, and FastAPI then validates the whole
  payload again against the `TaskList` `response_model`; the 50-row body measured 12,345
  bytes on average.
* **Root cause** - two Pydantic passes over every row plus a third validation of the
  envelope.
* **Why it might matter** - it is pure CPU inside the GIL, the resource Phase 3 showed to be
  saturating (API CPU 18 % -> 130 %).
* **Why it is only SUSPECTED** - the experiment designed to test it (same endpoint at page
  size 1 / 50 / 200 under identical load) produced 68.75 vs ~30 vs ~10 rps for the *same*
  configuration, so its output was discarded as contaminated (B4). **No page-size
  conclusion is claimed.**
* **Candidate optimization** - build the response mapping once (avoid validate-then-copy),
  or return plain dicts, or use a faster JSON response class.
* **Trade-offs** - all three weaken the Pydantic validation that 102 tests rely on and risk
  changing the JSON contract.
* **Validation** - re-run `GET /tasks?limit=1` vs `?limit=50` vs `?limit=200` at 1,000
  tasks / 25 users, 2 repeats each, **only after** B4 is controlled. Flat latency across
  page sizes rejects S2 and points to fixed per-request overhead instead.

### S3 - GIL contention limits the benefit of extra uvicorn workers

* **Source** - the route handlers are declared `def`, so FastAPI runs them in an anyio
  worker thread.
* **Why it might matter** - Phase 3 CPU stayed at ~1.3-1.7 cores (psutil 130-169 %) while
  latency exploded, consistent with Python work not parallelising.
* **Why it is only SUSPECTED** - no worker-count experiment was run.
* **Trade-offs** - multiple uvicorn workers against one SQLite file introduces write-lock
  contention; with the measured `journal_mode=delete` that is a real risk.
* **Validation** - 1 vs 2 vs 4 workers under identical load; if rps does not rise, S3 is
  confirmed as the limiter and worker tuning is worthless here.

---

## 3. REJECTED HYPOTHESES

| Hypothesis | Verdict | Evidence |
| --- | --- | --- |
| An N+1 query regression has returned | **REJECTED** | Statement count is a flat `3` for every `/tasks` variant at both 1,000 and 10,000 rows, and identical for `limit=50` and `limit=200` (`query_counts-*.json`). No growth with page size or dataset size. |
| An index on `status`/`priority` would speed up `GET /tasks` | **REJECTED** | `EXPLAIN` shows the filtered list already uses covering index scans and SQL is ~1-2 % of the request (B1). Max possible gain ~2 %. |
| `COUNT(*)` in `crud.list_tasks` is a major cost | **REJECTED as a primary cause** | It is **0.040-0.042 ms** of the 0.245 ms total for `/tasks@10k`. It *is* dominant only for filtered/search queries (1.107 ms for status+priority, 6.604 ms for `?q=`) - already counted as B3. |
| Page size drives the latency | **INCONCLUSIVE - claim withdrawn** | The dedicated A/B experiment was invalidated by B4. No number is claimed. |
| More uvicorn workers will raise throughput | **UNSUPPORTED** | No experiment was run (S3). Not claimed either way. |
| The database is the bottleneck of `GET /tasks` | **REJECTED** | B1: 0.120-0.245 ms of SQL per request against 9.87-167.19 ms end-to-end. |

---

## 4. RECOMMENDED OPTIMIZATION EXPERIMENT

**First experiment (best evidence-to-risk ratio, verifiable with the noise-free metrics):**
add an index on `Task.due_date` for `GET /tasks/stats` (B2).

Why first:

* It is the **only** place where the evidence identifies a specific statement costing more
  than the rest of the request (2.726 ms of 4.054 ms).
* It is **verifiable without trusting timings**: `EXPLAIN QUERY PLAN` is deterministic and
  must flip from `SCAN tasks` to a `SEARCH ... USING INDEX`.
* It is **reversible** and does not touch the response contract, so it cannot break the
  102-test suite.

**Primary-endpoint experiment (for `GET /tasks`, only after B4 is controlled):** resolve S2
by re-running the page-size A/B (1 / 50 / 200). Depending on the result the next step is
either per-row construction removal or a response cache - explicitly **not** an index.

### Exact before/after metrics that decide success

| Experiment | Metric | Before (recorded in this repo) | After (success threshold) |
| --- | --- | --- | --- |
| `due_date` index (B2) | `EXPLAIN QUERY PLAN` of the overdue count | `SCAN tasks` | contains `SEARCH` + `USING INDEX` |
| `due_date` index (B2) | `measure_query_counts.py --tasks 10000`, `/tasks/stats` `total_db_ms` | **4.054 ms** | **< 1.0 ms** |
| `due_date` index (B2) | statement count for `/tasks/stats` | 6 | 6 (must not change) |
| `due_date` index (B2) | HTTP `/tasks/stats` avg ms, 10k / 10 users | **21.21 ms** | <= ~17 ms (the ~19 % DB share) |
| page-size A/B (S2) | `GET /tasks?limit=1` vs `?limit=50` avg ms, 1k / 25 users | limit=50 baseline **25.37 ms** | a >=3x gap proves per-row cost; <1.5x rejects S2 |
| any of the above | environment control | rps spread up to **10x** across identical runs (B4) | spread <15 % over 5 repeats, else the result is void |

---

## 5. Structural facts recorded during this analysis

| Fact | Value | Where read |
| --- | --- | --- |
| Connection pool | `QueuePool`, size 5, overflow 10, timeout 30 s | `app.database.engine.pool` |
| Journal mode | `delete` (not WAL) | `PRAGMA journal_mode` |
| Synchronous | `2` (FULL) | `PRAGMA synchronous` |
| SQLite page cache | `cache_size = -2000` (~2 MB) vs a ~3.4 MB database at 10k rows | `PRAGMA cache_size`, `page_count` |
| Indexes present | `tasks(id)`, `tasks(title)`, `tasks(status)`, `tasks(priority)`, `comments(id)`, `comments(task_id)` | SQLAlchemy inspector |
| Indexes absent | `tasks(due_date)`, `tasks(description)`, `tasks(created_at)` | SQLAlchemy inspector |
| Access paths | `SEARCH` (index) for the list page, the counts and the comment group-by; `SCAN tasks` for the overdue count and for `?q=` | `EXPLAIN QUERY PLAN` |