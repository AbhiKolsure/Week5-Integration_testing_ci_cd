"""Reproducible Locust load-test orchestrator.

One command seeds a deterministic dataset, starts ``uvicorn`` on a free port against a
throw-away SQLite database, drives the Locust scenarios headfully, then writes the raw
Locust CSV/HTML plus a JSON summary and a Markdown report into
``artifacts/performance/<label>/``.

Everything that makes a run reproducible is recorded: dataset size, users, spawn rate,
duration, request parameters, environment (Python/OS/package versions), database type
and the exact Locust command.

Examples::

    python scripts/performance/run_load_test.py --tasks 1000  --users 20 --run-time 30s
    python scripts/performance/run_load_test.py --tasks 10000 --users 50 --run-time 60s --label baseline-10000
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import secrets
import socket
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
_HERE = Path(__file__).resolve().parent
for _path in (str(PROJECT_ROOT), str(_HERE)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import httpx  # noqa: E402
from locust_summary import parse_stats_csv, render_markdown  # noqa: E402
from seed_dataset import (  # noqa: E402
    DEFAULT_COMMENTS_PER_TASK,
    DEFAULT_TASKS,
    SEARCH_TOKEN,
    expected_search_matches,
    seed_database,
)

DEFAULT_LOCUSTFILE = PROJECT_ROOT / "benchmarks" / "locustfile.py"
DEFAULT_OUT_DIR = PROJECT_ROOT / "artifacts" / "performance"
STARTUP_TIMEOUT_SECONDS = 60.0


def free_port() -> int:
    """Return a free TCP port on the loopback interface."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:  # pragma: no cover - defensive
        return "not installed"


def collect_environment(database_url: str) -> dict[str, object]:
    """Return the environment/configuration block recorded with every run."""
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor_count": os.cpu_count() or 0,
        "database_type": "SQLite (file)",
        "database_url": database_url,
        "fastapi": package_version("fastapi"),
        "starlette": package_version("starlette"),
        "pydantic": package_version("pydantic"),
        "sqlalchemy": package_version("sqlalchemy"),
        "uvicorn": package_version("uvicorn"),
        "locust": package_version("locust"),
        "gevent": package_version("gevent"),
    }


def wait_for_health(client: httpx.Client, base_url: str) -> dict[str, object] | None:
    deadline = time.time() + STARTUP_TIMEOUT_SECONDS
    while time.time() < deadline:
        try:
            response = client.get(f"{base_url}/health")
            if response.status_code == 200:
                return response.json()
        except httpx.HTTPError:
            time.sleep(0.25)
    return None


def build_locust_command(
    locustfile: Path,
    base_url: str,
    csv_prefix: Path,
    html_report: Path,
    users: int,
    spawn_rate: float,
    run_time: str,
    tags: str = "",
) -> list[str]:
    """Return the exact ``locust`` argv used for the run."""
    command = [
        sys.executable,
        "-m",
        "locust",
        "-f",
        str(locustfile),
        "--headless",
        "-u",
        str(users),
        "-r",
        str(spawn_rate),
        "-t",
        run_time,
        "--host",
        base_url,
        "--csv",
        str(csv_prefix),
        "--html",
        str(html_report),
        "--only-summary",
        "--loglevel",
        "WARNING",
    ]
    if tags:
        # Restrict the run to the scenarios carrying these @tag(...) labels, e.g.
        # "list50" for a single-endpoint baseline or "stats" for /tasks/stats only.
        command += ["--tags", tags]
    return command


