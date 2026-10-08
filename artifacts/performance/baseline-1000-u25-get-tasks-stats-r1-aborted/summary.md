# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u25-get-tasks-stats-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u25-get-tasks-stats-r1 |
| timestamp_utc | 2026-10-03T09:09:39+00:00 |
| dataset_tasks | 1000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 143 |
| users | 25 |
| spawn_rate | 5.0 |
| run_time | 30s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:63785 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 30s --host http://127.0.0.1:63785 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u25-get-tasks-stats-r1\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u25-get-tasks-stats-r1\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 61 |
| api_mean_cpu_percent | 46.01 |
| api_max_cpu_percent | 80.7 |
| api_mean_rss_mb | 87.1 |
| api_max_rss_mb | 87.85 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_z0_w806o/week4_perf_tasks.db |
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
| request_count | 2145.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 74.19 |
| average_ms | 12.60 |
| median_ms | 11.00 |
| p95_ms | 25.00 |
| p99_ms | 36.00 |
| min_ms | 4.35 |
| max_ms | 74.63 |
| average_content_size | 303.51 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 0.86 | 32.33 | 32.00 | 49.00 | 61.00 |
| /tasks/stats | 2120 | 0 | 0.00 | 73.32 | 12.37 | 11.00 | 24.00 | 33.00 |
