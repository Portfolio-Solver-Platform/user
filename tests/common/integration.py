from src.config import Config
from tests.conftest import TestConfig


def url(path: str):
    assert path.startswith("/")
    return f"{TestConfig.Gateway.BASE_URL}{Config.Api.ROOT_PATH}{path}"


def api_url(path: str):
    assert path.startswith("/")
    return url(f"/{Config.Api.VERSION}{path}")
