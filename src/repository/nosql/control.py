from typing import List, Optional

from src.models.nosql.control import ControlModelNoSQL
from src.utils.conflog import logger


class ControlNoSQLRepository:
    def insert_control(self, value: list) -> ControlModelNoSQL:
        model = [ControlModelNoSQL(**data) for data in value]
        result = ControlModelNoSQL.objects.insert(model)
        logger.info("Data successfully saved.")
        return result

    def add_control(self, value: dict) -> ControlModelNoSQL:
        _control = ControlModelNoSQL(**value)
        logger.info("Data successfully saved.")
        return _control.save()

    def update_control(
        self, _id: str, value: dict
    ) -> Optional[ControlModelNoSQL]:
        result = ControlModelNoSQL.objects(id=_id).update_one(**value)
        logger.info("Data updated successfully.")
        return result

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[ControlModelNoSQL]:
        if is_active:
            return ControlModelNoSQL.objects(id=_id, is_active=is_active).first()
        return ControlModelNoSQL.objects(id=_id).first()

    def select_all(self, is_active: bool | None = None) -> List[ControlModelNoSQL]:
        if is_active:
            return ControlModelNoSQL.objects(is_active=is_active).all()
        return ControlModelNoSQL.objects.all()
