from src.config import Config
from tests.common import api_path
from tests.conftest import TestConfig


def url(path: str):
    assert path.startswith("/")
    return f"{TestConfig.Gateway.BASE_URL}{Config.Api.ROOT_PATH}{path}"


def api_url(path: str):
    assert path.startswith("/")
    return url(api_path(path))
