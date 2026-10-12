# ACEest Fitness & Gym

Flask baseline plus client create/list/read endpoints. This stage stores clients in memory; restarting the app clears them.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Test with `GET /health`, `GET /clients`, and `POST /clients` with JSON such as `{"name":"Asha","email":"asha@example.com"}`.
