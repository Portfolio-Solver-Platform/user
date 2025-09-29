import pytest
import requests
from tests.common.integration import api_url


@pytest.mark.integration
def test_login(client):
    response = requests.post(
        api_url("/login"), json={"username": "user", "password": "user"}
    )
    assert response.status_code == 200
    print(response.json())
    assert False
    pass
