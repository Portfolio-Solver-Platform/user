from fastapi import APIRouter
from urllib.parse import urlparse, urlunparse
from starlette.requests import Request
from src.auth import auth

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("login_auth")
    return await auth.client().authorize_redirect(request, redirect_uri)
    # If Keycloak says "Invalid parameter: redirect_uri", then
    # you need to make sure that the user service's URI is in the
    # valid redirect URIs for the client.


@router.get("/auth")
async def login_auth(request: Request):
    token = await auth.client().authorize_access_token(request)
    user = token["userinfo"]
    return dict(token)


@router.get("/test")
async def auth_test(request: Request):
    token = auth.get_token(request)
    return {"claims": token.claims, "header": token.header}
