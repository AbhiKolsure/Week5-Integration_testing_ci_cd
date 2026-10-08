# Final Authentication and Swagger/API Root-Cause Notes

## Findings

No application-code defect was found for the reported `401`, `422`, or `409`
responses. The current registration and authentication behavior matches the
request schemas and route security configuration.

- `POST /auth/register` requires `email` and `password`. The email must be
  valid, the password must be 8–128 characters, and additional fields such as
  `username` are rejected. Live requests with an invalid email, a username-only
  payload, or a short password each returned `422 Unprocessable Entity`.
- Registering the same normalized email twice returned `409 Conflict`, as
  expected for an existing account.
- Invalid login credentials returned `401 Unauthorized`.
- All task routes use HTTP Bearer authentication. Missing or malformed tokens
  returned `401`. A valid access token returned `200` for `GET /tasks`.
- The Swagger UI `Authorize` value must contain the raw `access_token` from the
  login response, not the text `Bearer ` followed by the token. The raw token
  successfully authorized a task request; entering a value with the extra
  prefix produced a `401` because Swagger adds the Bearer scheme itself.

The exact value entered during the original failed request was not available,
so the extra-prefix behavior is a verified explanation for that common Swagger
401 cause, not a claim that it was necessarily the user's exact input.

## Verified Swagger sequence

1. Register with JSON containing a valid `email` and an 8–128 character
   `password`.
2. Log in with those same credentials.
3. Copy only the response's `access_token` value.
4. In Swagger's **Authorize** dialog, paste that raw value into **Value**.
5. Execute a protected `/tasks` request. The UI adds the Bearer scheme.

The browser-backed Swagger run returned `201` for registration, `200` for
login, `201` for authenticated task creation, and `204` for task deletion.
The response did not include a password or password hash. Missing the token,
using malformed token text, and pasting an already-prefixed token were also
verified to return `401` against the live API.

## Evidence and cleanup

The live HTTP observations are recorded in
[`final_auth_live_validation.txt`](./final_auth_live_validation.txt), and the
browser-specific observations are recorded in
[`final_browser_api_validation.txt`](./final_browser_api_validation.txt).
The new automated regression coverage is in
[`test_auth_integration.py`](../tests/test_auth_integration.py): it checks the
OpenAPI security declaration and a unique-user authentication/task lifecycle.

Temporary test users and tasks were removed after live validation. No
passwords, access tokens, or signing keys were written to the evidence files.
No application source, authentication behavior, or Week 4 benchmark/load
evidence was changed.
