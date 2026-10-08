# Load test summary

*Source CSV:* `C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-recorded\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | week5-auth-smoke-recorded |
| timestamp_utc | 2026-10-08T05:00:55+00:00 |
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
| host | http://127.0.0.1:52649 |
| tags | (all scenarios) |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 1 -r 1.0 -t 12s --host http://127.0.0.1:52649 --csv C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-recorded\locust --html C:\Week5_Integration_testing_ci_cd\Week5_Integration_testing_ci_cd\week4_performance_load_testing\artifacts\performance\week5-auth-smoke-recorded\locust_report.html --only-summary --loglevel WARNING |
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
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_q10o2ykq/week4_perf_tasks.db |
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
| request_count | 37.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 3.40 |
| average_ms | 15.39 |
| median_ms | 14.00 |
| p95_ms | 30.00 |
| p99_ms | 66.00 |
| min_ms | 7.49 |
| max_ms | 65.65 |
| average_content_size | 2310.70 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 1 | 0 | 0.00 | 0.09 | 65.65 | 65.65 | 66.00 | 66.00 |
| /tasks/stats | 2 | 0 | 0.00 | 0.18 | 18.45 | 25.84 | 26.00 | 26.00 |
| /tasks/{id} | 2 | 0 | 0.00 | 0.18 | 9.33 | 11.00 | 11.00 | 11.00 |
| /tasks/{id}/comments | 2 | 0 | 0.00 | 0.18 | 11.90 | 14.00 | 14.00 | 14.00 |
| /tasks?limit=200 | 4 | 0 | 0.00 | 0.37 | 13.74 | 13.00 | 16.00 | 16.00 |
| /tasks?limit=50 | 8 | 0 | 0.00 | 0.73 | 13.92 | 15.00 | 16.00 | 16.00 |
| /tasks?priority=<value> | 1 | 0 | 0.00 | 0.09 | 12.64 | 12.64 | 13.00 | 13.00 |
| /tasks?q=<term> | 8 | 0 | 0.00 | 0.73 | 14.00 | 13.00 | 30.00 | 30.00 |
| /tasks?status=&priority= | 3 | 0 | 0.00 | 0.28 | 16.91 | 16.00 | 20.00 | 20.00 |
| /tasks?status=<value> | 6 | 0 | 0.00 | 0.55 | 13.77 | 15.00 | 16.00 | 16.00 |
