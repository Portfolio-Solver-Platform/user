from src.config import Config
import requests
from requests import Response


def url(route: str, is_management: bool = False) -> str:
    assert route.startswith("/"), "Route should start with '/'"
    port = Config.Keycloak.MANAGEMENT_PORT if is_management else Config.Keycloak.PORT
    return f"http://{Config.Keycloak.HOST}:{port}{route}"


def realm_url(realm: str, route: str) -> str:
    assert route.startswith("/"), "Route should start with '/'"
    return url(f"/realms/{realm}{route}")


def oic_url(realm: str, route: str) -> str:
    assert route.startswith("/"), "Route should start with '/'"
    return realm_url(realm, f"/protocol/openid-connect{route}")


def send_ready_request() -> Response:
    return requests.get(
        url("/health/ready", is_management=True),
        timeout=Config.Keycloak.Timeout.READINESS,
    )


def send_login_request(username: str, password: str) -> Response:
    url = oic_url(Config.Keycloak.REALM, "/token")
    data = {
        "client_id": Config.Keycloak.CLIENT_ID,
        "client_secret": Config.Keycloak.CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    return requests.post(url, data=data, timeout=Config.Keycloak.Timeout.DEFAULT)


def send_logout_request():
    pass


def send_userinfo_request():
    pass
