# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| `main` branch | Yes |
| All others | No |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please send a private report by one of these methods:

- **GitHub Private Vulnerability Reporting** — use the *"Report a vulnerability"* button on the [Security tab](https://github.com/neshi-dev/xrwvm-fullstack_developer_capstone/security) of this repository.
- **Email** — contact the repository owner directly via the email address on their GitHub profile.

Please include:

1. A description of the vulnerability and its potential impact.
2. Step-by-step instructions to reproduce it.
3. Any proof-of-concept code (if applicable).
4. Your suggested fix (optional but appreciated).

You can expect an acknowledgement within **48 hours** and a status update within **7 days**.

---

## Security Practices in This Project

- **Secrets** are read from environment variables — never hardcoded.
  See [`.env.example`](.env.example) for all required variables.
- **`DEBUG` mode** is controlled by the `DJANGO_DEBUG` environment variable and must be set to `False` in production.
- **Request body size** is limited to 1 MB on the Express API to prevent DoS via large payloads.
- **URL parameters** are encoded with `urllib.parse.urlencode` / `quote` to prevent injection attacks.
- **HTTP security headers** (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `X-XSS-Protection`) are set by Django's security middleware.
- **CORS** on the Express API is restricted via the `ALLOWED_ORIGINS` environment variable in production.

### Additional hardening recommended for production deployments

- Set `SECURE_SSL_REDIRECT = True` and `SECURE_HSTS_SECONDS = 31536000`.
- Set `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`.
- Replace `ALLOWED_HOSTS = ['*']` with your actual domain name.
- Remove the `@csrf_exempt` decorators and configure the React frontend to send the `X-CSRFToken` header.
- Run behind a reverse proxy (e.g., Nginx) that enforces TLS.
