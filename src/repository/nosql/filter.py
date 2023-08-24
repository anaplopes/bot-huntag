from typing import List, Optional

from src.models.nosql.filter import FilterModelNoSQL
from src.utils.conflog import logger


class FilterNoSQLRepository:
    def insert_filter(self, value: list) -> FilterModelNoSQL:
        model = [FilterModelNoSQL(**data) for data in value]
        result = FilterModelNoSQL.objects.insert(model)
        logger.info("Data successfully saved.")
        return result

    def add_filter(self, value: dict) -> FilterModelNoSQL:
        _filter = FilterModelNoSQL(**value)
        logger.info("Data successfully saved.")
        return _filter.save()

    def update_filter(
        self, _id: str, value: dict
    ) -> Optional[FilterModelNoSQL]:
        result = FilterModelNoSQL.objects(id=_id).update_one(**value)
        logger.info("Data updated successfully.")
        return result

    def toggle_filter(
        self, _id: str, action: bool
    ) -> Optional[FilterModelNoSQL]:
        result = FilterModelNoSQL.objects(id=_id).update_one(
            {"is_active": action}
        )
        logger.info("Status updated successfully.")
        return result

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[FilterModelNoSQL]:
        if is_active:
            return FilterModelNoSQL.objects(id=_id, is_active=is_active).first()
        return FilterModelNoSQL.objects(id=_id).first()

    def select_all(self, is_active: bool | None = None) -> List[FilterModelNoSQL]:
        if is_active:
            return FilterModelNoSQL.objects(is_active=is_active).all()
        return FilterModelNoSQL.objects.all()
