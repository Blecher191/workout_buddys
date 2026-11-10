import logging

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import get_settings


class HealthResponse(BaseModel):
    status: str
    environment: str


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)

    app = FastAPI(
        title="Workout Buddys API",
        version="0.1.0",
        # Interactive docs are a development aid; do not expose them in production.
        docs_url=None if settings.app_env == "production" else "/docs",
        redoc_url=None,
        openapi_url=None if settings.app_env == "production" else "/openapi.json",
    )

    @app.get("/health", response_model=HealthResponse, tags=["ops"])
    def health() -> HealthResponse:
        """Liveness check. Does not touch any external service."""
        return HealthResponse(status="ok", environment=settings.app_env)

    return app


app = create_app()
