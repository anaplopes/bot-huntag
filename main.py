from src.database.connection import DatabaseConnection
from src.robot import Robot

if __name__ == "__main__":
    DatabaseConnection().create_data_model()
    bot = Robot()
    bot.run()
