from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # Include routes
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app

app = create_app()
