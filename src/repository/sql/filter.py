from typing import List, Optional

from sqlalchemy import insert, select, update

from src.database.connection_sql import ConnectionSQLDatabase
from src.models.sql.filter import FilterModelSQL
from src.utils.conflog import logger


class FilterSQLRepository:
    def __init__(self) -> None:
        self.session = ConnectionSQLDatabase().get_session()

    def insert_filter(self, value: list) -> FilterModelSQL:
        stmt = insert(FilterModelSQL).values(value).returning(FilterModelSQL)
        result = self.session.scalars(stmt)
        self.session.commit()
        logger.info("All filters successfully saved.")
        return result.first()

    def add_filter(self, value: dict) -> FilterModelSQL:
        model = FilterModelSQL(**value)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        logger.info("Filter successfully saved.")
        return model

    def update_filter(
        self, filter_id: str, value: dict
    ) -> Optional[FilterModelSQL]:
        stmt = (
            update(FilterModelSQL)
            .where(FilterModelSQL.id == filter_id)
            .values(value)
            .returning(FilterModelSQL)
        )
        result = self.session.scalars(stmt)
        self.session.commit()
        logger.info("Filter updated successfully.")
        return result.first()

    def toggle_filter(
        self, filter_id: str, action: bool
    ) -> Optional[FilterModelSQL]:
        stmt = (
            update(FilterModelSQL)
            .where(FilterModelSQL.id == filter_id)
            .values({FilterModelSQL.is_active: action})
            .returning(FilterModelSQL)
        )
        result = self.session.scalars(stmt)
        self.session.commit()
        logger.info("Filter status updated successfully.")
        return result.first()

    def select_by_id(
        self, filter_id: str, is_active: bool | None = None
    ) -> Optional[FilterModelSQL]:
        stmt = select(FilterModelSQL).where(FilterModelSQL.id == filter_id)
        if is_active:
            stmt = stmt.where(FilterModelSQL.is_active == is_active)
        return self.session.scalars(stmt).first()

    def select_all(
        self, is_active: bool | None = None
    ) -> List[FilterModelSQL]:
        stmt = select(FilterModelSQL)
        if is_active:
            stmt = stmt.where(FilterModelSQL.is_active == is_active)
        return self.session.scalars(stmt).all()
