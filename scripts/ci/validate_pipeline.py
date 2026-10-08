"""Validate the local Actions workflow structure and simulated deployment gate."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "ci-cd.yml"
SIMULATOR_PATH = PROJECT_ROOT / "scripts" / "ci" / "simulate_deployment.py"


def check(label: str, passed: bool) -> bool:
    print(f"[{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")
    workflow: dict[str, Any] = yaml.load(workflow_text, Loader=yaml.BaseLoader)
    jobs = workflow.get("jobs", {})
    ci = jobs.get("ci", {})
    deployment = jobs.get("simulated-cd", {})
    ci_steps = ci.get("steps", [])
    deployment_steps = deployment.get("steps", [])
    ci_commands = [step["run"] for step in ci_steps if "run" in step]
    deployment_commands = [step["run"] for step in deployment_steps if "run" in step]
    results = [
        check(
            "push and pull_request triggers target main",
            workflow.get("on", {}).get("push", {}).get("branches") == ["main"]
            and workflow.get("on", {}).get("pull_request", {}).get("branches") == ["main"],
        ),
        check(
            "both jobs configure Python 3.14",
            all(
                any(
                    step.get("with", {}).get("python-version") == "3.14"
                    for step in steps
                )
                for steps in (ci_steps, deployment_steps)
            ),
        ),
        check(
            "both jobs install requirements.txt",
            all(
                "python -m pip install -r requirements.txt" in commands
                for commands in (ci_commands, deployment_commands)
            ),
        ),
        check(
            "CI includes Ruff and the complete pytest suite",
            "python -m ruff check app tests scripts benchmarks" in ci_commands
            and "python -m pytest -q" in ci_commands,
        ),
        check(
            "Ruff and pytest are required failure-sensitive steps",
            all(
                "continue-on-error" not in step
                for step in ci_steps
                if step.get("run")
                in {
                    "python -m ruff check app tests scripts benchmarks",
                    "python -m pytest -q",
                }
            ),
        ),
        check(
            "simulated deployment depends on successful CI",
            deployment.get("needs") == "ci"
            and deployment.get("if") == "needs.ci.result == 'success'",
        ),
        check(
            "simulated deployment invokes the local validation script",
            "python scripts/ci/simulate_deployment.py" in deployment_commands,
        ),
        check(
            "workflow contents permission is read-only",
            workflow.get("permissions", {}).get("contents") == "read",
        ),
    ]

    actions = [
        step["uses"]
        for step in ci_steps + deployment_steps
        if "uses" in step
    ]
    results.append(
        check(
            "workflow actions are limited to checkout and Python setup",
            len(actions) == 4
            and all(
                action.startswith(("actions/checkout@", "actions/setup-python@"))
                for action in actions
            ),
        )
    )

    high_confidence_secret = re.compile(
        r"gh[pousr]_[A-Za-z0-9]{30,}"
        r"|AKIA[0-9A-Z]{16}"
        r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    )
    results.append(
        check(
            "workflow contains no credential literals or GitHub secret references",
            not high_confidence_secret.search(workflow_text)
            and "secrets." not in workflow_text,
        )
    )

    commands = "\n".join(ci_commands + deployment_commands)
    results.extend(
        (
            check(
                "workflow contains no cloud/production deployment command",
                not re.search(
                    r"(?i)\b(aws|az|gcloud|kubectl|terraform|vercel|flyctl|heroku)\b",
                    commands,
                ),
            ),
            check(
                "workflow contains no destructive command",
                not re.search(
                    r"(?i)\b(rm\s+-rf|rmdir|remove-item|drop\s+database|kubectl\s+delete)\b",
                    commands,
                ),
            ),
        )
    )

    simulations = [
        subprocess.run(
            [sys.executable, str(SIMULATOR_PATH)],
            cwd=PROJECT_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        for _ in range(2)
    ]
    successful_runs = all(
        run.returncode == 0 and "Final result: PASS" in run.stdout
        for run in simulations
    )
    results.append(check("two simulated deployment runs pass", successful_runs))
    results.append(
        check(
            "simulated deployment success output is repeatable",
            simulations[0].stdout == simulations[1].stdout,
        )
    )
    print(f"Pipeline validation: {sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
