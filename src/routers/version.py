from fastapi import APIRouter
from src.config import Config
from pydantic import BaseModel

router = APIRouter()


class VersionResponse(BaseModel):
    service: str
    version: str
    api_version: str


@router.get("/version")
def version():
    return VersionResponse(
        service=Config.App.NAME,
        version=Config.App.VERSION,
        api_version=Config.Api.VERSION,
    )
