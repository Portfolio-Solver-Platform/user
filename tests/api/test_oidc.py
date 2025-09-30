import pytest
import requests
from tests.common.integration import api_url


@pytest.mark.integration
def test_well_known(client):
    response = requests.get(api_url("/.well-known"))
    assert response.status_code == 200
    data = response.json()

    assert "authorization_endpoint" in data
    assert "token_endpoint" in data
    assert "introspection_endpoint" in data
    assert "userinfo_endpoint" in data
    assert "end_session_endpoint" in data
    assert "jwks_uri" in data
