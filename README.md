# ACEest Fitness & Gym

Flask + SQLite API with a basic browser UI for managing clients and fitness programs, Pytest coverage, and Docker support.

## Local run

```bash
python -m pip install -r requirements.txt
python app.py
python -m pytest -v
```

## Docker

```bash
docker build -t aceest-fitness:local .
docker run --rm -p 5000:5000 -v aceest-data:/data aceest-fitness:local
```

Open `http://localhost:5000/` for the UI. The dashboard uses `GET/POST /clients` and `GET/POST /programs`; `/health` reports API status. The named volume preserves the SQLite database. Run tests locally with `python -m pytest -v`.
