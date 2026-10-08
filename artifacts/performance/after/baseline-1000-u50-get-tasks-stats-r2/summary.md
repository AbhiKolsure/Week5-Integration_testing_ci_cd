# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-1000-u50-get-tasks-stats-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u50-get-tasks-stats-r2 |
| timestamp_utc | 2026-10-07T08:21:13+00:00 |
| dataset_tasks | 1000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 143 |
| users | 50 |
| spawn_rate | 10.0 |
| run_time | 20s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:62233 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f benchmarks\locustfile.py --headless -u 50 -r 10.0 -t 20s --host http://127.0.0.1:62233 --csv artifacts\performance\after\baseline-1000-u50-get-tasks-stats-r2\locust --html artifacts\performance\after\baseline-1000-u50-get-tasks-stats-r2\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 62.36 |
| api_max_cpu_percent | 114.6 |
| api_mean_rss_mb | 91.48 |
| api_max_rss_mb | 93.53 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_8b0m2dai/week4_perf_tasks.db |
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
| request_count | 2762.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 144.73 |
| average_ms | 14.21 |
| median_ms | 9.00 |
| p95_ms | 44.00 |
| p99_ms | 74.00 |
| min_ms | 2.87 |
| max_ms | 101.72 |
| average_content_size | 341.97 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 50 | 0 | 0.00 | 2.62 | 64.44 | 68.00 | 88.00 | 95.00 |
| /tasks/stats | 2712 | 0 | 0.00 | 142.11 | 13.29 | 9.00 | 39.00 | 66.00 |
