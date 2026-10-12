import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request, g, render_template

app = Flask(__name__)
app.config["DATABASE"] = os.environ.get("DATABASE_PATH", str(Path("instance") / "aceest.db"))


def get_db():
    if "db" not in g:
        db_path = Path(app.config["DATABASE"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT ''
        );
    """)
    db.commit()

@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

with app.app_context():
    init_db()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/clients")
def list_clients():
    rows = get_db().execute("SELECT id, name, email FROM clients ORDER BY id").fetchall()
    return jsonify([dict(row) for row in rows]), 200

@app.post("/clients")
def create_client():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "")
    email = payload.get("email", "")
    if not isinstance(name, str) or not name.strip() or not isinstance(email, str) or not email.strip():
        return jsonify({"error": "name and email are required"}), 400
    try:
        db = get_db()
        cursor = db.execute("INSERT INTO clients (name, email) VALUES (?, ?)", (name.strip(), email.strip().lower()))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "email already exists"}), 409
    row = db.execute("SELECT id, name, email FROM clients WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

@app.get("/clients/<int:client_id>")
def get_client(client_id):
    row = get_db().execute("SELECT id, name, email FROM clients WHERE id = ?", (client_id,)).fetchone()
    if row is None:
        return jsonify({"error": "client not found"}), 404
    return jsonify(dict(row)), 200

@app.get("/programs")
def list_programs():
    rows = get_db().execute("SELECT id, name, description FROM programs ORDER BY id").fetchall()
    return jsonify([dict(row) for row in rows]), 200

@app.post("/programs")
def create_program():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "")
    description = payload.get("description", "")
    if not isinstance(name, str) or not name.strip() or not isinstance(description, str):
        return jsonify({"error": "name is required and description must be text"}), 400
    db = get_db()
    cursor = db.execute("INSERT INTO programs (name, description) VALUES (?, ?)", (name.strip(), description.strip()))
    db.commit()
    row = db.execute("SELECT id, name, description FROM programs WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
