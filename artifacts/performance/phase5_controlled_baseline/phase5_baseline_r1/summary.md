# Load test summary

*Source CSV:* `artifacts\performance\phase5_controlled_baseline\phase5_baseline_r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | phase5_baseline_r1 |
| timestamp_utc | 2026-10-07T07:47:07+00:00 |
| dataset_tasks | 10000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 1429 |
| users | 10 |
| spawn_rate | 2.0 |
| run_time | 30s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:59308 |
| tags | (all scenarios) |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 30s --host http://127.0.0.1:59308 --csv artifacts\performance\phase5_controlled_baseline\phase5_baseline_r1\locust --html artifacts\performance\phase5_controlled_baseline\phase5_baseline_r1\locust_report.html --only-summary --loglevel WARNING |
| api_cpu_samples | None |
| api_mean_cpu_percent | None |
| api_max_cpu_percent | None |
| api_mean_rss_mb | None |
| api_max_rss_mb | None |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_tmvqxg77/week4_perf_tasks.db |
| fastapi | 0.141.1 |
| starlette | 1.6.0 |
| pydantic | 2.13.5 |
| sqlalchemy | 2.0.52 |
| uvicorn | 0.52.4 |
| locust | 2.46.6 |
| gevent | 26.9.0 |

## Totals

| Metric | Value |
| --- | --- |
| request_count | 862.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 29.47 |
| average_ms | 14.37 |
| median_ms | 12.00 |
| p95_ms | 29.00 |
| p99_ms | 39.00 |
| min_ms | 2.47 |
| max_ms | 122.95 |
| average_content_size | 15300.50 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.34 | 20.38 | 20.00 | 35.00 | 35.00 |
| /tasks/stats | 39 | 0 | 0.00 | 1.33 | 20.51 | 20.00 | 40.00 | 48.00 |
| /tasks/{id} | 71 | 0 | 0.00 | 2.43 | 7.77 | 8.00 | 14.00 | 24.00 |
| /tasks/{id}/comments | 39 | 0 | 0.00 | 1.33 | 8.86 | 8.00 | 15.00 | 29.00 |
| /tasks?limit=200 | 118 | 0 | 0.00 | 4.03 | 19.11 | 17.00 | 35.00 | 100.00 |
| /tasks?limit=50 | 199 | 0 | 0.00 | 6.80 | 11.97 | 11.00 | 24.00 | 39.00 |
| /tasks?priority=<value> | 73 | 0 | 0.00 | 2.50 | 11.98 | 11.00 | 21.00 | 29.00 |
| /tasks?q=<term> | 114 | 0 | 0.00 | 3.90 | 21.18 | 21.00 | 35.00 | 56.00 |
| /tasks?status=&priority= | 74 | 0 | 0.00 | 2.53 | 14.32 | 13.00 | 27.00 | 33.00 |
| /tasks?status=<value> | 125 | 0 | 0.00 | 4.27 | 12.01 | 11.00 | 22.00 | 28.00 |
