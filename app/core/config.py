from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "OUS API"
    API_V1_PREFIX: str = "/api/v1"
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
