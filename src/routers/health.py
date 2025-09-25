from fastapi import APIRouter
from src.config import Config
import requests
from requests.exceptions import ConnectionError
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str


@router.get("/healthz", response_model=HealthResponse)
def healthz():
    return HealthResponse(status="ok")


class ReadyResponse(BaseModel):
    status: str


@router.get("/readyz", response_model=ReadyResponse)
def readyz():
    if is_keycloak_ready():
        status = "ready"
    else:
        status = "not ready"
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
