# ACEest Fitness & Gym

Flask REST API with SQLite persistence for clients and fitness programs. The database is created automatically on startup. Set `DATABASE_PATH` to change its location.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Example client request: `POST /clients` with `{"name":"Asha","email":"asha@example.com"}`. Programs use `POST /programs` with `{"name":"Strength","description":"Three sessions per week"}`.
