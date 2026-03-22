# Best Cars Dealership — Full Stack Web Application

![CI](https://github.com/neshi-dev/xrwvm-fullstack_developer_capstone/actions/workflows/main.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Node.js](https://img.shields.io/badge/Node.js-Express-339933?logo=node.js)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

A full-stack car dealership review platform built as the capstone project for the **IBM Full Stack Software Developer Professional Certificate**. Users can browse dealerships across the United States, read customer reviews with AI-powered sentiment analysis, and post their own reviews after logging in.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Run with Docker](#run-with-docker)
  - [Run Locally](#run-locally)
- [API Reference](#api-reference)
- [Running Tests](#running-tests)
- [CI/CD](#cicd)
- [Security](#security)
- [License](#license)

---

## Features

- **Browse Dealerships** — View all dealerships or filter by U.S. state
- **Dealer Reviews** — Read customer reviews enriched with sentiment scores (Positive / Neutral / Negative)
- **AI Sentiment Analysis** — A dedicated Flask microservice uses NLTK's VADER model to analyse review text in real time
- **User Authentication** — Register, log in, and log out with Django's built-in auth system
- **Post Reviews** — Authenticated users can submit reviews including car make, model, year, and purchase date
- **Responsive UI** — Single-page React application styled with Bootstrap
- **Containerised Deployment** — Each service ships as a Docker container; Kubernetes manifests included

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Browser (React SPA)                    │
└────────────────────────────┬─────────────────────────────────┘
                             │ HTTP
┌────────────────────────────▼─────────────────────────────────┐
│               Django (Python 3.12 · Gunicorn)                 │
│   Serves the React build, handles auth & proxies API calls    │
└──────┬──────────────────────────────────────┬────────────────┘
       │ REST                                  │ REST
┌──────▼──────────────┐            ┌──────────▼──────────────┐
│  Node.js / Express  │            │  Flask Sentiment Service │
│  Dealerships &      │            │  NLTK VADER analysis     │
│  Reviews data store │            │  /analyze/<text>         │
└─────────────────────┘            └─────────────────────────┘
```

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React 18, React Router 6, Bootstrap | SPA served by Django |
| Backend API | Django 4, Django REST Framework | Auth, proxy, business logic |
| Dealership DB | Node.js, Express | In-memory JSON store for dealers & reviews |
| Sentiment Service | Flask, NLTK VADER | Classifies review text as positive/neutral/negative |
| Container | Docker, Docker Compose | Local development orchestration |
| Orchestration | Kubernetes | Production deployment manifests |

---

## Tech Stack

**Backend**
- Python 3.12, Django 4, Gunicorn
- Node.js, Express, CORS
- Flask, NLTK (VADER sentiment analyser)

**Frontend**
- React 18, React Router 6
- Bootstrap 4

**DevOps**
- Docker & Docker Compose
- Kubernetes
- GitHub Actions (lint + test CI)

---

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── main.yml          # CI: lint + test pipeline
├── server/
│   ├── djangoproj/           # Django project settings & root URLs
│   ├── djangoapp/            # Main Django application
│   │   ├── models.py         # CarMake, CarModel models
│   │   ├── views.py          # Auth, dealership & review endpoints
│   │   ├── restapis.py       # HTTP client for microservices
│   │   ├── urls.py           # URL routing
│   │   ├── tests.py          # Django unit tests
│   │   └── microservices/
│   │       ├── app.py        # Flask sentiment analyser
│   │       └── test_app.py   # Flask unit tests
│   ├── database/
│   │   ├── app.js            # Express dealership/review API
│   │   └── data/             # Seed JSON files
│   ├── frontend/             # React SPA (Create React App)
│   ├── Dockerfile            # Django service image
│   └── requirements.txt      # Python dependencies (pinned)
├── .env.example              # Environment variable template
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
└── README.md
```

---

## Getting Started

### Prerequisites

| Tool | Minimum Version |
|------|----------------|
| Python | 3.12 |
| Node.js | 18 LTS |
| npm | 9 |
| Docker | 24 |
| Docker Compose | 2.20 |

### Environment Variables

Copy the template and fill in your values:

```bash
cp .env.example server/.env
```

See [`.env.example`](.env.example) for all available variables and their descriptions.

### Run with Docker

The fastest way to start all three services together:

```bash
# 1. Start the Node.js dealership/review API
cd server/database
docker compose up -d

# 2. Start the Flask sentiment service
cd server/djangoapp/microservices
docker build -t sentiment-analyzer .
docker run -d -p 5050:5050 sentiment-analyzer

# 3. Start Django + React
cd server
docker build -t bestcars-django .
docker run -d -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-secret-key \
  -e DJANGO_DEBUG=False \
  -e backend_url=http://host.docker.internal:3030 \
  -e sentiment_analyzer_url=http://host.docker.internal:5050/ \
  bestcars-django
```

Open [http://localhost:8000](http://localhost:8000).

### Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/neshi-dev/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone
```

**2. Python backend**

```bash
cd server
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env   # then edit .env with your values
python manage.py migrate
python manage.py runserver
```

**3. Node.js dealership API** (new terminal)

```bash
cd server/database
npm install
node app.js
```

**4. Flask sentiment service** (new terminal)

```bash
cd server/djangoapp/microservices
pip install flask nltk
python -c "import nltk; nltk.download('vader_lexicon')"
python app.py
```

**5. React frontend** (new terminal — development mode)

```bash
cd server/frontend
npm install
npm start
```

The React dev server proxies API calls to Django at `http://localhost:8000`.

---

## API Reference

All Django endpoints are prefixed with `/djangoapp/`.

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/djangoapp/register` | None | Create a new user account |
| `POST` | `/djangoapp/login` | None | Log in and start a session |
| `GET` | `/djangoapp/logout` | Session | End the current session |

### Dealerships

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/djangoapp/get_dealers/` | None | List all dealerships |
| `GET` | `/djangoapp/get_dealers/<state>/` | None | Filter dealerships by U.S. state code |
| `GET` | `/djangoapp/dealer/<id>/` | None | Get a single dealer by ID |

### Reviews

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/djangoapp/reviews/dealer/<id>/` | None | Get reviews for a dealer (includes sentiment) |
| `POST` | `/djangoapp/add_review/` | Session | Submit a new review |

### Cars

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/djangoapp/get_cars` | None | List all car makes and models |

**Example — register a user:**

```bash
curl -X POST http://localhost:8000/djangoapp/register \
  -H "Content-Type: application/json" \
  -d '{"userName":"jane","password":"S3cur3Pass!","firstName":"Jane","lastName":"Doe","email":"jane@example.com"}'
```

**Example — fetch dealers in Texas:**

```bash
curl http://localhost:8000/djangoapp/get_dealers/TX/
```

---

## Running Tests

**Django:**

```bash
cd server
python manage.py test djangoapp
```

**Flask sentiment service:**

```bash
cd server/djangoapp/microservices
python -m pytest test_app.py -v
```

**React (Jest):**

```bash
cd server/frontend
npm test -- --watchAll=false
```

---

## CI/CD

Every push and pull request to `main` / `master` triggers the GitHub Actions pipeline defined in [`.github/workflows/main.yml`](.github/workflows/main.yml):

| Job | What it does |
|-----|-------------|
| `lint_python` | Runs `flake8` across all Python source files |
| `lint_js` | Runs `jshint` on all Express server JavaScript |
| `test_django` | Runs Django unit tests with `manage.py test` |
| `test_flask` | Runs Flask microservice tests with `pytest` |

---

## Security

Security issues and vulnerability reports are handled according to our [Security Policy](SECURITY.md).

Key practices in this project:

- Secrets are read from **environment variables** — never committed to source control
- `DEBUG` mode is controlled per-environment via `DJANGO_DEBUG`
- Request bodies are limited to **1 MB** to prevent DoS
- Query parameters are **URL-encoded** to prevent injection attacks
- `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, and `X-XSS-Protection` headers are set

---

## License

Distributed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for details.

> Built as part of the [IBM Full Stack Software Developer Professional Certificate](https://www.coursera.org/professional-certificates/ibm-full-stack-cloud-developer) on Coursera.
