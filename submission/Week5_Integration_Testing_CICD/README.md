# Week 5 — Integration Testing and Continuous Deployment Simulation

This educational internship project extends the inherited Week 4 FastAPI backend in an isolated Week 5 copy. It adds authentication, HTTP integration tests, regression checks, GitHub Actions CI, and a simulated deployment gate. The original Week 4 project and inherited performance evidence remain preserved; expensive Week 4 load tests were not rerun.

## 1. Project Overview

The application integrates FastAPI routes, Pydantic schemas, SQLAlchemy models/database sessions, CRUD operations, and HTTP error handling. Week 5 adds registration/login and protects task and comment operations.

## 2. Week 5 Objective

The project validates authentication, data management, and error handling as an integrated API, then exercises static checks, the complete test suite, and non-production deployment validation in an automated workflow.

## 3. Existing Backend Architecture

- `app/main.py` builds the FastAPI application, lifespan, and routes.
- `app/routes/` contains authentication and task/comment endpoints.
- `app/schemas.py` defines request validation and response shapes.
- `app/models.py` and `app/database.py` define SQLAlchemy persistence.
- `app/crud.py` contains task/comment data operations.
- `app/security.py` contains password hashing, JWT handling, and bearer validation.
- `tests/` covers HTTP integration and regression behavior.

Authenticated users continue to share existing task/comment data; per-user ownership isolation is outside this project scope.

## 4. Authentication Architecture

Registration stores an Argon2id password hash. Login validates credentials and returns an expiring HS256 JWT. The signing key is runtime configuration, not committed source. Public responses omit password data.

## 5. API Authentication Flow

Register at `/auth/register` and log in at `/auth/login`; for protected task/comment requests, include the returned token as a Bearer credential in the HTTP authorization header.

## 6. Integration Testing Strategy

FastAPI TestClient exercises real HTTP routing, validation, authentication, persistence, and response handling. Tests use isolated in-memory SQLite databases.

## 7. Regression Testing

Regression tests protect inherited task behavior, including validation, filters, missing-resource handling, and task/comment operations.

## 8. Test Environment

Local verification used Python 3.14.3 and isolated SQLite test databases. No hosted database or production infrastructure is required.

## 9. Test Commands

```powershell
python -m pytest -q
python -m pytest tests/test_auth_integration.py -q
python -m pytest tests/test_regression.py -q
python -m ruff check app tests scripts benchmarks
python scripts/ci/simulate_deployment.py
```

## 10. Authentication Test Coverage

Authentication cases include registration, duplicate accounts, valid/invalid credentials, password-hash persistence, token claims and expiry, invalid tokens, missing credentials, and protected API access.

## 11. CI Pipeline

The workflow checks out the repository, configures Python 3.14, installs dependencies, runs Ruff, and runs the complete pytest suite. Ruff or pytest failure fails CI.

## 12. GitHub Actions Workflow

`.github/workflows/ci-cd.yml` triggers for pushes to `main` and pull requests targeting `main`. The GitHub repository is https://github.com/AbhiKolsure/Week5-Integration_testing_ci_cd. Hosted run 37741348125 completed successfully; both CI and Simulated deployment jobs succeeded.

## 13. Simulated Continuous Deployment

The deployment simulator validates required files, imports the application, starts its lifespan, and checks `/health`. It uses temporary local resources and does not perform production deployment or contact cloud infrastructure.

## 14. CI → CD Gate

The simulated deployment job requires CI success. In hosted run 37741348125, CI completed successfully before the simulated deployment job, which also passed.

## 15. Security Considerations

Passwords are hashed with Argon2id; JWT signing keys come from runtime configuration. `.gitignore` excludes real environment files, caches, bytecode, and local database files. The security scan found no suspicious credentials in tracked content. This is not a claim of complete security.

## 16. Validation Results

- Local full pytest: **125 passed, 2 deprecation warnings**.
- Authentication integration tests: **17 passed**.
- Regression tests: **8 passed**.
- Ruff: **PASS**.
- Simulated CD: **PASS**.
- GitHub Actions run 37741348125: **completed / success**, with both jobs successful.

Older captured audit outputs are historical snapshots from before the remote
was configured. The current status is recorded in this README and
`artifacts/final_submission_audit.txt`.

## 17. Known Limitations

The deployment is simulated, not production CD. Upstream test-client deprecation warnings remain. Task data is shared across authenticated accounts; ownership isolation, token revocation, and login rate limiting are not implemented. No production-capacity or security guarantee is claimed.

## 18. Repository Structure

```text
app/                    application modules
tests/                  integration and regression tests
scripts/ci/             pipeline validation and simulated deployment
.github/workflows/      GitHub Actions workflow
artifacts/              actual local validation and audit evidence
report/                 final report, DOCX, and submission description
docs/                   authentication and CI/CD documentation
benchmarks/              retained inherited Week 4 benchmark material
```

## 19. Reproduction Instructions

Install dependencies from `requirements.txt`, set a fresh `AUTH_SECRET_KEY` in the runtime environment, then execute the commands in section 9. Never commit a real secret or `.env` file.

## 20. Week 5 Conclusion

The project demonstrates tested integration across API, authentication, and persistence modules and a CI-gated deployment simulation. The GitHub workflow and its successful run are documented above. This remains an educational project and does not deploy to production.
