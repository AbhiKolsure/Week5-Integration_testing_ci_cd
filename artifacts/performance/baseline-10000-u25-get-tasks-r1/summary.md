# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u25-get-tasks-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-10000-u25-get-tasks-r1 |
| timestamp_utc | 2026-10-03T09:18:52+00:00 |
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
| host | http://127.0.0.1:52658 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 20s --host http://127.0.0.1:52658 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u25-get-tasks-r1\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u25-get-tasks-r1\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 42 |
| api_mean_cpu_percent | 53.05 |
| api_max_cpu_percent | 99.0 |
| api_mean_rss_mb | 86.94 |
| api_max_rss_mb | 87.91 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_zca83fj7/week4_perf_tasks.db |
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
| request_count | 1345.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 70.59 |
| average_ms | 21.36 |
| median_ms | 16.00 |
| p95_ms | 53.00 |
| p99_ms | 85.00 |
| min_ms | 4.75 |
| max_ms | 147.14 |
| average_content_size | 12231.74 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 1.31 | 45.05 | 40.00 | 70.00 | 85.00 |
| /tasks?limit=50 | 1320 | 0 | 0.00 | 69.27 | 20.91 | 16.00 | 52.00 | 83.00 |
