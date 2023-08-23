import logging

from pydantic import BaseModel


class ConfLog(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "bot_huntag"
    LOG_FORMAT: str = (
        "%(levelprefix)s %(asctime)s| %(module)s line %(lineno)d | %(message)s"
    )
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


logger = logging.getLogger(ConfLog().LOGGER_NAME)
