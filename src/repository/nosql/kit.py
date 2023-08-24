from typing import List, Optional

from src.models.nosql.kit import KitModelNoSQL
from src.utils.conflog import logger


class KitNoSQLRepository:
    def insert_kit(self, value: list) -> KitModelNoSQL:
        model = [KitModelNoSQL(**data) for data in value]
        result = KitModelNoSQL.objects.insert(model)
        logger.info("Data successfully saved.")
        return result

    def add_kit(self, value: dict) -> KitModelNoSQL:
        _kit = KitModelNoSQL(**value)
        logger.info("Data successfully saved.")
        return _kit.save()

    def update_kit(self, _id: str, value: dict) -> Optional[KitModelNoSQL]:
        result = KitModelNoSQL.objects(id=_id).update_one(**value)
        logger.info("Data updated successfully.")
        return result

    def select_by_kit_id(self, kit_id: str) -> Optional[KitModelNoSQL]:
        return KitModelNoSQL.objects(kit_id=kit_id).first()

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[KitModelNoSQL]:
        if is_active:
            return KitModelNoSQL.objects(id=_id, is_active=is_active).first()
        return KitModelNoSQL.objects(id=_id).first()

    def select_all(self, is_active: bool | None = None) -> List[KitModelNoSQL]:
        if is_active:
            return KitModelNoSQL.objects(is_active=is_active).all()
        return KitModelNoSQL.objects.all()
