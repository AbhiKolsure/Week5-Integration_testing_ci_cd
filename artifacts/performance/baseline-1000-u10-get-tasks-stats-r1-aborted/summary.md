# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u10-get-tasks-stats-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u10-get-tasks-stats-r1 |
| timestamp_utc | 2026-10-03T09:06:53+00:00 |
| dataset_tasks | 1000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 143 |
| users | 10 |
| spawn_rate | 2.0 |
| run_time | 30s |
| page_size | 50 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:62760 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 30s --host http://127.0.0.1:62760 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u10-get-tasks-stats-r1\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u10-get-tasks-stats-r1\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 73 |
| api_mean_cpu_percent | 14.75 |
| api_max_cpu_percent | 52.8 |
| api_mean_rss_mb | 84.74 |
| api_max_rss_mb | 86.45 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_82vlnd_n/week4_perf_tasks.db |
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
| request_count | 783.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 23.40 |
| average_ms | 49.16 |
| median_ms | 9.00 |
| p95_ms | 260.00 |
| p99_ms | 480.00 |
| min_ms | 4.32 |
| max_ms | 4342.30 |
| average_content_size | 310.17 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.30 | 14.62 | 14.00 | 21.00 | 21.00 |
| /tasks/stats | 773 | 0 | 0.00 | 23.10 | 49.61 | 9.00 | 260.00 | 480.00 |
