# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-10000-u25-get-tasks-stats-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-10000-u25-get-tasks-stats-r1 |
| timestamp_utc | 2026-10-07T08:22:04+00:00 |
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
| host | http://127.0.0.1:59149 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 20s --host http://127.0.0.1:59149 --csv artifacts\performance\after\baseline-10000-u25-get-tasks-stats-r1\locust --html artifacts\performance\after\baseline-10000-u25-get-tasks-stats-r1\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 81.86 |
| api_max_cpu_percent | 139.6 |
| api_mean_rss_mb | 101.82 |
| api_max_rss_mb | 106.53 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_1hdq6g6r/week4_perf_tasks.db |
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
| request_count | 1372.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 71.71 |
| average_ms | 16.86 |
| median_ms | 14.00 |
| p95_ms | 36.00 |
| p99_ms | 51.00 |
| min_ms | 7.34 |
| max_ms | 64.23 |
| average_content_size | 353.49 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 1.31 | 23.15 | 23.00 | 29.00 | 34.00 |
| /tasks/stats | 1347 | 0 | 0.00 | 70.40 | 16.74 | 13.00 | 36.00 | 51.00 |
