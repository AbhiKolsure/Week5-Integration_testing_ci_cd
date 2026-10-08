# Week 5 Continuous Integration and Simulated Deployment

## Continuous Integration

The GitHub Actions workflow at `.github/workflows/ci-cd.yml` runs for pushes
to `main` and pull requests targeting `main`. It checks out the code, sets up
Python 3.14 (the version used to validate this project), upgrades pip, and
installs the dependencies from `requirements.txt`.

CI runs `python -m ruff check app tests scripts benchmarks` followed by
`python -m pytest -q`. Both commands are required steps: if Ruff or the full
pytest suite exits unsuccessfully, the CI job fails.

## Simulated Continuous Deployment

The simulated deployment job depends on the CI job and runs only when CI
reports success. It installs the project dependencies and runs
`python scripts/ci/simulate_deployment.py`. The validation checks required
application/configuration files, imports the FastAPI application, starts its
lifespan, and requests `/health`.

The simulation assigns a fresh in-process authentication key and a SQLite
database inside a temporary directory. It does not use secrets, cloud
credentials, production infrastructure, or the project's existing database.
This is a deployment validation gate only; it does not deploy the application
to any environment.

## Pipeline Flow

Code Change
→ GitHub Actions
→ Install Dependencies
→ Ruff
→ Pytest
→ CI Success
→ Simulated CD
→ Deployment Validation
→ Success

## Local verification and evidence

Local commands use the same Python version, dependency installation, Ruff,
pytest, and simulated-deployment commands configured in the workflow. Their
actual output is recorded in:

- `artifacts/week5_ci_local_validation.txt`
- `artifacts/week5_cd_simulation.txt`
- `artifacts/week5_ci_cd_security_check.txt`
- `python scripts/ci/validate_pipeline.py` checks workflow structure, safety,
  and repeatable simulator output.

The Week 5 project copy currently has no Git metadata or configured remote.
Therefore, no push, pull request, or GitHub-hosted workflow run is claimed.
