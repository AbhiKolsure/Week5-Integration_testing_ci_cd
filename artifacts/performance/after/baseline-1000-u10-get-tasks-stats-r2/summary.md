# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-1000-u10-get-tasks-stats-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u10-get-tasks-stats-r2 |
| timestamp_utc | 2026-10-07T08:15:21+00:00 |
| dataset_tasks | 1000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 143 |
| users | 10 |
| spawn_rate | 2.0 |
| run_time | 20s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:60839 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 20s --host http://127.0.0.1:60839 --csv artifacts\performance\after\baseline-1000-u10-get-tasks-stats-r2\locust --html artifacts\performance\after\baseline-1000-u10-get-tasks-stats-r2\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 12.42 |
| api_max_cpu_percent | 45.6 |
| api_mean_rss_mb | 84.8 |
| api_max_rss_mb | 85.11 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_36mgggpx/week4_perf_tasks.db |
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
| request_count | 562.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 29.44 |
| average_ms | 8.18 |
| median_ms | 7.00 |
| p95_ms | 17.00 |
| p99_ms | 24.00 |
| min_ms | 3.33 |
| max_ms | 34.20 |
| average_content_size | 340.12 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.52 | 13.28 | 13.00 | 18.00 | 18.00 |
| /tasks/stats | 552 | 0 | 0.00 | 28.92 | 8.09 | 7.00 | 17.00 | 24.00 |
