# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\ts-check\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | ts-check |
| timestamp_utc | 2026-10-03T08:28:40+00:00 |
| dataset_tasks | 200 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 29 |
| users | 4 |
| spawn_rate | 4.0 |
| run_time | 6s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:51904 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 4 -r 4.0 -t 6s --host http://127.0.0.1:51904 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\ts-check\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\ts-check\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 13 |
| api_mean_cpu_percent | 6.65 |
| api_max_cpu_percent | 15.5 |
| api_mean_rss_mb | 81.4 |
| api_max_rss_mb | 81.82 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_niibq8d1/week4_perf_tasks.db |
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
| request_count | 65.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 13.09 |
| average_ms | 11.34 |
| median_ms | 9.00 |
| p95_ms | 32.00 |
| p99_ms | 50.00 |
| min_ms | 4.34 |
| max_ms | 49.70 |
| average_content_size | 11965.72 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 4 | 0 | 0.00 | 0.81 | 39.13 | 39.00 | 50.00 | 50.00 |
| /tasks?limit=50 | 61 | 0 | 0.00 | 12.28 | 9.52 | 8.00 | 18.00 | 23.00 |
