import types


def test_health_endpoint(client):
    """Test the health endpoint"""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_ready_endpoint(client, monkeypatch):
    """Test the ready endpoint"""
    assume_keycloak_ready_state(monkeypatch, True)

    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ready"


def assume_keycloak_ready_state(monkeypatch, is_ready: bool):
    def fake_get_keycloak_ready_response():
        return types.SimpleNamespace(
            json=lambda: {"status": "UP" if is_ready else "DOWN"}
        )

    monkeypatch.setattr(
        "src.blueprints.health.try_get_keycloak_ready_response",
        fake_get_keycloak_ready_response,
    )
