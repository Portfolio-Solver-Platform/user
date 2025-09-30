from src.config import Config


def api_path(path: str):
    assert path.startswith("/")
    return f"/{Config.Api.VERSION}{path}"
