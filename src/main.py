from fastapi import FastAPI
from .routers import health, version
import prometheus_fastapi_instrumentator

app = FastAPI()

app.include_router(health.router, tags=["Health", "Info"])
app.include_router(version.router, tags=["Info"])

# Monitoring
prometheus_fastapi_instrumentator.Instrumentator().instrument(app).expose(app)
