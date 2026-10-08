# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-1000-u25-get-tasks-stats-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u25-get-tasks-stats-r1 |
| timestamp_utc | 2026-10-07T08:18:59+00:00 |
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
| host | http://127.0.0.1:62557 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 20s --host http://127.0.0.1:62557 --csv artifacts\performance\after\baseline-1000-u25-get-tasks-stats-r1\locust --html artifacts\performance\after\baseline-1000-u25-get-tasks-stats-r1\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 37.67 |
| api_max_cpu_percent | 71.5 |
| api_mean_rss_mb | 88.34 |
| api_max_rss_mb | 89.01 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_5_x_w2gi/week4_perf_tasks.db |
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
| request_count | 1413.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 73.96 |
| average_ms | 8.85 |
| median_ms | 7.00 |
| p95_ms | 22.00 |
| p99_ms | 35.00 |
| min_ms | 3.04 |
| max_ms | 55.62 |
| average_content_size | 339.52 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 1.31 | 25.32 | 23.00 | 38.00 | 39.00 |
| /tasks/stats | 1388 | 0 | 0.00 | 72.65 | 8.55 | 7.00 | 20.00 | 34.00 |
