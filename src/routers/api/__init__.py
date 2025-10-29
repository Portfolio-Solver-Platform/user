from fastapi import APIRouter
from . import well_known

router = APIRouter()

router.include_router(well_known.router, tags=["OpenID Connect"])
