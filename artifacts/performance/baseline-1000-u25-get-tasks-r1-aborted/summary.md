# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u25-get-tasks-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u25-get-tasks-r1 |
| timestamp_utc | 2026-10-03T09:08:23+00:00 |
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
| host | http://127.0.0.1:64791 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 30s --host http://127.0.0.1:64791 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u25-get-tasks-r1\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u25-get-tasks-r1\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 61 |
| api_mean_cpu_percent | 38.75 |
| api_max_cpu_percent | 79.2 |
| api_mean_rss_mb | 86.81 |
| api_max_rss_mb | 88.51 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_bv5m_9k3/week4_perf_tasks.db |
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
| request_count | 1514.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 53.36 |
| average_ms | 130.02 |
| median_ms | 13.00 |
| p95_ms | 660.00 |
| p99_ms | 820.00 |
| min_ms | 4.23 |
| max_ms | 1041.85 |
| average_content_size | 12243.50 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 0.88 | 505.34 | 640.00 | 710.00 | 770.00 |
| /tasks?limit=50 | 1489 | 0 | 0.00 | 52.48 | 123.72 | 13.00 | 650.00 | 820.00 |
