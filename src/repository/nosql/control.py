from typing import List, Optional

from src.models.nosql.control import ControlModelNoSQL
from src.utils.conflog import logger


class ControlNoSQLRepository:
    def insert_control(self, value: list) -> ControlModelNoSQL:
        model = [ControlModelNoSQL(**data) for data in value]
        result = ControlModelNoSQL.objects.insert(model)
        logger.info("All controls successfully saved.")
        return result

    def add_control(self, value: dict) -> ControlModelNoSQL:
        _control = ControlModelNoSQL(**value)
        logger.info("Control successfully saved.")
        return _control.save()

    def update_control(
        self, control_id: str, value: dict
    ) -> Optional[ControlModelNoSQL]:
        result = ControlModelNoSQL.objects(id=control_id).update_one(**value)
        logger.info("Control updated successfully.")
        return result

    def select_by_status(
        self, kit_id: int, kit_creation_date: str, action: str, status: str
    ) -> Optional[ControlModelNoSQL]:
        return ControlModelNoSQL.objects(
            kit_id=kit_id,
            kit_creation_date=kit_creation_date,
            action=action,
            status=status,
        ).first()

    def select_by_id(self, control_id: str) -> Optional[ControlModelNoSQL]:
        return ControlModelNoSQL.objects(id=control_id).first()

    def select_all(self) -> List[ControlModelNoSQL]:
        return ControlModelNoSQL.objects.all()
