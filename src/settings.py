import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool | str = os.getenv("DEBUG", False)

    HUNTAG_URL: str = os.getenv("HUNTAG_URL")
    HUNTAG_EMAIL: str = os.getenv("HUNTAG_EMAIL")
    HUNTAG_PASSWORD: str = os.getenv("HUNTAG_PASSWORD")

    PATH_DIR_DOWNLOAD: str = os.getenv("PATH_DIR_DOWNLOAD")
    PATH_DIR_TARGET: str = os.getenv("PATH_DIR_TARGET")

    DATABASE_ENGINE: str = "postgresql+psycopg2"
    DATABASE_USER: str = os.getenv("DATABASE_USER", "pguser")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "pgpwd")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "huntag")

    AZURE_APP_CLIENT_ID: str = os.getenv("AZURE_APP_CLIENT_ID")
    AZURE_DIRETORY_TENANT_ID: str = os.getenv("AZURE_DIRETORY_TENANT_ID")
    AZURE_APP_CLIENT_SECRET: str = os.getenv("AZURE_APP_CLIENT_SECRET")

    class Config:
        case_sensitive = True


settings = Settings()
