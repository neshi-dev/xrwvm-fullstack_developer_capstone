# Contributing to Best Cars Dealership

Thank you for your interest in contributing! This document explains how to get the project running locally and how to submit changes.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Running Tests](#running-tests)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Bugs](#reporting-bugs)

---

## Code of Conduct

Be respectful and constructive. Harassment of any kind is not tolerated.

---

## Getting Started

1. **Fork** the repository and clone your fork:

   ```bash
   git clone https://github.com/<your-username>/xrwvm-fullstack_developer_capstone.git
   cd xrwvm-fullstack_developer_capstone
   ```

2. **Configure environment variables** — copy the template and fill in your values:

   ```bash
   cp .env.example server/.env
   ```

3. **Follow the setup steps** in the [README](README.md#getting-started).

---

## Development Workflow

```bash
# Create a branch for your change
git checkout -b feature/short-description

# Make your changes, then commit
git add <files>
git commit -m "feat: short description of what was changed and why"

# Push and open a pull request
git push origin feature/short-description
```

### Commit message format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) style:

| Prefix | When to use |
|--------|-------------|
| `feat:` | A new feature |
| `fix:` | A bug fix |
| `docs:` | Documentation only |
| `test:` | Adding or fixing tests |
| `refactor:` | Code change that neither fixes a bug nor adds a feature |
| `chore:` | Build process or tooling changes |

---

## Coding Standards

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/). The CI pipeline enforces this with `flake8`.
- Keep lines to a maximum of **79 characters**.
- Use descriptive variable names.
- Write docstrings for public functions and classes.

### JavaScript

- Follow the `jshint` config in `package.json`.
- Use `const`/`let` — avoid `var`.
- Keep functions small and single-purpose.

### React

- One component per file.
- Use functional components and hooks.
- Keep component state minimal — prefer lifting state up.

---

## Running Tests

Run the full test suite before submitting a PR:

```bash
# Django unit tests
cd server
python manage.py test djangoapp --verbosity=2

# Flask microservice tests
cd server/djangoapp/microservices
pytest test_app.py -v

# React tests
cd server/frontend
npm test -- --watchAll=false
```

All tests must pass and linting must produce no errors.

---

## Submitting a Pull Request

1. Ensure all tests pass and linting is clean.
2. Update the `README.md` if your change affects setup, configuration, or usage.
3. Open a pull request against the `main` branch with:
   - A clear title (use the commit message format above).
   - A description of *what* changed and *why*.
   - Any relevant issue numbers (e.g., `Closes #42`).

A maintainer will review your PR within a few days.

---

## Reporting Bugs

Please [open an issue](https://github.com/neshi-dev/xrwvm-fullstack_developer_capstone/issues/new) with:

- A short, descriptive title.
- Steps to reproduce the problem.
- Expected vs. actual behaviour.
- Your OS, Python version, and Node.js version.

For security vulnerabilities, please follow the [Security Policy](SECURITY.md) instead of opening a public issue.
