# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-1000-u25-get-tasks-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u25-get-tasks-r2 |
| timestamp_utc | 2026-10-07T08:18:32+00:00 |
| dataset_tasks | 1000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 143 |
| users | 25 |
| spawn_rate | 5.0 |
| run_time | 20s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:62875 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 20s --host http://127.0.0.1:62875 --csv artifacts\performance\after\baseline-1000-u25-get-tasks-r2\locust --html artifacts\performance\after\baseline-1000-u25-get-tasks-r2\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 37.99 |
| api_max_cpu_percent | 73.0 |
| api_mean_rss_mb | 87.64 |
| api_max_rss_mb | 88.46 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_eysksetu/week4_perf_tasks.db |
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
| request_count | 1373.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 72.00 |
| average_ms | 10.03 |
| median_ms | 8.00 |
| p95_ms | 24.00 |
| p99_ms | 39.00 |
| min_ms | 3.13 |
| max_ms | 50.51 |
| average_content_size | 12233.07 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 1.31 | 25.99 | 27.00 | 37.00 | 39.00 |
| /tasks?limit=50 | 1348 | 0 | 0.00 | 70.69 | 9.74 | 8.00 | 22.00 | 38.00 |
