from flask import Flask, jsonify, request

app = Flask(__name__)
clients = []
next_client_id = 1

@app.get("/")
def home():
    return jsonify({"message": "Welcome to ACEest Fitness & Gym"})

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/clients")
def list_clients():
    return jsonify(clients), 200

@app.post("/clients")
def create_client():
    global next_client_id
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip()
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400
    client = {"id": next_client_id, "name": name, "email": email}
    next_client_id += 1
    clients.append(client)
    return jsonify(client), 201

@app.get("/clients/<int:client_id>")
def get_client(client_id):
    client = next((item for item in clients if item["id"] == client_id), None)
    if client is None:
        return jsonify({"error": "client not found"}), 404
    return jsonify(client), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
