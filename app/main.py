from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.project_name)

    # Include routes
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
