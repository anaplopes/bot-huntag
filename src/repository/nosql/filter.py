from typing import List, Optional

from src.database.connection_nosql import ConnectionNoSQLDatabase
from src.models.nosql.filter import FilterModelNoSQL
from src.utils.conflog import logger


class FilterNoSQLRepository:
    def __init__(self) -> None:
        self.db = ConnectionNoSQLDatabase()

    def insert_filter(self, value: list) -> FilterModelNoSQL:
        model = [FilterModelNoSQL(**data) for data in value]
        result = FilterModelNoSQL.objects.insert_many(model)
        logger.info("Data successfully saved.")
        return result

    def add_filter(self, value: dict) -> FilterModelNoSQL:
        result = FilterModelNoSQL(**value).save()
        logger.info("Data successfully saved.")
        return result

    def update_filter(self, _id: str, value: dict) -> Optional[FilterModelNoSQL]:
        result = FilterModelNoSQL.objects(id=_id).update_one(**value)
        logger.info("Data updated successfully.")
        return result

    def toggle_filter(self, _id: str, action: bool) -> Optional[FilterModelNoSQL]:
        result = FilterModelNoSQL.objects(id=_id).update_one({"is_active": action})
        logger.info("Status updated successfully.")
        return result

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[FilterModelNoSQL]:
        if is_active:
            return FilterModelNoSQL.objects.get(id=_id, is_active=is_active)
        return FilterModelNoSQL.objects.get(id=_id)

    def select_all(self) -> List[FilterModelNoSQL]:
        return FilterModelNoSQL.objects.all()
