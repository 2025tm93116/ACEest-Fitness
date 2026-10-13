# ACEest Fitness & Gym — DevOps Assignment

A small Flask REST API with SQLite persistence for clients and fitness programs, automated tests, Docker packaging, GitHub Actions, and a Jenkins validation pipeline.

## Local setup

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Check `GET /health`. Create a client with `POST /clients` and JSON `{"name":"Asha","email":"asha@example.com"}`. Create a program with `POST /programs` and JSON `{"name":"Strength","description":"Three sessions per week"}`.

## Tests and quality checks

```bash
python -m pytest -v
python -m compileall -q app.py tests
ruff check app.py tests
```

## Docker

```bash
docker build -t aceest-fitness:local .
docker run --rm -p 5000:5000 -v aceest-data:/data aceest-fitness:local
```

## GitHub Actions

`.github/workflows/main.yml` runs on every push and pull request. It has independent jobs for syntax/lint validation, Docker image assembly, and Pytest validation. The Pytest job installs the project dependencies and runs the test suite. The Docker job proves the image can be assembled.

## Jenkins

The included `Jenkinsfile` checks out the repository, creates a clean Python virtual environment, installs requirements, compiles and lints the code, runs Pytest, and builds the Docker image. Configure a Pipeline job to use this repository and ensure the Jenkins agent has Python 3, Git, and Docker CLI/daemon access. On a Windows-only Jenkins agent, adapt the shell steps to Windows batch/PowerShell commands.

## Database

SQLite is created automatically. `DATABASE_PATH` can point to a custom database file. Docker defaults to `/data/aceest.db`; mount a volume at `/data` to preserve data between container runs.

## Scope

This is an educational DevOps assignment starter, not a production-ready service. It intentionally focuses on a small API and delivery pipeline rather than authentication or deployment to a public environment.
