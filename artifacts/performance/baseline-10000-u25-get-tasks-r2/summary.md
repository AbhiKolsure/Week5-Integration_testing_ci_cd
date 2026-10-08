# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u25-get-tasks-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-10000-u25-get-tasks-r2 |
| timestamp_utc | 2026-10-03T09:19:25+00:00 |
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
| host | http://127.0.0.1:60263 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 20s --host http://127.0.0.1:60263 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u25-get-tasks-r2\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u25-get-tasks-r2\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 51 |
| api_mean_cpu_percent | 41.64 |
| api_max_cpu_percent | 115.2 |
| api_mean_rss_mb | 87.09 |
| api_max_rss_mb | 88.52 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_q3nlh13c/week4_perf_tasks.db |
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
| request_count | 1367.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 60.82 |
| average_ms | 34.65 |
| median_ms | 14.00 |
| p95_ms | 49.00 |
| p99_ms | 100.00 |
| min_ms | 4.52 |
| max_ms | 3463.33 |
| average_content_size | 12233.58 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 1.11 | 27.13 | 27.00 | 38.00 | 40.00 |
| /tasks?limit=50 | 1342 | 0 | 0.00 | 59.71 | 34.79 | 14.00 | 49.00 | 100.00 |
