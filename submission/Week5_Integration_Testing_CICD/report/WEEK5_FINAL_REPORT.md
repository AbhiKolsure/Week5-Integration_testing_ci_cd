# Week 5 Final Report

## 1. Cover Page

Week 5 — Integration Testing and Continuous Deployment Simulation

Educational internship project using an isolated Week 5 copy of the inherited Week 4 FastAPI backend.

## 2. Executive Summary

This project extends the inherited FastAPI backend with authentication, API integration validation, and a CI/CD simulation. It validates that backend modules work together correctly and that the application can be checked locally without performing a production deployment. The final evidence reflects actual local test runs and static checks rather than assumptions about GitHub-hosted execution.

## 3. Internship Task Objective

The objective was to integrate backend modules, cover authentication and error handling with integration tests, and implement a CI pipeline that runs tests automatically. A simulated deployment gate was added to verify file existence, importability, startup, and health validation without contacting external infrastructure.

## 4. Existing Backend

The inherited backend includes FastAPI routes, schemas, ORM models, database configuration, CRUD logic, and task/comment APIs. Week 4 evidence was preserved and no original Week 4 files were modified. Week 5 work was kept inside the isolated Week 5 project directory only.

## 5. Problem Statement

A backend that works in isolation can still fail when authentication, request validation, database persistence, and API behavior are combined. This project addressed that by testing the application through HTTP requests and a fresh in-memory database. The goal was to check real integration points, not just isolated functions.

## 6. Week 5 Approach

The Week 5 approach added secure authentication, protected task routes, integration tests, regression checks, and CI validation. The project also added a deployment simulator that verifies whether the application is importable and starts correctly before a simulated deployment is considered successful.

## 7. Authentication Implementation

Authentication was implemented with Argon2id password hashing, JWT access tokens, and bearer-token enforcement. User registration and login routes were added without changing the original Week 4 backend behavior beyond required route protection. Invalid or missing tokens are rejected with HTTP 401 responses.

## 8. Registration and Login

Registration validates email and password input, hashes the password, stores the user record, and returns a sanitized public response. Login checks the stored hash and returns a JWT that includes required token claims and expiration. A generic 401 response is used for invalid credentials to avoid revealing account existence.

## 9. Password Security

Passwords are never stored in plaintext. The user record stores only an Argon2id hash. Public responses omit password/hash values, and the runtime secret is required to be set in the environment. Example placeholders are rejected during app startup validation.

## 10. JWT Authentication

JWTs are generated and validated using the configured secret key. Token claims are checked for issuer, subject, token type, and expiration. Protected task and comment endpoints require a valid bearer token before they will proceed.

## 11. Protected APIs

Protected endpoints include task access, comment access, and related operations that require a valid authenticated user. Calls without authorization return HTTP 401, and malformed or expired tokens are rejected before the request reaches the business logic.

## 12. Integration Test Architecture

Integration tests call the API through FastAPI TestClient and an in-memory SQLite database. Each test uses isolated dependencies and verifies behavior from route handling to database persistence. This gives a realistic view of how modules interact in real requests.

## 13. Test Scenarios

The integration suite covers duplicate registration, invalid login, token validation, missing bearer tokens, protected route access, and task/comment lifecycle flows. These tests validate both success and failure scenarios and confirm that the API returns predictable HTTP statuses.

## 14. Regression Tests

Regression tests preserve the expected behavior of existing task and comment routes. They check validation, missing-resource handling, filters, statistics, and known behavior that must remain stable after the authentication addition. The tests intentionally do not claim production-scale performance results.

## 15. CI Pipeline

The workflow file `.github/workflows/ci-cd.yml` runs on pushes to `main` and pull requests targeting `main`. It installs dependencies, sets up Python 3.14, runs Ruff, and executes the complete pytest suite. Failures in either lint or tests fail the CI job.

## 16. GitHub Actions

The GitHub remote is configured at https://github.com/AbhiKolsure/Week5-Integration_testing_ci_cd. GitHub Actions run 37741348125 completed successfully on `main`; the CI and Simulated deployment jobs both succeeded. The successful CI job executed dependency installation, Ruff, and the complete pytest suite. Older captured local audit outputs are historical snapshots from before remote configuration.

## 17. Simulated CD

The simulated deployment script validates file presence, application import, startup behavior, and health checks. It is designed to behave as a non-production deployment gate and does not contact cloud infrastructure, deploy to production, or use credentials.

## 18. CI/CD Gate

The deployment job depends on the successful completion of CI. If the lint or pytest step fails, the deployment simulation is not treated as successful. This forms a valid CI-to-CD gate without performing a real release.

## 19. Security Validation

Security checks include secret scanning, `.gitignore` review, environment-file review, and verification that no real credentials were committed. The workflow contains no secrets or credentials. It uses checkout and Python setup actions only.

## 20. Actual Test Results

Measured against the actual project environment:

- Python 3.14.3
- Full pytest suite: 125 passed, 2 warnings
- Authentication integration tests: 17 passed, 2 warnings
- Regression tests: 8 passed, 2 warnings
- Ruff: All checks passed
- Simulated deployment: PASS
- GitHub Actions run 37741348125: completed / success; both workflow jobs succeeded.

## 21. Actual CI/CD Results

Local validation used the same Ruff, pytest, and simulated deployment commands configured in CI. In addition, GitHub-hosted run 37741348125 completed successfully with both workflow jobs passing. The CI-to-simulated-CD gate passed: simulated deployment ran only after CI success.

## 22. Known Limitations

The project is not a production deployment system. The app uses local SQLite for testing and does not claim production-scale capacity or security guarantees. Some upstream deprecation warnings remain visible in the dependency stack, but they do not fail the current test suite. GitHub run 37741348125 verifies the commit it tested; later commits require their own workflow verification.

## 23. Repository Structure

- app/
- tests/
- scripts/
- .github/workflows/
- artifacts/
- report/
- docs/
- README.md
- requirements.txt
- pyproject.toml

## 24. Reproduction Steps

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:AUTH_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
python -m pytest -q
python -m ruff check app tests scripts benchmarks
python scripts/ci/simulate_deployment.py
```

## 25. Conclusion

The Week 5 project delivers measured, evidence-based validation for backend integration, authentication, CI, and deployment simulation. GitHub Actions run 37741348125 succeeded in both jobs. The simulated deployment validates application readiness only and is not a production deployment.
