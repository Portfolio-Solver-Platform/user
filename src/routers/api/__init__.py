from fastapi import APIRouter
from . import well_known, login

router = APIRouter()

router.include_router(well_known.router, tags=["OpenID Connect"])
router.include_router(login.router, tags=["OpenID Connect"])
