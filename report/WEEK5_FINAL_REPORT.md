# Week 5 — Integration Testing and Continuous Deployment Simulation

**YuvaIntern technical internship project**  
**Validation date:** 2026-10-08  
**Project:** Isolated Week 5 copy of the inherited FastAPI task-management backend

## 1. Executive Summary

This project integrates account authentication with an existing FastAPI task
service, validates user/task/comment/error behavior through HTTP integration
tests, and defines a GitHub Actions pipeline for continuous integration and
simulated deployment validation. Local checks use an isolated SQLite database
for tests and a temporary database for the deployment simulation.

The final local validation ran the complete pytest suite, targeted
authentication, task API/task lifecycle and regression tests, Ruff, two HTTP
smoke scripts, application startup/health validation, and workflow/security
checks. The complete suite reported 125 passing tests and two existing
deprecation warnings. The simulated deployment reported PASS. No GitHub remote
is configured; GitHub-hosted workflow execution is therefore not claimed.

## 2. Official Task Requirements

Week 5 calls for integration testing across authentication, data management and
error handling; a CI configuration that runs tests on code changes; simulated
CD; documentation of backend module interactions; and a reproducible account
of test and pipeline validation. This project covers those requirements with
HTTP-to-database tests, an Actions workflow, a CI-gated deployment validation
job, and evidence files containing actual local command output.

## 3. Project Architecture

- `app/main.py` constructs the FastAPI application, validates auth settings
  during startup, and registers system/auth/task routes.
- `app/routes/auth.py` implements registration and login.
- `app/routes/tasks.py` protects task, comment, filtering and statistics
  endpoints using the shared bearer-auth dependency.
- `app/schemas.py` validates HTTP input and limits public response fields.
- `app/security.py` hashes/verifies passwords, signs/verifies JWT access
  tokens, and resolves users through the database dependency.
- `app/models.py` contains the user, task and comment ORM models.
- `app/database.py` configures SQLAlchemy sessions and SQLite.
- `app/crud.py` contains task/comment data operations called by the API layer.
- `tests/` combines HTTP API tests, auth integration tests, regressions,
  business-logic and query behavior tests.

The test fixtures override the database dependency with a fresh in-memory
SQLite database. No external database service is used by tests.

## 4. Authentication Implementation

Registration normalizes email input, validates the password, writes an Argon2id
hash, and returns a public user representation that excludes password fields.
Duplicate accounts return HTTP 409. Login returns an HS256 signed bearer JWT
with issuer, subject, issued-at, expiration and token-type claims. The default
token lifetime is 30 minutes, configurable from 1 through 1440 minutes.

`AUTH_SECRET_KEY` must be supplied from the runtime environment and contain at
least 32 bytes. The example placeholder is rejected during configuration
validation. Protected task/comment/statistics endpoints return HTTP 401 for
missing or invalid bearer credentials. Unknown-email and incorrect-password
login failures have the same generic response.

## 5. Integration Testing Strategy

Tests use FastAPI's HTTP test client against the actual route stack and a
per-test isolated database. This validates request parsing and schemas, auth
dependencies, ORM persistence, CRUD behavior, and the HTTP response or error
contract together.

The integration coverage review found these exercised interactions:

1. Client requests pass through registration/login routes, schema validation,
   password verification/hashing, persistence and public HTTP response
   filtering.
2. Issued tokens are decoded by the protected-route dependency, resolved to a
   stored user, and either authorize API operations or produce an HTTP 401.
3. Authenticated task/comment requests flow through schemas, routes, CRUD and
   database persistence; reads/filters/statistics return values based on stored
   records and deletion updates subsequent reads.
4. Invalid inputs and missing resources produce the expected HTTP 422/404
   responses; duplicate registration and invalid credentials produce 409/401.
5. Regression tests check task response codes, validation, filtering/search,
   missing-resource behavior, timestamp normalization and query behavior.

**Coverage percentage was not used as a completion claim; integration behavior was validated through executable tests.**

## 6. Test Scenarios

Authentication tests cover unsafe/missing/example secret configuration,
registration and password-hash persistence, public response fields, duplicate
registration, valid and invalid login, token claims/lifetime, invalid input,
missing/malformed/wrong-scheme/expired/invalid-signature tokens, and a full
registered-user task/comment lifecycle.

Task and comment API tests cover task creation, reads, pagination, updates,
filters, statistics, comment creation/listing, deletion/cascade behavior,
validation errors and unknown identifiers. Regression tests retain the
identified defect cases. All tests use test fixtures rather than the persistent
runtime database.

## 7. Error Handling

Invalid schemas return HTTP 422. Duplicate email registration returns HTTP 409.
Invalid login returns a generic HTTP 401. Missing or invalid tokens return HTTP
401 with a Bearer challenge. Unknown tasks return HTTP 404 without exposing
database exception details. Tests assert status codes and relevant response
payloads.

