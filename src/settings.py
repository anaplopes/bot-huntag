import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_ENGINE = "postgresql+psycopg2"
    DATABASE_USER = os.getenv("DATABASE_USER", "pguser")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "pgpwd")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "huntag")

    class Config:
        case_sensitive = True


settings = Settings()
