import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    """Test client"""
    with TestClient(app) as client:
        yield client
