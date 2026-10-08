# Load test summary

*Source CSV:* `artifacts\performance\after\baseline-1000-u50-get-tasks-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u50-get-tasks-r2 |
| timestamp_utc | 2026-10-07T08:20:20+00:00 |
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
| host | http://127.0.0.1:63823 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f benchmarks\locustfile.py --headless -u 50 -r 10.0 -t 20s --host http://127.0.0.1:63823 --csv artifacts\performance\after\baseline-1000-u50-get-tasks-r2\locust --html artifacts\performance\after\baseline-1000-u50-get-tasks-r2\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 40 |
| api_mean_cpu_percent | 96.92 |
| api_max_cpu_percent | 215.9 |
| api_mean_rss_mb | 91.86 |
| api_max_rss_mb | 93.78 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_bz6dag2v/week4_perf_tasks.db |
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
| request_count | 2577.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 135.31 |
| average_ms | 35.50 |
| median_ms | 18.00 |
| p95_ms | 120.00 |
| p99_ms | 160.00 |
| min_ms | 3.18 |
| max_ms | 219.85 |
| average_content_size | 12225.73 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 50 | 0 | 0.00 | 2.63 | 55.03 | 54.00 | 82.00 | 90.00 |
| /tasks?limit=50 | 2527 | 0 | 0.00 | 132.69 | 35.11 | 18.00 | 120.00 | 160.00 |
