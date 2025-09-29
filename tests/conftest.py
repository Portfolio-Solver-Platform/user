import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Test client"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def config():
    """Test configuration"""
    yield TestConfig()


class TestConfig:
    class Gateway:
        BASE_URL = "http://local"
