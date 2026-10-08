# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u50-get-tasks-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-10000-u50-get-tasks-r1 |
| timestamp_utc | 2026-10-03T09:21:08+00:00 |
| dataset_tasks | 10000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 1429 |
| users | 50 |
| spawn_rate | 10.0 |
| run_time | 20s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:65290 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 50 -r 10.0 -t 20s --host http://127.0.0.1:65290 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u50-get-tasks-r1\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-10000-u50-get-tasks-r1\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 44 |
| api_mean_cpu_percent | 130.27 |
| api_max_cpu_percent | 215.8 |
| api_mean_rss_mb | 90.68 |
| api_max_rss_mb | 93.49 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_bbhycqjs/week4_perf_tasks.db |
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
| request_count | 2006.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 111.03 |
| average_ms | 105.24 |
| median_ms | 99.00 |
| p95_ms | 230.00 |
| p99_ms | 330.00 |
| min_ms | 5.37 |
| max_ms | 492.93 |
| average_content_size | 12192.78 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 50 | 0 | 0.00 | 2.77 | 83.99 | 80.00 | 120.00 | 130.00 |
| /tasks?limit=50 | 1956 | 0 | 0.00 | 108.27 | 105.78 | 100.00 | 230.00 | 330.00 |
