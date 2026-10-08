# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\probe-1000-u25-p200-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | probe-1000-u25-p200-r1 |
| timestamp_utc | 2026-10-03T09:42:04+00:00 |
| dataset_tasks | 1000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 143 |
| users | 25 |
| spawn_rate | 2.0 |
| run_time | 20s |
| page_size | 200 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:54061 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 25 -r 2.0 -t 20s --host http://127.0.0.1:54061 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\probe-1000-u25-p200-r1\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\probe-1000-u25-p200-r1\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 45 |
| api_mean_cpu_percent | 49.23 |
| api_max_cpu_percent | 94.7 |
| api_mean_rss_mb | 88.31 |
| api_max_rss_mb | 93.03 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_oo33yz8r/week4_perf_tasks.db |
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
| request_count | 504.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 24.75 |
| average_ms | 429.08 |
| median_ms | 400.00 |
| p95_ms | 990.00 |
| p99_ms | 1800.00 |
| min_ms | 23.54 |
| max_ms | 1906.21 |
| average_content_size | 47198.12 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 1.23 | 168.29 | 110.00 | 540.00 | 550.00 |
| /tasks?limit=50 | 479 | 0 | 0.00 | 23.52 | 442.69 | 410.00 | 1000.00 | 1800.00 |
