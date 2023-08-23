from typing import List, Optional

from src.database.connection_nosql import ConnectionNoSQLDatabase
from src.models.nosql.kit import KitModelNoSQL
from src.utils.conflog import logger


class KitNoSQLRepository:
    def __init__(self) -> None:
        self.db = ConnectionNoSQLDatabase()

    def insert_kit(self, value: list) -> KitModelNoSQL:
        model = [KitModelNoSQL(**data) for data in value]
        result = KitModelNoSQL.objects.insert_many(model)
        logger.info("Data successfully saved.")
        return result

    def add_kit(self, value: dict) -> KitModelNoSQL:
        result = KitModelNoSQL(**value).save()
        logger.info("Data successfully saved.")
        return result

    def update_kit(self, _id: str, value: dict) -> Optional[KitModelNoSQL]:
        result = KitModelNoSQL.objects(id=_id).update_one(**value)
        logger.info("Data updated successfully.")
        return result

    def select_by_kit_id(self, kit_id: str) -> Optional[KitModelNoSQL]:
        return KitModelNoSQL.objects.get(kit_id=kit_id)

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[KitModelNoSQL]:
        if is_active:
            return KitModelNoSQL.objects.get(id=_id, is_active=is_active)
        return KitModelNoSQL.objects.get(id=_id)

    def select_all(self) -> List[KitModelNoSQL]:
        return KitModelNoSQL.objects.all()
