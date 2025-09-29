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
