# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\smoke\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | smoke |
| timestamp_utc | 2026-10-03T08:18:18+00:00 |
| dataset_tasks | 200 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 29 |
| users | 3 |
| spawn_rate | 3.0 |
| run_time | 8s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:64258 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 3 -r 3.0 -t 8s --host http://127.0.0.1:64258 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\smoke\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\smoke\locust_report.html --only-summary --loglevel WARNING |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_acq5sm98/week4_perf_tasks.db |
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
| request_count | 64.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 9.62 |
| average_ms | 12.69 |
| median_ms | 10.00 |
| p95_ms | 26.00 |
| p99_ms | 52.00 |
| min_ms | 5.29 |
| max_ms | 51.92 |
| average_content_size | 16371.33 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 3 | 0 | 0.00 | 0.45 | 44.97 | 46.00 | 52.00 | 52.00 |
| /tasks/stats | 2 | 0 | 0.00 | 0.30 | 11.91 | 13.76 | 14.00 | 14.00 |
| /tasks/{id} | 3 | 0 | 0.00 | 0.45 | 9.17 | 10.00 | 11.00 | 11.00 |
| /tasks/{id}/comments | 5 | 0 | 0.00 | 0.75 | 7.63 | 7.00 | 11.00 | 11.00 |
| /tasks?limit=200 | 12 | 0 | 0.00 | 1.80 | 15.74 | 14.00 | 26.00 | 26.00 |
| /tasks?limit=50 | 19 | 0 | 0.00 | 2.86 | 10.03 | 9.00 | 19.00 | 19.00 |
| /tasks?priority=<value> | 6 | 0 | 0.00 | 0.90 | 9.28 | 10.00 | 11.00 | 11.00 |
| /tasks?q=<term> | 8 | 0 | 0.00 | 1.20 | 10.99 | 10.00 | 21.00 | 21.00 |
| /tasks?status=&priority= | 1 | 0 | 0.00 | 0.15 | 16.33 | 16.33 | 16.00 | 16.00 |
| /tasks?status=<value> | 5 | 0 | 0.00 | 0.75 | 9.63 | 9.00 | 12.00 | 12.00 |
