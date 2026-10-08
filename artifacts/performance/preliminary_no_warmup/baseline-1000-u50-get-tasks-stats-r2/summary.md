# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u50-get-tasks-stats-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u50-get-tasks-stats-r2 |
| timestamp_utc | 2026-10-03T08:49:19+00:00 |
| dataset_tasks | 1000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 143 |
| users | 50 |
| spawn_rate | 10.0 |
| run_time | 20s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:53951 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 50 -r 10.0 -t 20s --host http://127.0.0.1:53951 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u50-get-tasks-stats-r2\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u50-get-tasks-stats-r2\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 41 |
| api_mean_cpu_percent | 74.1 |
| api_max_cpu_percent | 118.5 |
| api_mean_rss_mb | 89.24 |
| api_max_rss_mb | 90.76 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_akt3le9s/week4_perf_tasks.db |
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
| request_count | 2750.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 144.26 |
| average_ms | 15.87 |
| median_ms | 14.00 |
| p95_ms | 34.00 |
| p99_ms | 60.00 |
| min_ms | 3.69 |
| max_ms | 104.97 |
| average_content_size | 342.44 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 50 | 0 | 0.00 | 2.62 | 61.07 | 62.00 | 92.00 | 100.00 |
| /tasks/stats | 2700 | 0 | 0.00 | 141.63 | 15.03 | 14.00 | 31.00 | 42.00 |
