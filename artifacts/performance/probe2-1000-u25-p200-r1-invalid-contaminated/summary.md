# Load test summary

*Source CSV:* `C:\Performance Testing\week4_performance_load_testing\artifacts\performance\probe2-1000-u25-p200-r1\locust_stats.csv`

## Environment and dataset

| Item | Value |
| --- | --- |
| run_label | probe2-1000-u25-p200-r1 |
| timestamp_utc | 2026-10-03T09:46:24+00:00 |
| dataset_tasks | 1000 |
| dataset_comments_per_task | 1 |
| dataset_search_matches | 143 |
| users | 25 |
| spawn_rate | 5.0 |
| run_time | 20s |
| page_size | 200 |
| full_page_size | 200 |
| search_term | burndown |
| filter_status | pending |
| filter_priority | high |
| host | http://127.0.0.1:53933 |
| tags | list50 |
| locust_command | C:\Program Files\Python314\python.exe -m locust -f C:\Performance Testing\week4_performance_load_testing\benchmarks\locustfile.py --headless -u 25 -r 5.0 -t 20s --host http://127.0.0.1:53933 --csv C:\Performance Testing\week4_performance_load_testing\artifacts\performance\probe2-1000-u25-p200-r1\locust --html C:\Performance Testing\week4_performance_load_testing\artifacts\performance\probe2-1000-u25-p200-r1\locust_report.html --only-summary --loglevel WARNING --tags list50 |
| api_cpu_samples | 56 |
| api_mean_cpu_percent | 10.39 |
| api_max_cpu_percent | 29.5 |
| api_mean_rss_mb | 89.11 |
| api_max_rss_mb | 92.32 |
| python | 3.14.3 |
| platform | Windows-11-10.0.26300-SP0 |
| machine | AMD64 |
| processor_count | 12 |
| database_type | SQLite (file) |
| database_url | sqlite:///C:/Users/kolsu/AppData/Local/Temp/week4_load_qxxhsbfe/week4_perf_tasks.db |
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
| request_count | 129.00 |
| failure_count | 0.00 |
| failure_rate | 0.00 |
| requests_per_second | 5.55 |
| average_ms | 3802.18 |
| median_ms | 3900.00 |
| p95_ms | 6600.00 |
| p99_ms | 7300.00 |
| min_ms | 863.42 |
| max_ms | 10727.74 |
| average_content_size | 40977.53 |

## Per endpoint

| Endpoint | Requests | Failures | Failure rate | RPS | Avg ms | Median ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /tasks [bootstrap] | 25 | 0 | 0.00 | 1.08 | 2451.03 | 1600.00 | 5000.00 | 5000.00 |
| /tasks?limit=50 | 104 | 0 | 0.00 | 4.48 | 4126.97 | 4100.00 | 6700.00 | 7300.00 |
