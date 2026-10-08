# Load test summary

*Source CSV:* `artifacts\performance\phase5_controlled_baseline\phase5_baseline_r3\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | phase5_baseline_r3 |
| timestamp_utc | 2026-10-07T07:48:46+00:00 |
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
| host | http://127.0.0.1:50799 |
| tags | (all scenarios) |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 30s --host http://127.0.0.1:50799 --csv artifacts\performance\phase5_controlled_baseline\phase5_baseline_r3\locust --html artifacts\performance\phase5_controlled_baseline\phase5_baseline_r3\locust_report.html --only-summary --loglevel WARNING |
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
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_niu9we_1/week4_perf_tasks.db |
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
| request_count | 892.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 30.49 |
| average_ms | 13.16 |
| median_ms | 12.00 |
| p95_ms | 24.00 |
| p99_ms | 33.00 |
| min_ms | 2.74 |
| max_ms | 47.06 |
| average_content_size | 15222.38 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.34 | 17.46 | 19.00 | 21.00 | 21.00 |
| /tasks/stats | 40 | 0 | 0.00 | 1.37 | 19.44 | 19.00 | 35.00 | 36.00 |
| /tasks/{id} | 81 | 0 | 0.00 | 2.77 | 7.71 | 7.00 | 14.00 | 17.00 |
| /tasks/{id}/comments | 45 | 0 | 0.00 | 1.54 | 7.76 | 7.00 | 12.00 | 20.00 |
| /tasks?limit=200 | 124 | 0 | 0.00 | 4.24 | 16.76 | 16.00 | 31.00 | 46.00 |
| /tasks?limit=50 | 192 | 0 | 0.00 | 6.56 | 11.26 | 11.00 | 20.00 | 27.00 |
| /tasks?priority=<value> | 89 | 0 | 0.00 | 3.04 | 11.49 | 11.00 | 21.00 | 26.00 |
| /tasks?q=<term> | 119 | 0 | 0.00 | 4.07 | 18.99 | 19.00 | 28.00 | 33.00 |
| /tasks?status=&priority= | 78 | 0 | 0.00 | 2.67 | 12.67 | 13.00 | 21.00 | 24.00 |
| /tasks?status=<value> | 114 | 0 | 0.00 | 3.90 | 11.42 | 11.00 | 20.00 | 23.00 |
