def test_health_endpoint(client):
    """Test the health endpoint"""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_ready_endpoint(client):
    """Test the ready endpoint"""
    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ready"
