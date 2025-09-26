from typing import Literal
from fastapi import APIRouter, HTTPException
from src.config import Config
import requests
from requests.exceptions import ConnectionError
from pydantic import BaseModel
from enum import Enum

router = APIRouter()


class HealthResponse(BaseModel):
    status: Literal["ok"]


@router.get(
    "/healthz",
    response_model=HealthResponse,
    summary="Get the health of the service",
    include_in_schema=False,
)
def healthz():
    """
    Get the health of the service.
    """
    return HealthResponse(status="ok")


class ReadyResponse(BaseModel):
    status: Literal["ready"]


@router.get(
    "/readyz",
    response_model=ReadyResponse,
    summary="Get whether the service is ready",
    include_in_schema=False,
)
def readyz():
    """
    Get whether the service is ready to serve requests
    """
    if not is_keycloak_ready():
        raise HTTPException(status_code=503, detail="Service is not ready")

    return ReadyResponse(status="ready")


def is_keycloak_ready() -> bool:
    response = try_get_keycloak_ready_response()
    if response is None:
        return False

    data = response.json()
    return data["status"] == "UP"


def try_get_keycloak_ready_response() -> requests.Response | None:
    url = f"http://{Config.Keycloak.HOST}/health/ready"
    try:
        return requests.get(url, timeout=Config.Keycloak.Timeout.READINESS)
    except ConnectionError:
        return None
