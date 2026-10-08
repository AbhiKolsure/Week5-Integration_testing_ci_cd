# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-10000-u50-get-tasks-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-10000-u50-get-tasks-r2 |
| timestamp_utc | 2026-10-07T08:23:26+00:00 |
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
| host | http://127.0.0.1:56050 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 50 -r 10.0 -t 20s --host http://127.0.0.1:56050 --csv artifacts\performance\after\baseline-10000-u50-get-tasks-r2\locust --html artifacts\performance\after\baseline-10000-u50-get-tasks-r2\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 83.47 |
| api_max_cpu_percent | 164.8 |
| api_mean_rss_mb | 91.77 |
| api_max_rss_mb | 93.16 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_7fr428zj/week4_perf_tasks.db |
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
| request_count | 2667.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 139.74 |
| average_ms | 23.89 |
| median_ms | 18.00 |
| p95_ms | 65.00 |
| p99_ms | 92.00 |
| min_ms | 3.22 |
| max_ms | 129.32 |
| average_content_size | 12230.76 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 50 | 0 | 0.00 | 2.62 | 45.38 | 47.00 | 62.00 | 78.00 |
| /tasks?limit=50 | 2617 | 0 | 0.00 | 137.12 | 23.48 | 18.00 | 65.00 | 92.00 |
