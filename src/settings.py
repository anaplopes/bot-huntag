import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool | str = os.getenv("DEBUG", False)
    DATABASE_ENGINE: str = "postgresql+psycopg2"
    DATABASE_USER: str = os.getenv("DATABASE_USER", "pguser")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "pgpwd")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "huntag")

    class Config:
        case_sensitive = True


settings = Settings()
