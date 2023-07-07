from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from src.model.base import Base
from src.settings import settings
from src.utils.logger import logger


class ConnectionDatabase:
    def __init__(self) -> None:
        self.__engine = self.create_connect()

    def __str_url(self) -> str:
        engine = settings.DATABASE_ENGINE
        user = settings.DATABASE_USER
        password = settings.DATABASE_PASSWORD
        host = settings.DATABASE_HOST
        port = settings.DATABASE_PORT
        name = settings.DATABASE_NAME
        return f"{engine}://{user}:{password}@{host}:{port}/{name}"

    def create_connect(self) -> Engine:
        try:
            logger.info("Connecting to database...")
            conn = create_engine(url=self.__str_url(), echo=settings.DEBUG)
        except Exception as error:
            e = str(error)
            logger.exception(f"Engine connection error: {e}")
            raise SQLAlchemyError(f"Engine connection error: {e}")
        else:
            logger.info("Connected to database.")
            return conn

    def __session_factory(self) -> Session:
        Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.__engine
        )
        return Session()

    def create_data_model(self) -> None:
        try:
            logger.info("Creating tables...")
            Base.metadata.create_all(bind=self.__engine)
        except Exception as error:
            e = str(error)
            logger.exception(f"Create tables error: {e}")
            raise SQLAlchemyError(f"Create tables error: {e}")
        finally:
            self.__engine.dispose()

    def get_session(self):
        try:
            session = self.__session_factory()
            return session
        except Exception as error:
            e = str(error)
            logger.exception(f"Session rollback: {e}")
            session.rollback()
            raise SQLAlchemyError(f"Session rollback: {e}")
        finally:
            session.close()
            self.__engine.dispose()
