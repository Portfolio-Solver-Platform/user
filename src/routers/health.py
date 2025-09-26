from fastapi import APIRouter
from src.config import Config
import requests
from requests.exceptions import ConnectionError
from pydantic import BaseModel
from enum import Enum

router = APIRouter()


class HealthStatus(str, Enum):
    healthy = "ok"


class HealthResponse(BaseModel):
    status: HealthStatus


@router.get(
    "/healthz", response_model=HealthResponse, summary="Get the health of the service"
)
def healthz():
    """
    Get the health of the service.
    """
    return HealthResponse(status=HealthStatus.healthy)


class ReadyStatus(str, Enum):
    ready = "ready"
    not_ready = "not_ready"


class ReadyResponse(BaseModel):
    status: ReadyStatus


@router.get(
    "/readyz", response_model=ReadyResponse, summary="Get whether the service is ready"
)
def readyz():
    """
    Get whether the service is ready to serve requests
    """
    if is_keycloak_ready():
        status = ReadyStatus.ready
    else:
        status = ReadyStatus.not_ready
    return ReadyResponse(status=status)


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
