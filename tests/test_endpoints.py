def test_shorten_returns_201(client):
    response = client.post("/shorten", json={"url": "https://example.com/long"})
    assert response.status_code == 201
    data = response.json()
    assert "code" in data
    assert "short_url" in data
    assert len(data["code"]) == 8
    assert data["short_url"].endswith(data["code"])


def test_shorten_invalid_url(client):
    response = client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 422


def test_shorten_missing_url(client):
    response = client.post("/shorten", json={})
    assert response.status_code == 422


def test_redirect_existing_code(client):
    resp = client.post("/shorten", json={"url": "https://example.com/target"})
    code = resp.json()["code"]

    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com/target"


def test_redirect_nonexistent_code(client):
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 404


def test_stats_existing_code(client):
    resp = client.post("/shorten", json={"url": "https://example.com/stats"})
    code = resp.json()["code"]

    response = client.get(f"/stats/{code}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == code
    assert data["redirect_count"] == 0


def test_stats_nonexistent_code(client):
    response = client.get("/stats/nonexistent")
    assert response.status_code == 404


def test_stats_increments_after_redirect(client):
    resp = client.post("/shorten", json={"url": "https://example.com/count"})
    code = resp.json()["code"]

    # Redirect twice
    client.get(f"/{code}", follow_redirects=False)
    client.get(f"/{code}", follow_redirects=False)

    response = client.get(f"/stats/{code}")
    assert response.status_code == 200
    assert response.json()["redirect_count"] == 2
