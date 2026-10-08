# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-10000-u25-get-tasks-stats-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-10000-u25-get-tasks-stats-r2 |
| timestamp_utc | 2026-10-07T08:22:32+00:00 |
| dataset_tasks | 10000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 1429 |
| users | 25 |
| spawn_rate | 5.0 |
| run_time | 20s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:58426 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 20s --host http://127.0.0.1:58426 --csv artifacts\performance\after\baseline-10000-u25-get-tasks-stats-r2\locust --html artifacts\performance\after\baseline-10000-u25-get-tasks-stats-r2\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 71.73 |
| api_max_cpu_percent | 139.7 |
| api_mean_rss_mb | 101.29 |
| api_max_rss_mb | 105.54 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_jd0p7yb5/week4_perf_tasks.db |
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
| request_count | 1351.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 70.67 |
| average_ms | 16.77 |
| median_ms | 14.00 |
| p95_ms | 37.00 |
| p99_ms | 48.00 |
| min_ms | 7.13 |
| max_ms | 78.50 |
| average_content_size | 355.18 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 1.31 | 24.99 | 24.00 | 34.00 | 43.00 |
| /tasks/stats | 1326 | 0 | 0.00 | 69.36 | 16.62 | 14.00 | 37.00 | 48.00 |
