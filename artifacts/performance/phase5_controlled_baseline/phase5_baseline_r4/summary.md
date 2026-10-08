# Load test summary

*Source CSV:* `artifacts\performance\phase5_controlled_baseline\phase5_baseline_r4\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | phase5_baseline_r4 |
| timestamp_utc | 2026-10-07T07:49:39+00:00 |
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
| host | http://127.0.0.1:60536 |
| tags | (all scenarios) |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 30s --host http://127.0.0.1:60536 --csv artifacts\performance\phase5_controlled_baseline\phase5_baseline_r4\locust --html artifacts\performance\phase5_controlled_baseline\phase5_baseline_r4\locust_report.html --only-summary --loglevel WARNING |
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
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_3t92_wf9/week4_perf_tasks.db |
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
| request_count | 873.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 29.92 |
| average_ms | 12.16 |
| median_ms | 10.00 |
| p95_ms | 26.00 |
| p99_ms | 36.00 |
| min_ms | 2.87 |
| max_ms | 47.67 |
| average_content_size | 14929.95 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.34 | 14.61 | 15.00 | 19.00 | 19.00 |
| /tasks/stats | 35 | 0 | 0.00 | 1.20 | 15.73 | 15.00 | 26.00 | 27.00 |
| /tasks/{id} | 76 | 0 | 0.00 | 2.61 | 6.84 | 7.00 | 13.00 | 18.00 |
| /tasks/{id}/comments | 49 | 0 | 0.00 | 1.68 | 5.94 | 5.00 | 11.00 | 13.00 |
| /tasks?limit=200 | 114 | 0 | 0.00 | 3.91 | 16.59 | 14.00 | 32.00 | 40.00 |
| /tasks?limit=50 | 210 | 0 | 0.00 | 7.20 | 10.44 | 10.00 | 20.00 | 32.00 |
| /tasks?priority=<value> | 84 | 0 | 0.00 | 2.88 | 10.79 | 10.00 | 22.00 | 36.00 |
| /tasks?q=<term> | 99 | 0 | 0.00 | 3.39 | 18.36 | 17.00 | 33.00 | 48.00 |
| /tasks?status=&priority= | 81 | 0 | 0.00 | 2.78 | 11.91 | 11.00 | 20.00 | 32.00 |
| /tasks?status=<value> | 115 | 0 | 0.00 | 3.94 | 11.61 | 11.00 | 23.00 | 28.00 |
