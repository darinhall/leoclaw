from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from shared.utils import get_logger

from .config import get_settings
from .executor import Executor
from .routes import client_router, tasks_router

logger = get_logger(__name__)
settings = get_settings()

# Module-level singleton — routes import this directly
executor = Executor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LeoClaw Orchestrator starting up (v%s)", "0.1.0")
    yield
    logger.info("Orchestrator shutting down")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(tasks_router)
app.include_router(client_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "orchestrator"}
