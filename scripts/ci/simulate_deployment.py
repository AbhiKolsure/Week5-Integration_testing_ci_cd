"""Validate the application locally without deploying or touching project data."""

from __future__ import annotations

import importlib
import os
import secrets
import sys
import tempfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
REQUIRED_FILES = (
    Path("app/main.py"),
    Path("app/database.py"),
    Path("app/security.py"),
    Path("requirements.txt"),
    Path("pyproject.toml"),
    Path(".github/workflows/ci-cd.yml"),
)


def report(label: str, passed: bool, detail: str = "") -> None:
    result = "PASS" if passed else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"{label}: {result}{suffix}")


def validate_required_files() -> tuple[bool, list[str]]:
    missing = [str(path) for path in REQUIRED_FILES if not (PROJECT_ROOT / path).is_file()]
    return not missing, missing


def validate_application() -> tuple[bool, bool, str]:
    previous_environment = {
        key: os.environ.get(key)
        for key in ("AUTH_SECRET_KEY", "ACCESS_TOKEN_EXPIRE_MINUTES", "DATABASE_URL")
    }
    import_ok = False
    health_ok = False
    detail = ""

    try:
        with tempfile.TemporaryDirectory(prefix="week5-simulated-cd-") as temp_dir:
            database_path = Path(temp_dir) / "simulation.db"
            os.environ["AUTH_SECRET_KEY"] = secrets.token_urlsafe(48)
            os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
            os.environ["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"

            module = importlib.import_module("app.main")
            application: Any = getattr(module, "app", None)
            import_ok = isinstance(application, FastAPI)
            if not import_ok:
                detail = "app.main does not expose a FastAPI app"
            else:
                try:
                    with TestClient(application) as client:
                        response = client.get("/health")
                    health_ok = (
                        response.status_code == 200
                        and response.json().get("status") == "ok"
                    )
                    detail = (
                        f"HTTP {response.status_code}, status={response.json().get('status')!r}"
                        if health_ok
                        else f"HTTP {response.status_code}, response={response.text}"
                    )
                finally:
                    database_module = importlib.import_module("app.database")
                    database_module.engine.dispose()

    except Exception as exc:
        health_ok = False
        detail = f"{type(exc).__name__}: {exc}"
    finally:
        for key, value in previous_environment.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    return import_ok, health_ok, detail


def main() -> int:
    print("SIMULATED DEPLOYMENT")
    print("--------------------")

    files_ok, missing_files = validate_required_files()
    report(
        "Required files",
        files_ok,
        "missing: " + ", ".join(missing_files) if missing_files else "",
    )

    import_ok, health_ok, detail = validate_application()
    report("Application import", import_ok)
    report("Startup/health validation", health_ok, detail)

    gate_ok = files_ok and import_ok and health_ok
    report("Deployment gate", gate_ok)
    report("Final result", gate_ok)
    return 0 if gate_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
