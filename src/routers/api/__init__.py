from fastapi import APIRouter
from . import route

router = APIRouter()

router.include_router(route.router)
