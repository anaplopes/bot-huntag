from mongoengine import connect
from mongoengine.errors import MongoEngineException

from src.settings import settings
from src.utils.conflog import logger


class ConnectionNoSQLDatabase:
    def __init__(self) -> None:
        self.__client = self.create_connect()

    def create_connect(self):
        try:
            logger.info("Connecting to database...")
            conn = connect(host=settings.NOSQL_DATABASE_HOST)
        except Exception as error:
            error_message = (
                f"An unexpected error occurred during connection: {error}"
            )
            logger.exception(error_message)
            raise MongoEngineException(error_message)
        else:
            logger.info("Connected to database.")
            return conn
