from typing import List, Optional

from src.models.nosql.filter import FilterModelNoSQL
from src.utils.conflog import logger


class FilterNoSQLRepository:
    def insert_filter(self, value: list) -> FilterModelNoSQL:
        model = [FilterModelNoSQL(**data) for data in value]
        result = FilterModelNoSQL.objects.insert(model)
        logger.info("All filters successfully saved.")
        return result

    def add_filter(self, value: dict) -> FilterModelNoSQL:
        _filter = FilterModelNoSQL(**value)
        logger.info("Filter successfully saved.")
        return _filter.save()

    def update_filter(
        self, filter_id: str, value: dict
    ) -> Optional[FilterModelNoSQL]:
        result = FilterModelNoSQL.objects(id=filter_id).update_one(**value)
        logger.info("Filter updated successfully.")
        return result

    def toggle_filter(
        self, filter_id: str, action: bool
    ) -> Optional[FilterModelNoSQL]:
        result = FilterModelNoSQL.objects(id=filter_id).update_one(
            {"is_active": action}
        )
        logger.info("Filter status updated successfully.")
        return result

    def select_by_id(
        self, filter_id: str, is_active: bool | None = None
    ) -> Optional[FilterModelNoSQL]:
        if is_active:
            return FilterModelNoSQL.objects(
                id=filter_id, is_active=is_active
            ).first()
        return FilterModelNoSQL.objects(id=filter_id).first()

    def select_all(
        self, is_active: bool | None = None
    ) -> List[FilterModelNoSQL]:
        if is_active:
            return FilterModelNoSQL.objects(is_active=is_active).all()
        return FilterModelNoSQL.objects.all()
