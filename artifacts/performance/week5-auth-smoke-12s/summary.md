# Load test summary

*Source CSV:* `C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-12s\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | week5-auth-smoke-12s |
| timestamp_utc | 2026-10-08T04:58:39+00:00 |
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
| host | http://127.0.0.1:55162 |
| tags | (all scenarios) |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 1 -r 1.0 -t 12s --host http://127.0.0.1:55162 --csv C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-12s\locust --html C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-12s\locust_report.html --only-summary --loglevel WARNING |
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
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_60sjz55a/week4_perf_tasks.db |
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
| requests_per_second | 3.16 |
| average_ms | 14.82 |
| median_ms | 14.00 |
| p95_ms | 22.00 |
| p99_ms | 37.00 |
| min_ms | 7.86 |
| max_ms | 36.98 |
| average_content_size | 3102.24 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 1 | 0 | 0.00 | 0.09 | 36.98 | 36.98 | 37.00 | 37.00 |
| /tasks/stats | 2 | 0 | 0.00 | 0.19 | 17.53 | 21.96 | 22.00 | 22.00 |
| /tasks/{id} | 1 | 0 | 0.00 | 0.09 | 13.24 | 13.24 | 13.00 | 13.00 |
| /tasks/{id}/comments | 1 | 0 | 0.00 | 0.09 | 12.60 | 12.60 | 13.00 | 13.00 |
| /tasks?limit=200 | 11 | 0 | 0.00 | 1.02 | 13.44 | 13.00 | 17.00 | 17.00 |
| /tasks?limit=50 | 7 | 0 | 0.00 | 0.65 | 13.91 | 13.00 | 18.00 | 18.00 |
| /tasks?priority=<value> | 1 | 0 | 0.00 | 0.09 | 15.98 | 15.98 | 16.00 | 16.00 |
| /tasks?q=<term> | 5 | 0 | 0.00 | 0.47 | 14.08 | 14.00 | 18.00 | 18.00 |
| /tasks?status=&priority= | 3 | 0 | 0.00 | 0.28 | 13.30 | 14.00 | 18.00 | 18.00 |
| /tasks?status=<value> | 2 | 0 | 0.00 | 0.19 | 17.29 | 17.63 | 18.00 | 18.00 |
