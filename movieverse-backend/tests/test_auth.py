def test_register_user(client):
    response = client.post("/api/register", json={
        "username": "tester",
        "email": "tester@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User created successfully"

def test_login_user(client):

    client.post("/api/register", json={
        "username": "tester",
        "email": "tester@example.com",
        "password": "password123"
    })

    response = client.post("/api/login", json={
        "username": "tester",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "access_token" in response.get_json()
