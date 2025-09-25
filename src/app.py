from fastapi import FastAPI
from .config import Config
from .routers import health, version

app = FastAPI()

app.include_router(health.router)
app.include_router(version.router)
