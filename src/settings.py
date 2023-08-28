import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    TYPE_DB: str = "NoSQL"

    HUNTAG_URL: str = os.getenv("HUNTAG_URL")
    HUNTAG_EMAIL: str = os.getenv("HUNTAG_EMAIL")
    HUNTAG_PASSWORD: str = os.getenv("HUNTAG_PASSWORD")

    PATH_DIR_SOURCE: str = os.getenv("PATH_DIR_SOURCE")
    PATH_DIR_TARGET: str = os.getenv("PATH_DIR_TARGET")

    SQL_DATABASE_ENGINE: str = "postgresql+psycopg2"
    SQL_DATABASE_USER: str = os.getenv("SQL_DATABASE_USER", "pguser")
    SQL_DATABASE_PASSWORD: str = os.getenv("SQL_DATABASE_PASSWORD", "pgpwd")
    SQL_DATABASE_HOST: str = os.getenv("SQL_DATABASE_HOST", "localhost")
    SQL_DATABASE_PORT: str = os.getenv("SQL_DATABASE_PORT", "5432")
    SQL_DATABASE_NAME: str = os.getenv("SQL_DATABASE_NAME", "huntag")

    NOSQL_DATABASE_HOST: str = os.getenv(
        "NOSQL_DATABASE_HOST", "mongodb://127.0.0.1:27017/huntag"
    )

    AZURE_APP_CLIENT_ID: str = os.getenv("AZURE_APP_CLIENT_ID")
    AZURE_DIRETORY_TENANT_ID: str = os.getenv("AZURE_DIRETORY_TENANT_ID")
    AZURE_APP_CLIENT_SECRET: str = os.getenv("AZURE_APP_CLIENT_SECRET")

    class Config:
        case_sensitive = True


settings = Settings()
