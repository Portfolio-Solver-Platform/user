import pytest
import requests
from tests.common.integration import api_url


@pytest.mark.integration
def test_login(client):
    response = requests.post(
        api_url("/login"), json={"username": "user", "password": "user"}
    )
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert "expires_in" in data
    assert "refresh_expires_in" in data
    assert "token_type" in data
