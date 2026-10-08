# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u10-get-tasks-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-10000-u10-get-tasks-r2 |
| timestamp_utc | 2026-10-03T09:17:24+00:00 |
| dataset_tasks | 10000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 1429 |
| users | 10 |
| spawn_rate | 2.0 |
| run_time | 20s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:56599 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 20s --host http://127.0.0.1:56599 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u10-get-tasks-r2\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u10-get-tasks-r2\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 43 |
| api_mean_cpu_percent | 24.08 |
| api_max_cpu_percent | 46.4 |
| api_mean_rss_mb | 83.81 |
| api_max_rss_mb | 85.1 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_0pkq56h8/week4_perf_tasks.db |
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
| request_count | 517.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 28.51 |
| average_ms | 14.49 |
| median_ms | 12.00 |
| p95_ms | 26.00 |
| p99_ms | 40.00 |
| min_ms | 6.65 |
| max_ms | 60.77 |
| average_content_size | 12227.10 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.55 | 21.98 | 22.00 | 28.00 | 28.00 |
| /tasks?limit=50 | 507 | 0 | 0.00 | 27.96 | 14.34 | 11.00 | 25.00 | 40.00 |
