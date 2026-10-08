# Load test summary

*Source CSV:* `C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-final\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | week5-auth-smoke-final |
| timestamp_utc | 2026-10-08T04:59:45+00:00 |
| dataset_tasks | 20 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 3 |
| users | 1 |
| spawn_rate | 1.0 |
| run_time | 12s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:50939 |
| tags | (all scenarios) |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 1 -r 1.0 -t 12s --host http://127.0.0.1:50939 --csv C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-final\locust --html C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-final\locust_report.html --only-summary --loglevel WARNING |
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
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_shuo05nm/week4_perf_tasks.db |
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
| request_count | 34.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 3.13 |
| average_ms | 16.06 |
| median_ms | 15.00 |
| p95_ms | 32.00 |
| p99_ms | 33.00 |
| min_ms | 9.10 |
| max_ms | 33.28 |
| average_content_size | 2603.50 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 1 | 0 | 0.00 | 0.09 | 33.28 | 33.28 | 33.00 | 33.00 |
| /tasks/stats | 1 | 0 | 0.00 | 0.09 | 23.12 | 23.12 | 23.00 | 23.00 |
| /tasks/{id} | 6 | 0 | 0.00 | 0.55 | 11.25 | 11.00 | 15.00 | 15.00 |
| /tasks?limit=200 | 3 | 0 | 0.00 | 0.28 | 14.09 | 14.00 | 15.00 | 15.00 |
| /tasks?limit=50 | 10 | 0 | 0.00 | 0.92 | 16.44 | 16.00 | 32.00 | 32.00 |
| /tasks?priority=<value> | 2 | 0 | 0.00 | 0.18 | 19.26 | 21.00 | 21.00 | 21.00 |
| /tasks?q=<term> | 5 | 0 | 0.00 | 0.46 | 14.59 | 14.00 | 22.00 | 22.00 |
| /tasks?status=<value> | 6 | 0 | 0.00 | 0.55 | 17.33 | 17.00 | 27.00 | 27.00 |