## 8. CI Pipeline

`.github/workflows/ci-cd.yml` is configured for pushes to `main` and pull
requests targeting `main`. The CI job checks out the repository, configures
Python 3.14, upgrades pip, installs `requirements.txt`, runs
`python -m ruff check app tests scripts benchmarks`, and runs
`python -m pytest -q`. The steps are fail-fast in normal Actions behavior: a
non-zero Ruff or pytest result fails the CI job.

The simulated deployment job declares `needs: ci` and runs only when
`needs.ci.result == 'success'`. Thus a failed CI job prevents the deployment
validation from being reported as successful.

## 9. Simulated CD Pipeline

The simulation runs `scripts/ci/simulate_deployment.py`. It verifies required
application/configuration files, imports `app.main`, checks for a FastAPI
application object, starts the application lifespan, and requests `/health`.
The script uses a generated per-run auth key and an SQLite file in a temporary
directory, disposes of the engine, restores prior environment settings, and
returns non-zero if validation fails.

This is a testable deployment gate only. It does not publish an image, modify
external infrastructure, contact cloud services, or perform a production
deployment.

## 10. Security Measures

- Argon2id password hashing; plaintext password is not stored.
- Public schemas omit stored password hashes.
- Runtime-only signing key with minimum-size and example-placeholder
  validation.
- Expiring, signed access tokens with required-claim validation.
- Protected endpoints require a resolvable authenticated user.
- Login error messages do not disclose whether the email exists.
- `.gitignore` excludes `.env`, SQLite database files, and Python caches.
- Workflow permissions are limited to read-only repository contents.
- Workflow has no secret references or deployment credentials and uses only
  checkout and Python setup actions.

Automated scans/checks found no apparent real credentials in the inspected
project files. The project contains synthetic test-only key strings used to
exercise auth behavior and a clearly unusable example placeholder. The folder
has no `.git` metadata, so Git history and tracked commit contents could not be
audited.

## 11. Validation Results

Local validation was performed with Python 3.14.3. The final actual results
recorded in `artifacts/final_week5_validation.txt` include:

- Full pytest suite: **125 passed**, 2 warnings.
- Auth integration tests: **17 passed**, 2 warnings.
- Existing task API/task lifecycle tests: **32 passed**, 2 warnings.
- Regression tests: **8 passed**, 2 warnings.
- Ruff: **All checks passed!**
- `scripts/smoke_check.py`: real HTTP server health/auth/protected task
  lifecycle checks; output recorded in the final artifact.
- `scripts/final_api_smoke.py`: real HTTP auth and broad task/comment
  validation; output recorded in the final artifact.
- Simulated CD: required files PASS; app import PASS; startup/health PASS;
  deployment gate PASS; final result PASS.
- PyYAML workflow syntax, trigger, commands, job dependency, permissions and
  safety checks: **14/14 passed** via `python scripts/ci/validate_pipeline.py`;
  details are in `artifacts/final_ci_cd_validation.txt`.

The test client reports Starlette/httpx and AnyIO deprecation warnings. They
did not fail the tests. No Week 4 performance/load suite was rerun for this
phase.

GitHub-hosted workflow execution: NOT VERIFIED — repository remote is not configured.

## 12. Known Limitations

- There is no Git repository metadata or configured GitHub remote. No remote
  workflow result, branch, or commit history can be verified.
- Simulated CD is validation, not production deployment.
- Test execution reports two existing deprecation warnings.
- Task data is shared among authenticated accounts; account ownership
  separation, token revocation and login rate limiting are not included.
- No test coverage percentage was measured.
- Inherited Week 4 performance artifacts are retained in the source project;
  expensive performance/load tests were not run in final validation.

## 13. Reproduction Instructions

From the project root, with Python 3.14:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ruff check app tests scripts benchmarks
python -m pytest -q
python -m pytest tests/test_auth_integration.py -q
python -m pytest tests/test_api.py tests/test_tasks.py -q
python -m pytest tests/test_regression.py -q
python scripts/smoke_check.py
python scripts/final_api_smoke.py
python scripts/ci/validate_pipeline.py
python scripts/ci/simulate_deployment.py
```

To start the app locally, set a new `AUTH_SECRET_KEY` in the shell environment
and run `python -m uvicorn app.main:app --reload`. Never commit a real key or
`.env` file.

## 14. Conclusion

The local evidence verifies integrated authentication/data flows, task and
comment behavior, expected error responses, regressions, static analysis, and
the simulated CI-to-CD validation path. The workflow is configured but has not
been run by GitHub because no remote exists. No production deployment or
GitHub-hosted success is claimed.
