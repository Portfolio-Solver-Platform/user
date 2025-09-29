from src.config import Config
import requests


def url(route: str):
    assert route.startswith("/"), "Route should start with '/'"
    return f"http://{Config.Keycloak.HOST}{route}"


def realm_url(realm: str, route: str):
    assert route.startswith("/"), "Route should start with '/'"
    url(f"/realms/{realm}{route}")


def oic_url(realm: str, route: str):
    assert route.startswith("/"), "Route should start with '/'"
    realm_url(realm, f"/protocol/openid-connect{route}")


def send_ready_request():
    return requests.get(url("/health/ready"), timeout=Config.Keycloak.Timeout.READINESS)


def send_login_request(username: str, password: str):
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
