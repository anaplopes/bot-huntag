from typing import List, Optional

from src.database.connection_nosql import ConnectionNoSQLDatabase
from src.models.nosql.control import ControlModelNoSQL
from src.utils.conflog import logger


class ControlNoSQLRepository:
    def __init__(self) -> None:
        self.db = ConnectionNoSQLDatabase()

    def insert_control(self, value: list) -> ControlModelNoSQL:
        model = [ControlModelNoSQL(**data) for data in value]
        result = ControlModelNoSQL.objects.insert_many(model)
        logger.info("Data successfully saved.")
        return result

    def add_control(self, value: dict) -> ControlModelNoSQL:
        result = ControlModelNoSQL(**value).save()
        logger.info("Data successfully saved.")
        return result

    def update_control(self, _id: str, value: dict) -> Optional[ControlModelNoSQL]:
        result = ControlModelNoSQL.objects(id=_id).update_one(**value)
        logger.info("Data updated successfully.")
        return result

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[ControlModelNoSQL]:
        if is_active:
            return ControlModelNoSQL.objects.get(id=_id, is_active=is_active)
        return ControlModelNoSQL.objects.get(id=_id)

    def select_all(self) -> List[ControlModelNoSQL]:
        return ControlModelNoSQL.objects.all()
