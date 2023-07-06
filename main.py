from src.database.connection import DatabaseConnection
from src.robot.v2.robot import Robot
from logging.config import dictConfig
from src.utils.logger import Logger


if __name__ == "__main__":

    # config log
    dictConfig(Logger().dict())

    # create tables
    db = DatabaseConnection()
    db.create_data_model()

    # run bot
    bot = Robot()
    bot.execute()
