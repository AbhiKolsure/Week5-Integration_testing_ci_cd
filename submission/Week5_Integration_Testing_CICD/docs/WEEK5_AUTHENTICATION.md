# Week 5 Authentication and Integration Tests

## Scope

This phase adds authentication to the inherited FastAPI task-management API and
tests the authentication/data flow end to end. It does not introduce per-user
task ownership: all authenticated accounts continue to use the existing shared
task and comment data. Existing task payloads and CRUD behavior remain intact;
task routes now require a bearer access token.

The Phase 3 GitHub Actions workflow and local deployment simulation are
documented in [`WEEK5_CI_CD.md`](WEEK5_CI_CD.md).

The Week 4 load-test harnesses have been adapted to send authenticated task requests.
The Locust orchestrator obtains a temporary token outside the measured Locust run; the
in-process query/benchmark helpers create an isolated user and signed test token. The
archived Week 4 performance outputs predate authentication and are retained as
historical results rather than treated as comparable post-auth measurements.

## Module interactions

- `app/models.py` defines the `User` record alongside the existing `Task` and
  `Comment` models. User email is unique; the only password-related database
  field is `password_hash`.
- `app/database.py` remains the single SQLAlchemy/SQLite configuration. Its
  existing metadata initialization imports the models and creates the `users`
  table when needed; the existing task tables and fields are not changed.
- `app/schemas.py` validates registration and login input and defines public
  user and token responses. The public user response has no password/hash field.
- `app/security.py` hashes/verifies passwords, signs and validates access
  tokens, and resolves token subjects to existing users through the same
  database session dependency.
- `app/routes/auth.py` implements `POST /auth/register` and `POST /auth/login`.
- `app/routes/tasks.py` protects the existing task router using the shared
  authentication dependency. The handler and CRUD/service layer retain their
  existing task semantics.
- `app/main.py` validates authentication configuration during application
  startup and registers both authentication and task routers.

## Registration flow

1. The registration schema validates the email address and requires a password
   between 8 and 128 characters. Email input is trimmed and normalized to
   lowercase.
2. The auth route hashes the password with Argon2id using the library's secure
   defaults. Plaintext passwords are not written to the database.
3. SQLAlchemy stores the user in the same configured application database.
   Duplicate email addresses return HTTP 409; validation errors return HTTP
   422.
4. A successful response contains only the public user id, normalized email,
   and creation timestamp.

## Login and token flow

1. The login schema applies the same email/password validation.
2. The authentication service looks up the normalized email and verifies the
   password hash. Unknown emails and incorrect passwords return the same
   generic HTTP 401 response.
3. A successful login returns a JWT access token, `token_type: "bearer"`, and
   `expires_in` in seconds. Tokens use HS256 and contain a user id subject,
   issuer, issued-at time, expiration time, and access-token type.
4. The default lifetime is 30 minutes. `ACCESS_TOKEN_EXPIRE_MINUTES` may
   override it with a value from 1 through 1440.
5. For a protected request, the shared dependency verifies the signature,
   issuer, required claims, token type, and expiration, then loads the subject
   from the users table. Missing, malformed, invalid-signature, expired, or
   non-resolvable credentials return HTTP 401 with a Bearer challenge.

## Runtime configuration

Set `AUTH_SECRET_KEY` in the application environment to a random value of at
least 32 bytes. The application fails startup when the key is missing, too
short, or the unchanged example placeholder; it does not use a hard-coded
fallback. `ACCESS_TOKEN_EXPIRE_MINUTES` defaults to `30`. `.env.example`
contains a placeholder, not a usable secret, and `.env` is excluded by
`.gitignore`.

For a local PowerShell session, a secret can be generated without adding it to
the project:

```powershell
$env:AUTH_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
$env:ACCESS_TOKEN_EXPIRE_MINUTES = "30"
python -m uvicorn app.main:app --reload
```

Production deployments should provide the key through their secret manager or
runtime environment. Do not commit real keys or `.env` files.

## Integration-test strategy

`tests/conftest.py` creates a fresh in-memory SQLite database for every test and
overrides the FastAPI database dependency. The existing authenticated test
client keeps inherited API tests exercising the protected routes. Separate
fixtures provide an unauthenticated client, registration over HTTP, login over
HTTP, and an authenticated client using the resulting token.

`tests/test_auth_integration.py` uses the HTTP client and isolated database to
cover registration, password-hash persistence, duplicate accounts, successful
and failed logins, token response/claims, invalid registration data, missing
and malformed credentials, invalid signatures and claims, expired tokens, and
a complete authenticated task/comment/filter/statistics/deletion lifecycle.
No external service or persistent runtime database is used by these tests.

## Error handling and security considerations

- Invalid request fields return HTTP 422.
- Duplicate registrations return HTTP 409 without database exception details.
- Unknown-account and wrong-password login attempts use the same HTTP 401 body.
- Protected endpoints use HTTP 401 and a `WWW-Authenticate: Bearer` header for
  absent or invalid credentials.
- Password-hash fields are not included in any response schema.
- The JWT key is supplied at runtime and validated during application startup.
- Tokens are signed, time-limited, and checked for signature, issuer, required
  claims, access-token type, and a current user record.
- This implementation has no token revocation or rate limiting. It also does
  not isolate shared task data by user; both behaviors are outside this phase's
  stated scope.
- The Week 5 target directory has no Git metadata. Therefore, a Git history or
  remote scan for committed credentials cannot be claimed from this local
  checkout. No `.env` file is present in the target, and the example file uses
  a non-secret placeholder.

## Local validation record

The recorded outputs are preserved under `artifacts/`:

- [`week5_auth_test_output.txt`](../artifacts/week5_auth_test_output.txt):
  authentication integration tests, **17 passed**.
- [`week5_regression_test_output.txt`](../artifacts/week5_regression_test_output.txt):
  inherited regression tests, **8 passed**.
- [`week5_integration_test_output.txt`](../artifacts/week5_integration_test_output.txt):
  complete pytest suite, **125 passed**.
- [`week5_ruff_output.txt`](../artifacts/week5_ruff_output.txt): Ruff check,
  all checks passed.
- [`week5_http_smoke_output.txt`](../artifacts/week5_http_smoke_output.txt):
  both temporary-database HTTP smoke scripts completed with zero failed
  checks.
- [`week5_load_harness_smoke.txt`](../artifacts/week5_load_harness_smoke.txt):
  one 12-second harness smoke run sent 37 authenticated requests with zero
  failures. This is a connectivity/compatibility check, not a performance
  benchmark or capacity claim.
- [`week5_auth_security_check.txt`](../artifacts/week5_auth_security_check.txt):
  focused security verification and limitations.
- [`week5_week4_harness_compatibility.txt`](../artifacts/week5_week4_harness_compatibility.txt):
  defect-regression, temporary database-integrity, query-count, and benchmark
  harnesses run against the authenticated API.

The test process reported two existing Starlette/httpx deprecation warnings.
These warnings did not fail the tests. These are Phase 2 local results; current
Phase 3 validation evidence and the GitHub remote status are recorded in
[`WEEK5_CI_CD.md`](WEEK5_CI_CD.md) and its linked artifacts.
