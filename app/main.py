from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router
from app.db.database import Base, engine

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app

app = create_app()
