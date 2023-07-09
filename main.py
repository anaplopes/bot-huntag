from logging.config import dictConfig

from migration import migrate
from src.database.connection import ConnectionDatabase
from src.usecases.v2.robot import Robot
from src.utils.logger import Logger

if __name__ == "__main__":
    # config log
    dictConfig(Logger().dict())

    # create tables
    ConnectionDatabase().create_data_model()

    # migrate
    migrate.data_filter()

    # run bot
    bot = Robot().execute()
