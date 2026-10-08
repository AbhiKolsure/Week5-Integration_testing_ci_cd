# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u10-get-tasks-stats-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u10-get-tasks-stats-r2 |
| timestamp_utc | 2026-10-03T09:07:41+00:00 |
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
| host | http://127.0.0.1:58690 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 10 -r 2.0 -t 30s --host http://127.0.0.1:58690 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u10-get-tasks-stats-r2\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u10-get-tasks-stats-r2\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 70 |
| api_mean_cpu_percent | 18.7 |
| api_max_cpu_percent | 39.8 |
| api_mean_rss_mb | 83.74 |
| api_max_rss_mb | 84.75 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_h5dbkjt6/week4_perf_tasks.db |
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
| request_count | 656.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 22.64 |
| average_ms | 96.07 |
| median_ms | 71.00 |
| p95_ms | 240.00 |
| p99_ms | 480.00 |
| min_ms | 10.20 |
| max_ms | 618.31 |
| average_content_size | 324.91 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 10 | 0 | 0.00 | 0.35 | 81.37 | 83.00 | 170.00 | 170.00 |
| /tasks/stats | 646 | 0 | 0.00 | 22.30 | 96.29 | 71.00 | 240.00 | 480.00 |
