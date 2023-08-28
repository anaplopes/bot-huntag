from typing import List, Optional

from src.models.nosql.kit import KitModelNoSQL
from src.utils.conflog import logger


class KitNoSQLRepository:
    def insert_kit(self, value: list) -> KitModelNoSQL:
        model = [KitModelNoSQL(**data) for data in value]
        result = KitModelNoSQL.objects.insert(model)
        logger.info("All kits successfully saved.")
        return result

    def add_kit(self, value: dict) -> KitModelNoSQL:
        _kit = KitModelNoSQL(**value)
        logger.info("Kit successfully saved.")
        return _kit.save()

    def update_kit(self, kit_id: int, value: dict) -> Optional[KitModelNoSQL]:
        result = KitModelNoSQL.objects(kit_id=kit_id).update_one(**value)
        logger.info("Kit updated successfully.")
        return result

    def select_by_id(self, kit_id: int) -> Optional[KitModelNoSQL]:
        return KitModelNoSQL.objects(kit_id=kit_id).first()

    def select_all(self) -> List[KitModelNoSQL]:
        return KitModelNoSQL.objects.all()
