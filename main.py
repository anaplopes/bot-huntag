from src.database.connection import ConnectionDatabase
from src.robot.v2.robot import Robot
from logging.config import dictConfig
from src.utils.logger import Logger
from src.data import migrate


if __name__ == "__main__":

    # config log
    dictConfig(Logger().dict())

    # create tables
    ConnectionDatabase().create_data_model()

    # migrate
    migrate.data_filter()

    # run bot
    bot = Robot().execute()