class ProcessSampler:
    """Sample CPU and resident memory of the API process while the load test runs."""

    def __init__(self, pid: int, interval: float = 0.5) -> None:
        self.pid = pid
        self.interval = interval
        self.samples: list[tuple[float, float]] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._process = None

    def start(self) -> None:
        try:
            import psutil
        except ImportError:  # pragma: no cover - psutil ships with locust
            return
        try:
            self._process = psutil.Process(self.pid)
            self._process.cpu_percent(None)  # prime the counter
        except Exception:  # pragma: no cover - process already gone
            self._process = None
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.wait(self.interval):
            try:
                cpu = self._process.cpu_percent(None)
                rss_mb = self._process.memory_info().rss / (1024 * 1024)
            except Exception:  # pragma: no cover - process gone
                break
            self.samples.append((cpu, rss_mb))

    def stop(self) -> dict[str, object]:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5)
        if not self.samples:
            return {"available": False, "reason": "psutil unavailable or process exited"}
        cpu_values = [cpu for cpu, _ in self.samples]
        rss_values = [rss for _, rss in self.samples]
        return {
            "available": True,
            "sample_count": len(self.samples),
            "sample_interval_seconds": self.interval,
            "mean_cpu_percent": round(statistics.fmean(cpu_values), 2),
            "max_cpu_percent": round(max(cpu_values), 2),
            "mean_rss_mb": round(statistics.fmean(rss_values), 2),
            "max_rss_mb": round(max(rss_values), 2),
        }


@dataclass
class RunConfig:
    """Everything that defines exactly one measured load-test run."""

    tasks: int
    comments_per_task: int
    users: int
    spawn_rate: float
    run_time: str
    page_size: int
    full_page: int
    search_term: str
    filter_status: str
    filter_priority: str
    label: str = ""
    tags: str = ""
    out_dir: Path = DEFAULT_OUT_DIR
    locustfile: Path = DEFAULT_LOCUSTFILE
    database: str = ""
    keep_database: bool = False
    sample_process: bool = True
    warmup_seconds: float = 5.0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a reproducible Locust load test.")
    parser.add_argument("--tasks", type=int, default=DEFAULT_TASKS, help="seed dataset size (default: 1000)")
    parser.add_argument(
        "--comments-per-task",
        type=int,
        default=DEFAULT_COMMENTS_PER_TASK,
        help="comments per seeded task (default: 1)",
    )
    parser.add_argument("--users", type=int, default=10, help="concurrent Locust users (default: 10)")
    parser.add_argument("--spawn-rate", type=float, default=2.0, help="users spawned per second (default: 2)")
    parser.add_argument("--run-time", default="30s", help="Locust duration, e.g. 30s / 2m (default: 30s)")
    parser.add_argument("--page-size", type=int, default=50, help="default page size (default: 50)")
    parser.add_argument("--full-page", type=int, default=200, help="full page size (default: 200)")
    parser.add_argument("--search-term", default=SEARCH_TOKEN, help=f"search term (default: {SEARCH_TOKEN})")
    parser.add_argument("--filter-status", default="pending", help="status filter value (default: pending)")
    parser.add_argument("--filter-priority", default="high", help="priority filter value (default: high)")
    parser.add_argument("--label", default="", help="run label (default: dataset-<tasks>-users-<users>)")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="artifact root directory")
    parser.add_argument("--locustfile", default=str(DEFAULT_LOCUSTFILE), help="path to the Locust scenarios")
    parser.add_argument(
        "--tags",
        default="",
        help="comma separated @tag labels to run only (list50, list200, filters, search, detail, stats, primary)",
    )
    parser.add_argument("--database", default="", help="SQLite path to use (default: a temp file, removed afterwards)")
    parser.add_argument("--keep-database", action="store_true", help="keep the seeded database file")
    parser.add_argument(
        "--no-process-sampling",
        action="store_true",
        help="do not sample CPU/memory of the API process",
    )
    parser.add_argument(
        "--warmup",
        type=float,
        default=5.0,
        help="seconds of unmeasured warm-up requests before the measured run (default: 5)",
    )
    return parser.parse_args(argv)


def config_from_args(args: argparse.Namespace) -> RunConfig:
    """Translate parsed CLI arguments into a :class:`RunConfig`."""
    return RunConfig(
        tasks=args.tasks,
        comments_per_task=args.comments_per_task,
        users=args.users,
        spawn_rate=args.spawn_rate,
        run_time=args.run_time,
        page_size=args.page_size,
        full_page=args.full_page,
        search_term=args.search_term,
        filter_status=args.filter_status,
        filter_priority=args.filter_priority,
        label=args.label,
        tags=args.tags,
        out_dir=Path(args.out_dir),
        locustfile=Path(args.locustfile),
        database=args.database,
        keep_database=args.keep_database,
        sample_process=not args.no_process_sampling,
        warmup_seconds=args.warmup,
    )


