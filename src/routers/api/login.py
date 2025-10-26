from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.requests import Request
from src.auth import auth
from psp_auth import Token

router = APIRouter()


def security_scope_docs(scopes: list[str]):
    def f(request: Request):
        request.app.__openapi_extra__ = {"security": [{"HTTPBearer": scopes}]}

    return f


@router.get(
    "/test",
    # dependencies=[
    #     Security(auth.user_scopes(), scopes=["test", "admins"]),
    # ],
    # openapi_extra={"security": [{"HTTPBearer": ["users:testread"]}]},
    openapi_extra=auth.scope_docs(["admin"]),
)
async def auth_test(token: Annotated[Token, Depends(auth.token())]):
    return token
