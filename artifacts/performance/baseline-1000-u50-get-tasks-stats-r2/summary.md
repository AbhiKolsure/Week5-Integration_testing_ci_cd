# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u50-get-tasks-stats-r2\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | baseline-1000-u50-get-tasks-stats-r2 |
| timestamp_utc | 2026-10-03T09:16:25+00:00 |
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
| host | http://127.0.0.1:58350 |
| tags | stats |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 50 -r 10.0 -t 20s --host http://127.0.0.1:58350 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u50-get-tasks-stats-r2\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\baseline-1000-u50-get-tasks-stats-r2\locust_report.html --only-summary --loglevel WARNING --tags stats |
| api_cpu_samples | 43 |
| api_mean_cpu_percent | 110.06 |
| api_max_cpu_percent | 174.0 |
| api_mean_rss_mb | 90.89 |
| api_max_rss_mb | 93.8 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_3a72mxvl/week4_perf_tasks.db |
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
| request_count | 2055.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 113.85 |
| average_ms | 96.39 |
| median_ms | 84.00 |
| p95_ms | 220.00 |
| p99_ms | 330.00 |
| min_ms | 5.62 |
| max_ms | 487.09 |
| average_content_size | 379.11 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 50 | 0 | 0.00 | 2.77 | 181.88 | 160.00 | 410.00 | 490.00 |
| /tasks/stats | 2005 | 0 | 0.00 | 111.08 | 94.25 | 83.00 | 220.00 | 320.00 |