def execute_run(args: RunConfig, *, verbose: bool = True) -> dict[str, object]:
    """Run one measured load test and return its summary, metadata and process metrics."""
    label = args.label or f"dataset-{args.tasks}-users-{args.users}"
    out_dir = Path(args.out_dir) / label
    out_dir.mkdir(parents=True, exist_ok=True)
    locustfile = Path(args.locustfile)

    work_dir = Path(tempfile.mkdtemp(prefix="week4_load_"))
    db_path = Path(args.database) if args.database else work_dir / "week4_perf_tasks.db"
    database_url = f"sqlite:///{db_path.as_posix()}"

    print("=" * 96)
    print("Week 4 reproducible Locust load test")
    print("=" * 96)
    print(f"label        : {label}")
    print(f"artifact dir : {out_dir}")
    print(f"dataset      : {args.tasks} tasks x {args.comments_per_task} comment(s)")
    print(f"seeding      : {database_url}")
    seeded = seed_database(db_path, args.tasks, args.comments_per_task, reset=True)
    print(f"seeded       : {seeded['tasks']} tasks, {seeded['comments']} comments")

    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    env = dict(os.environ)
    # Host App Control blocks gevent C extensions; force the verified pure-Python
    # fallback so the SAME Locust tool/scenarios run (measurement tool unchanged).
    env.setdefault("PURE_PYTHON", "1")
    env.setdefault("AUTH_SECRET_KEY", secrets.token_urlsafe(48))
    env.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
    env["DATABASE_URL"] = database_url
    env["LOAD_PAGE_SIZE"] = str(args.page_size)
    env["LOAD_FULL_PAGE"] = str(args.full_page)
    env["LOAD_SEARCH_TERM"] = args.search_term
    env["LOAD_FILTER_STATUS"] = args.filter_status
    env["LOAD_FILTER_PRIORITY"] = args.filter_priority

    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--log-level",
            "warning",
        ],
        cwd=PROJECT_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    exit_code = 0
    try:
        print(f"starting     : uvicorn app.main:app --port {port} (cwd={PROJECT_ROOT})")
        with httpx.Client(timeout=10.0) as client:
            health = wait_for_health(client, base_url)
        if health is None:
            print("ERROR: the API did not become healthy in time", file=sys.stderr)
            return {"label": label, "error": "the API did not become healthy in time", "exit_code": 1}
        print(f"health       : {health}")

        load_email = f"load-{secrets.token_hex(8)}@example.com"
        load_password = secrets.token_urlsafe(32)
        with httpx.Client(base_url=base_url, timeout=10.0) as auth_client:
            registration = auth_client.post(
                "/auth/register",
                json={"email": load_email, "password": load_password},
            )
            if registration.status_code != 201:
                raise RuntimeError(f"Load-test account registration failed: HTTP {registration.status_code}")
            login = auth_client.post(
                "/auth/login",
                json={"email": load_email, "password": load_password},
            )
            if login.status_code != 200:
                raise RuntimeError(f"Load-test account login failed: HTTP {login.status_code}")
            env["LOAD_AUTH_TOKEN"] = str(login.json()["access_token"])

        if args.warmup_seconds > 0:
            # A freshly created SQLite file and a cold uvicorn process produce very slow
            # first requests (page cache cold). Warm both before measuring, otherwise the
            # first run of a configuration is dominated by start-up noise.
            print(f"warm-up      : {args.warmup_seconds}s against the seeded database")
            warmup_requests = 0
            warmup_deadline = time.time() + args.warmup_seconds
            with httpx.Client(
                base_url=base_url,
                timeout=30.0,
                headers={"Authorization": f"Bearer {env['LOAD_AUTH_TOKEN']}"},
            ) as warm_client:
                while time.time() < warmup_deadline:
                    warm_client.get("/tasks", params={"limit": args.page_size})
                    warmup_requests += 1
            print(f"warm-up done : {warmup_requests} requests")

        csv_prefix = out_dir / "locust"
        html_report = out_dir / "locust_report.html"
        command = build_locust_command(
            locustfile,
            base_url,
            csv_prefix,
            html_report,
            args.users,
            args.spawn_rate,
            args.run_time,
            args.tags,
        )
        print(f"load         : {args.users} users, spawn {args.spawn_rate}/s, duration {args.run_time}")
        if args.tags:
            print(f"tags         : {args.tags}")
        print(f"command      : {' '.join(command)}")
        print("-" * 96)
        sampler = ProcessSampler(server.pid)
        if args.sample_process:
            sampler.start()
        completed = subprocess.run(command, cwd=PROJECT_ROOT, env=env, capture_output=True, text=True)
        process_metrics = sampler.stop()
        (out_dir / "locust_stdout.txt").write_text(completed.stdout + completed.stderr, encoding="utf-8")
        if verbose:
            print(completed.stdout)
        if completed.stderr.strip():
            print(completed.stderr, file=sys.stderr)

        stats_csv = Path(f"{csv_prefix}_stats.csv")
        if not stats_csv.is_file():
            # Locust never produced a report (bad flag, crash, zero-time run). Record
            # the failure instead of raising, so a matrix runner can continue.
            message = "locust produced no stats CSV"
            print(f"ERROR: {message} (exit code {completed.returncode})", file=sys.stderr)
            return {"label": label, "error": message, "exit_code": completed.returncode or 1}
        summary = parse_stats_csv(stats_csv)
        metadata = {
            "run_label": label,
            "timestamp_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "dataset_tasks": args.tasks,
            "dataset_comments_per_task": args.comments_per_task,
            "dataset_search_matches": expected_search_matches(args.tasks),
            "users": args.users,
            "spawn_rate": args.spawn_rate,
            "run_time": args.run_time,
            "page_size": args.page_size,
            "full_page_size": args.full_page,
            "search_term": args.search_term,
            "filter_status": args.filter_status,
            "filter_priority": args.filter_priority,
            "host": base_url,
            "tags": args.tags or "(all scenarios)",
            "locust_command": " ".join(command),
            "api_cpu_samples": process_metrics.get("sample_count"),
            "api_mean_cpu_percent": process_metrics.get("mean_cpu_percent"),
            "api_max_cpu_percent": process_metrics.get("max_cpu_percent"),
            "api_mean_rss_mb": process_metrics.get("mean_rss_mb"),
            "api_max_rss_mb": process_metrics.get("max_rss_mb"),
            **collect_environment(database_url),
        }
        (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        (out_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        (out_dir / "summary.md").write_text(
            render_markdown(summary, metadata, f"{csv_prefix}_stats.csv"), encoding="utf-8"
        )

        aggregated = summary.get("aggregated") or {}
        print("-" * 96)
        print(
            "TOTALS  requests={req}  failures={fail}  failure_rate={fr:.4f}  rps={rps:.2f}  "
            "avg={avg:.1f}ms  median={med:.1f}ms  p95={p95:.1f}ms  p99={p99:.1f}ms".format(
                req=int(aggregated.get("request_count", 0)),
                fail=int(aggregated.get("failure_count", 0)),
                fr=float(aggregated.get("failure_rate", 0.0)),
                rps=float(aggregated.get("requests_per_second", 0.0)),
                avg=float(aggregated.get("average_ms", 0.0)),
                med=float(aggregated.get("median_ms", 0.0)),
                p95=float(aggregated.get("p95_ms", 0.0)),
                p99=float(aggregated.get("p99_ms", 0.0)),
            )
        )
        print(f"artifacts    : {out_dir} (summary.md, summary.json, locust_stats.csv, locust_report.html)")
        if completed.returncode != 0:
            print(f"WARNING: locust exited with code {completed.returncode}", file=sys.stderr)
            exit_code = completed.returncode
    finally:
        server.terminate()
        try:
            server.wait(timeout=15)
        except subprocess.TimeoutExpired:  # pragma: no cover - defensive
            server.kill()
        server_output = server.stdout.read() if server.stdout else ""
        if server_output.strip():
            (out_dir / "uvicorn_stdout.txt").write_text(server_output, encoding="utf-8")
        if not args.keep_database and not args.database and db_path.exists():
            db_path.unlink()

    return {
        "label": label,
        "summary": summary,
        "metadata": metadata,
        "exit_code": exit_code,
    }


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: run exactly one load test."""
    return int(execute_run(config_from_args(parse_args(argv))).get("exit_code", 0))


if __name__ == "__main__":
    raise SystemExit(main())
