from src.logging import logger
from fastapi import APIRouter
from src import keycloak
from urllib.parse import urlparse, urlunparse

router = APIRouter()


@router.get("/.well-known", summary="Get the OIDC .well-known")
def well_known():
    """Get the OpenID Connect .well-known"""
    response = keycloak.send_well_known_request()
    return response.json()


@router.get("/.well-known/intra", include_in_schema=False)
def well_known_intra():
    response = keycloak.send_well_known_request()
    response.raise_for_status()
    data = response.json()
    return update_well_known_for_intra(data)


KEYCLOAK_INTRA_URL = keycloak.url("/")


def update_well_known_for_intra(data: any):
    endpoints_to_modify = [
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

    return data
