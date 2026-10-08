# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\phase5-loader-smoke\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | phase5-loader-smoke |
| timestamp_utc | 2026-10-06T10:46:58+00:00 |
| dataset_tasks | 200 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 29 |
| users | 2 |
| spawn_rate | 2.0 |
| run_time | 8s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:52962 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 2 -r 2.0 -t 8s --host http://127.0.0.1:52962 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\phase5-loader-smoke\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\phase5-loader-smoke\locust_report.html --only-summary --loglevel WARNING --tags stats |
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
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_8pu2k4oc/week4_perf_tasks.db |
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
| request_count | 46.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 6.63 |
| average_ms | 14.72 |
| median_ms | 12.00 |
| p95_ms | 31.00 |
| p99_ms | 40.00 |
| min_ms | 8.36 |
| max_ms | 39.63 |
| average_content_size | 483.70 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 2 | 0 | 0.00 | 0.29 | 27.93 | 30.00 | 30.00 | 30.00 |
| /tasks/stats | 44 | 0 | 0.00 | 6.34 | 14.12 | 12.00 | 31.00 | 40.00 |
