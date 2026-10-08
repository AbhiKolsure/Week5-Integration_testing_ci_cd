# Load test summary

*Source CSV:* `artifacts\performance\phase5_controlled_baseline\phase5_baseline_r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | phase5_baseline_r2 |
| timestamp_utc | 2026-10-07T07:47:44+00:00 |
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
| host | http://127.0.0.1:63323 |
| tags | (all scenarios) |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 30s --host http://127.0.0.1:63323 --csv artifacts\performance\phase5_controlled_baseline\phase5_baseline_r2\locust --html artifacts\performance\phase5_controlled_baseline\phase5_baseline_r2\locust_report.html --only-summary --loglevel WARNING |
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
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_nei9glqu/week4_perf_tasks.db |
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
| request_count | 873.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 29.89 |
| average_ms | 14.04 |
| median_ms | 12.00 |
| p95_ms | 31.00 |
| p99_ms | 43.00 |
| min_ms | 3.32 |
| max_ms | 69.34 |
| average_content_size | 15319.16 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.34 | 12.61 | 13.00 | 19.00 | 19.00 |
| /tasks/stats | 35 | 0 | 0.00 | 1.20 | 21.06 | 16.00 | 46.00 | 54.00 |
| /tasks/{id} | 72 | 0 | 0.00 | 2.47 | 7.87 | 7.00 | 15.00 | 31.00 |
| /tasks/{id}/comments | 38 | 0 | 0.00 | 1.30 | 7.18 | 6.00 | 19.00 | 20.00 |
| /tasks?limit=200 | 118 | 0 | 0.00 | 4.04 | 17.86 | 17.00 | 38.00 | 49.00 |
| /tasks?limit=50 | 215 | 0 | 0.00 | 7.36 | 12.21 | 11.00 | 25.00 | 31.00 |
| /tasks?priority=<value> | 82 | 0 | 0.00 | 2.81 | 11.61 | 10.00 | 28.00 | 35.00 |
| /tasks?q=<term> | 113 | 0 | 0.00 | 3.87 | 21.56 | 20.00 | 39.00 | 58.00 |
| /tasks?status=&priority= | 71 | 0 | 0.00 | 2.43 | 14.43 | 11.00 | 32.00 | 45.00 |
| /tasks?status=<value> | 119 | 0 | 0.00 | 4.07 | 11.81 | 10.00 | 27.00 | 38.00 |
