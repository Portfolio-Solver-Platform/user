from src.logging import logger
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


def remove_well_known_ports(data: any):
    endpoints_to_modify = [
        "issuer",
        "authorization_endpoint",
        "token_endpoint",
        "introspection_endpoint",
        "userinfo_endpoint",
        "end_session_endpoint",
        "jwks_uri",
    ]

    for endpoint in endpoints_to_modify:
        if endpoint not in data:
            logger.error(
                f"Failed to remove port from .well-known: {endpoint} not found in the .well-known data"
            )
            continue

        public_url = data[endpoint]
        parsed_url = urlparse(public_url)
        new_url_parts = parsed_url._replace(
            netloc=parsed_url.hostname,  # Remove the port
        )
        data[endpoint] = urlunparse(new_url_parts)


def update_well_known_for_internal(data: any):
    endpoints_to_modify = [
        "issuer",
        "token_endpoint",
        "introspection_endpoint",
        "userinfo_endpoint",
        "end_session_endpoint",
        "jwks_uri",
    ]

    for endpoint in endpoints_to_modify:
        if endpoint not in data:
            logger.error(
                f"Failed to replace public endpoint with intra-cluster endpoint: {endpoint} not found in the .well-known data"
            )
            continue

        public_url = data[endpoint]
        parsed_url = urlparse(public_url)
        new_url_parts = parsed_url._replace(
            netloc=urlparse(KEYCLOAK_INTRA_URL).netloc,
            scheme=urlparse(KEYCLOAK_INTRA_URL).scheme,
        )
        data[endpoint] = urlunparse(new_url_parts)
