from src.config import Config
import requests
from requests import Response


def url(route: str, is_management: bool = False) -> str:
    if not route.startswith("/"):
        raise ValueError("Route should start with '/'")
    port = Config.Keycloak.MANAGEMENT_PORT if is_management else Config.Keycloak.PORT
    return f"{Config.Keycloak.SCHEME}://{Config.Keycloak.HOST}:{port}{route}"


def realm_url(realm: str, route: str) -> str:
    if not route.startswith("/"):
        raise ValueError("Route should start with '/'")
    return url(f"/realms/{realm}{route}")


def send_ready_request() -> Response:
    return requests.get(
        url("/health/ready", is_management=True),
        timeout=Config.Keycloak.Timeout.READINESS,
    )


def send_well_known_request() -> Response:
    url = realm_url(Config.Keycloak.REALM, "/.well-known/openid-configuration")
    return requests.get(url, timeout=Config.Keycloak.Timeout.DEFAULT)
