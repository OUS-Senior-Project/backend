from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field(default="Backend", env="PROJECT_NAME")
    api_v1_prefix: str = Field(default="/api/v1", env="API_V1_PREFIX")
    database_url: str = Field(default="sqlite:///./local.db", env="DATABASE_URL")

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
