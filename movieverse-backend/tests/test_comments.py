def test_post_comment(client):
    client.post("/api/register", json={
        "username": "testuser",
        "email": "test@comments.com",
        "password": "testpass"
    })
    login_response = client.post("/api/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    token = login_response.get_json()["access_token"]

    response = client.post("/api/comments", json={
        "imdb_id": "tt1234567",
        "comment_text": " This movie was lit!"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Comment added successfully"
