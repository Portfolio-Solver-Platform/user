from fastapi import APIRouter
from src import keycloak
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(request: LoginRequest):
    response = keycloak.send_login_request(request.username, request.password)
    return response.json()


@router.post("/userinfo")
def userinfo():
    raise NotImplementedError()


class LogoutRequest(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/logout")
def logout(request: LogoutRequest):
    raise NotImplementedError()


@router.post("/verify", summary="Verifies a token")
def verify():
    """Verifies that a token is still valid"""
    raise NotImplementedError()


@router.post("/revoke", summary="Revokes a token")
def revoke():
    """Revokes/invalidates a token"""
    raise NotImplementedError()


@router.get("/certs", summary="Returns the certificates for verifying a token")
def certs():
    raise NotImplementedError()
