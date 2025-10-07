from src.logging import logger
from typing import Callable
from fastapi import APIRouter
from src import keycloak
from urllib.parse import urlparse, urlunparse

router = APIRouter()


@router.get("/.well-known/openid-configuration", summary="Get the OIDC .well-known")
def well_known():
    """
    Get the OpenID Connect .well-known.

    For the endpoints in the response, only the following are officially supported:
    - issuer
    - authorization_endpoint
    - token_endpoint
    - introspection_endpoint
    - userinfo_endpoint
    - end_session_endpoint
    - jwks_uri
    """
    response = keycloak.send_well_known_request()
    response.raise_for_status()
    data = response.json()
    remove_well_known_ports(data)
    return data


@router.get("/.well-known/openid-configuration/internal", include_in_schema=False)
def well_known_intra():
    response = keycloak.send_well_known_request()
    response.raise_for_status()
    data = response.json()
    update_well_known_for_internal(data)
    return data


KEYCLOAK_INTRA_URL = keycloak.url("/")


def map_each_endpoint(data: dict, f: Callable[[str], str]):
    for key, value in data.items():
        if isinstance(value, str) and (
            key.endswith("_endpoint")
            or key == "issuer"
            or key == "jwks_uri"
            or key == "check_session_iframe"
        ):
            data[key] = f(value)

        if isinstance(value, dict):
            map_each_endpoint(data[key], f)


def remove_well_known_ports(data: dict):
    map_each_endpoint(data, remove_port)


def remove_port(value: str) -> str:
    parsed_url = urlparse(value)
    new_url_parts = parsed_url._replace(
        netloc=parsed_url.hostname,  # Remove the port
    )
    return urlunparse(new_url_parts)


def update_well_known_for_internal(data: dict):
    auth_endpoint = remove_port(data["authorization_endpoint"])
    issuer = remove_port(data["issuer"])

    map_each_endpoint(data, replace_host_with_internal_keycloak)

    data["authorization_endpoint"] = auth_endpoint
    data["issuer"] = issuer


def replace_host_with_internal_keycloak(url: str) -> str:
    parsed_url = urlparse(url)
    new_url_parts = parsed_url._replace(
        netloc=urlparse(KEYCLOAK_INTRA_URL).netloc,
        scheme=urlparse(KEYCLOAK_INTRA_URL).scheme,
    )
    return urlunparse(new_url_parts)
