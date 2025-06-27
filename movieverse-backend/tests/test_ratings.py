def test_rate_movie(client):
    
    client.post("/api/register", json={
        "username": "rateuser",
        "email": "rate@test.com",
        "password": "rate123"
    })
    login_response = client.post("/api/login", json={
        "username": "rateuser",
        "password": "rate123"
    })
    token = login_response.get_json()["access_token"]

    response = client.post("/api/ratings", json={
        "imdb_id": "tt1010101",
        "rating_value": 9
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Rating added"
