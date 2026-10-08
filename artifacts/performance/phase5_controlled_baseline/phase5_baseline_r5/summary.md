# Load test summary

*Source CSV:* `artifacts\performance\phase5_controlled_baseline\phase5_baseline_r5\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | phase5_baseline_r5 |
| timestamp_utc | 2026-10-07T07:49:58+00:00 |
| dataset_tasks | 10000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 1429 |
| users | 10 |
| spawn_rate | 2.0 |
| run_time | 30s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:53776 |
| tags | (all scenarios) |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 30s --host http://127.0.0.1:53776 --csv artifacts\performance\phase5_controlled_baseline\phase5_baseline_r5\locust --html artifacts\performance\phase5_controlled_baseline\phase5_baseline_r5\locust_report.html --only-summary --loglevel WARNING |
| api_cpu_samples | None |
| api_mean_cpu_percent | None |
| api_max_cpu_percent | None |
| api_mean_rss_mb | None |
| api_max_rss_mb | None |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_9jxitdyz/week4_perf_tasks.db |
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
| request_count | 851.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 29.12 |
| average_ms | 14.59 |
| median_ms | 12.00 |
| p95_ms | 32.00 |
| p99_ms | 48.00 |
| min_ms | 3.26 |
| max_ms | 77.34 |
| average_content_size | 15767.35 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.34 | 18.43 | 16.00 | 34.00 | 34.00 |
| /tasks/stats | 41 | 0 | 0.00 | 1.40 | 15.95 | 16.00 | 25.00 | 34.00 |
| /tasks/{id} | 62 | 0 | 0.00 | 2.12 | 7.47 | 7.00 | 15.00 | 21.00 |
| /tasks/{id}/comments | 35 | 0 | 0.00 | 1.20 | 7.81 | 7.00 | 17.00 | 18.00 |
| /tasks?limit=200 | 124 | 0 | 0.00 | 4.24 | 19.25 | 18.00 | 36.00 | 48.00 |
| /tasks?limit=50 | 188 | 0 | 0.00 | 6.43 | 11.87 | 11.00 | 22.00 | 31.00 |
| /tasks?priority=<value> | 84 | 0 | 0.00 | 2.87 | 12.19 | 11.00 | 22.00 | 30.00 |
| /tasks?q=<term> | 127 | 0 | 0.00 | 4.35 | 22.97 | 19.00 | 48.00 | 60.00 |
| /tasks?status=&priority= | 73 | 0 | 0.00 | 2.50 | 14.08 | 13.00 | 30.00 | 34.00 |
| /tasks?status=<value> | 107 | 0 | 0.00 | 3.66 | 11.73 | 10.00 | 21.00 | 26.00 |
