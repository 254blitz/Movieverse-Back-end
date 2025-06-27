def test_add_favorite(client):
    client.post("/api/register", json={
        "username": "faveuser",
        "email": "fave@test.com",
        "password": "fav123"
    })
    login_response = client.post("/api/login", json={
        "username": "faveuser",
        "password": "fav123"
    })
    token = login_response.get_json()["access_token"]

    response = client.post("/api/favorites", json={
        "movie_id": "tt8765432",
        "title": "The GOAT Movie",
        "poster_url": "https://image.tmdb.org/t/p/thegoat.jpg"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Favorite added"
