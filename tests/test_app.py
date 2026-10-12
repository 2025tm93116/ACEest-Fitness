def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest Fitness" in response.data
    assert b"client-form" in response.data
    assert b"program-form" in response.data

def test_create_and_list_client(client):
    response = client.post("/clients", json={"name": "Asha", "email": "asha@example.com"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Asha"
    listing = client.get("/clients")
    assert listing.status_code == 200
    assert len(listing.get_json()) == 1

def test_client_requires_name_and_email(client):
    response = client.post("/clients", json={"name": "Asha"})
    assert response.status_code == 400

def test_duplicate_email_is_rejected(client):
    payload = {"name": "Asha", "email": "asha@example.com"}
    assert client.post("/clients", json=payload).status_code == 201
    assert client.post("/clients", json=payload).status_code == 409

def test_missing_client_returns_404(client):
    assert client.get("/clients/999").status_code == 404

def test_create_and_list_program(client):
    response = client.post("/programs", json={"name": "Strength", "description": "Three days"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Strength"
    assert len(client.get("/programs").get_json()) == 1

def test_program_requires_name(client):
    assert client.post("/programs", json={"description": "No name"}).status_code == 400
