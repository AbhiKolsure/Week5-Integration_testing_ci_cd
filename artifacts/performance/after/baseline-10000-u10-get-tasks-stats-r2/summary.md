# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-10000-u10-get-tasks-stats-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-10000-u10-get-tasks-stats-r2 |
| timestamp_utc | 2026-10-07T08:20:44+00:00 |
| dataset_tasks | 10000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 1429 |
| users | 10 |
| spawn_rate | 2.0 |
| run_time | 20s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:62155 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 20s --host http://127.0.0.1:62155 --csv artifacts\performance\after\baseline-10000-u10-get-tasks-stats-r2\locust --html artifacts\performance\after\baseline-10000-u10-get-tasks-stats-r2\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 28.56 |
| api_max_cpu_percent | 51.5 |
| api_mean_rss_mb | 93.95 |
| api_max_rss_mb | 95.55 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_fexg2u_6/week4_perf_tasks.db |
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
| request_count | 528.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 27.65 |
| average_ms | 12.49 |
| median_ms | 11.00 |
| p95_ms | 22.00 |
| p99_ms | 28.00 |
| min_ms | 6.23 |
| max_ms | 31.59 |
| average_content_size | 357.77 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.52 | 8.89 | 8.00 | 13.00 | 13.00 |
| /tasks/stats | 518 | 0 | 0.00 | 27.12 | 12.56 | 11.00 | 22.00 | 28.00 |
