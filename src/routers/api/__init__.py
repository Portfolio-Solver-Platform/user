from fastapi import APIRouter
from . import oidc

router = APIRouter()

router.include_router(oidc.router, tags=["OpenID Connect"])
