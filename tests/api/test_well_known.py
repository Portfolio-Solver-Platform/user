import pytest
import json
import copy
from urllib.parse import urlparse
from unittest.mock import Mock
from tests.common import api_path
from src.config import Config


@pytest.mark.integration
def test_well_known(client, monkeypatch):
    fake_response = mock_keycloak_well_known_response(monkeypatch)
    response = client.get(api_path("/.well-known/openid-configuration"))
    assert response.status_code == 200
    fake_response.json.assert_called_once()
    data = response.json()

    endpoints = [
        "issuer",
        "authorization_endpoint",
        "token_endpoint",
        "introspection_endpoint",
        "userinfo_endpoint",
        "end_session_endpoint",
        "jwks_uri",
    ]

    for endpoint in endpoints:
        assert endpoint in data
        parsed = urlparse(data[endpoint])
        assert parsed.port is None


def test_well_known_internal(client, monkeypatch):
    fake_response = mock_keycloak_well_known_response(monkeypatch)
    original_data = copy.deepcopy(fake_response.json.return_value)

    response = client.get(api_path("/internal/.well-known/openid-configuration"))
    assert response.status_code == 200
    fake_response.json.assert_called_once()

    intra_data = response.json()

    endpoints = [
        "introspection_endpoint",
        "userinfo_endpoint",
        "end_session_endpoint",
        "jwks_uri",
    ]

    for endpoint in endpoints:
        original_url = original_data[endpoint]
        intra_url = intra_data[endpoint]
        assert original_url != intra_url

        original_parsed_url = urlparse(original_url)
        intra_parsed_url = urlparse(intra_url)
        assert original_parsed_url.netloc != intra_parsed_url.netloc
        assert intra_parsed_url.scheme == Config.Keycloak.SCHEME
        assert intra_parsed_url.hostname == Config.Keycloak.HOST
        assert intra_parsed_url.port == Config.Keycloak.PORT


def mock_keycloak_well_known_response(monkeypatch) -> Mock:
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = get_mock_keycloak_well_known_json()

    monkeypatch.setattr(
        "src.keycloak.send_well_known_request",
        lambda: fake_response,
    )

    return fake_response


def get_mock_keycloak_well_known_json():
    with open("tests/api/sample_well_known_output.json", "r") as file:
        return json.load(file)
