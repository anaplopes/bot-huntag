from logging.config import dictConfig

from migration import migrate
from src.database.connection_nosql import ConnectionNoSQLDatabase
from src.database.connection_sql import ConnectionSQLDatabase
from src.repository.nosql.control import ControlNoSQLRepository
from src.repository.nosql.filter import FilterNoSQLRepository
from src.repository.nosql.kit import KitNoSQLRepository
from src.repository.sql.control import ControlSQLRepository
from src.repository.sql.filter import FilterSQLRepository
from src.repository.sql.kit import KitSQLRepository
from src.settings import settings
from src.usecases.robot import Robot
from src.utils.conflog import ConfLog

if __name__ == "__main__":
    # config log
    dictConfig(ConfLog().dict())

    if settings.TYPE_DB == "SQL":
        ConnectionSQLDatabase().create_data_model()
        migrate.data_filter(repo=FilterSQLRepository())
        Robot(
            repo_control=ControlSQLRepository(),
            repo_filter=FilterSQLRepository(),
            repo_kit=KitSQLRepository(),
        ).execute()

    if settings.TYPE_DB == "NoSQL":
        ConnectionNoSQLDatabase()
        migrate.data_filter(repo=FilterNoSQLRepository())
        Robot(
            repo_control=ControlNoSQLRepository(),
            repo_filter=FilterNoSQLRepository(),
            repo_kit=KitNoSQLRepository(),
        ).execute()
