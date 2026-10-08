# Week 5 — Integration Testing and Continuous Deployment Simulation

## 1. Project Overview

This Week 5 project extends the inherited FastAPI backend with account
authentication, HTTP-to-database integration tests, and a GitHub Actions CI
workflow followed by a simulated deployment validation. The application runs
with SQLite; CI and deployment checks do not require production services.

## 2. Objectives

The work addresses the YuvaIntern Week 5 objectives to integrate backend
components, test authentication/data management/error handling, run integration
tests on code changes, and document a simulated CI/CD pipeline. The deployment
stage validates application startup and health only; it does not deploy to
production.

## 3. Existing Backend Architecture

- **FastAPI:** `app/main.py` creates the application and its lifespan.
- **Routes:** `app/routes/auth.py` implements registration/login;
  `app/routes/tasks.py` exposes authenticated task, comment, and statistics
  endpoints.
- **Schemas:** `app/schemas.py` defines request validation and public response
  shapes.
- **Database:** `app/database.py` configures SQLAlchemy and SQLite;
  `app/models.py` defines users, tasks, and comments.
- **Authentication:** `app/security.py` handles Argon2 password hashing,
  signed access tokens, and bearer-token validation.
- **Business logic/data access:** `app/crud.py` contains the task/comment
  persistence operations used by routes.
- **Tests:** `tests/` contains isolated-database API/auth integration,
  regression, CRUD, edge-case, and query-count tests.

The task and comment data remains shared across authenticated accounts; this
implementation does not add per-user ownership.

## 4. Authentication

`POST /auth/register` validates and normalizes an email, checks password
requirements, stores an Argon2id hash, and returns a public user response.
Duplicate email addresses return HTTP 409. `POST /auth/login` verifies the
password and returns a signed HS256 JWT with an expiration; invalid user/password
combinations share a generic HTTP 401 response. Token lifetime defaults to 30
minutes and is configurable from 1 to 1440 minutes.

Task, comment, filtering, and statistics endpoints require a valid bearer token.
Missing, malformed, expired, incorrectly signed, or otherwise invalid tokens
receive HTTP 401 with a Bearer challenge. Configure a random
`AUTH_SECRET_KEY` of at least 32 bytes in the process environment. The example
placeholder is rejected. Do not commit secrets or `.env` files.

## 5. Integration Testing Strategy

Integration tests call the FastAPI application through its HTTP test client
while using a fresh in-memory SQLite database. This exercises request parsing,
routes, auth dependencies, schemas, database persistence, task business logic,
and HTTP response handling together. No external database or service is needed.

Representative scenarios include registration and password-hash persistence,
duplicate registration, valid/invalid login, expired/malformed/invalid tokens,
unauthenticated protected routes, and a registered-user task/comment lifecycle
with list filters, statistics, and deletion.

## 6. Error Handling

- Invalid request data: HTTP 422.
- Duplicate registration: HTTP 409.
- Invalid login credentials: generic HTTP 401.
- Missing, malformed, or expired bearer token: HTTP 401.
- Unknown task: HTTP 404 with a clean resource-specific message.

## 7. CI Pipeline

`.github/workflows/ci-cd.yml` runs on pushes to `main` and pull requests
targeting `main`:

Code change → GitHub Actions → install dependencies → Ruff → pytest

It sets up Python 3.14, upgrades pip, installs `requirements.txt`, runs
`python -m ruff check app tests scripts benchmarks`, then runs
`python -m pytest -q`. A failure in either check fails the CI job.

## 8. Simulated CD

After successful CI, the `simulated-cd` job runs
`python scripts/ci/simulate_deployment.py`. The script checks required files,
imports the FastAPI app, runs application startup, and calls `/health`. It uses
a generated per-run signing key and a temporary SQLite file that is closed and
removed after validation.

CI success → deployment gate → application validation → startup/health →
simulated deployment

This is **not** a production deployment and does not contact cloud
infrastructure or require cloud credentials.

## 9. Test Results

Final local verification on Python 3.14.3:

- Full pytest suite: **125 passed**, 2 existing deprecation warnings.
- Authentication integration tests: **17 passed**, 2 warnings.
- Existing task API/task lifecycle tests (`test_api.py` and `test_tasks.py`):
  **32 passed**, 2 warnings.
- Regression tests: **8 passed**, 2 warnings.
- Ruff: **All checks passed!**
- HTTP auth/protected task smoke scripts: recorded with command output in the
  final validation artifact.
- Simulated deployment: PASS; startup and `/health` returned HTTP 200.
- YAML/workflow/security checks: PASS.

See `artifacts/final_week5_validation.txt` for commands and captured outputs.
GitHub-hosted CI has not run.

## 10. Security

Passwords are Argon2id-hashed; user responses omit password/hash fields.
Authentication signing keys are supplied at runtime, have minimum length
validation, and reject the sample placeholder. Tokens are signed, time-limited,
and validated for issuer, claims, type, and subject. Tests exercise invalid and
expired tokens. `.gitignore` excludes `.env` and local database files. No Git
metadata is present, so repository history/remote scanning is unavailable.

## 11. Repository Structure

```text
app/                    FastAPI app, routes, schemas, models, CRUD, auth
tests/                  HTTP integration, regression, and other tests
scripts/ci/             Simulated deployment validation
scripts/                Smoke and inherited Week 4 utility scripts
benchmarks/             Inherited benchmark and Locust scenarios
.github/workflows/      GitHub Actions CI and simulated CD
docs/                   Week 5 architecture and pipeline documentation
report/                 Final Markdown/DOCX report and submission description
artifacts/              Captured test, smoke, security, and pipeline evidence
```

## 12. Installation

Use Python 3.14 (locally verified as 3.14.3):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 13. Running Tests

```powershell
python -m pytest -q
python -m pytest tests/test_auth_integration.py -q
python -m pytest tests/test_api.py tests/test_tasks.py -q
python -m pytest tests/test_regression.py -q
python -m ruff check app tests scripts benchmarks
```

## 14. Running Authentication

Set a fresh key in the current PowerShell process; do not paste a real key into
source files or commit it:

```powershell
$env:AUTH_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
$env:ACCESS_TOKEN_EXPIRE_MINUTES = "30"
python -m uvicorn app.main:app --reload
```

Register at `/auth/register`, log in at `/auth/login`, then provide the returned
token as `Authorization: Bearer <access_token>` when calling task endpoints.

## 15. Running CI/CD Simulation

```powershell
python -m ruff check app tests scripts benchmarks
python -m pytest -q
python scripts/ci/simulate_deployment.py
```

The simulator reports actual file, import, startup/health, gate, and final
results and returns a non-zero exit code on failure.
Run `python scripts/ci/validate_pipeline.py` to validate workflow triggers,
commands, CI-to-CD dependency, safety checks, and repeatable simulation output.

## 16. Known Limitations

- The project has no Git metadata or configured remote. GitHub-hosted workflow
  execution is not verified.
- YuvaIntern requires a GitHub project URL for the technical internship
  submission; configure and verify a remote before submitting.
- The deployment job is a local/CI validation simulation, not production CD.
- Existing Starlette/httpx and AnyIO test-client deprecation warnings appear
  during pytest; they do not fail the current test run.
- Task data is shared among authenticated users; ownership isolation, token
  revocation, and login rate limiting are not implemented.
- The original Week 4 performance artifacts remain historical evidence; this
  phase did not rerun expensive performance/load suites.
