from typing import List, Optional

from sqlalchemy import delete, insert, select, update

from src.database.connection import ConnectionDatabase
from src.model.filter import FilterModel
from src.utils.logger import logger


class FilterRepository:
    def __init__(self) -> None:
        self.session = ConnectionDatabase().get_session()

    def delete_filter(self, _id: str) -> FilterModel:
        stmt = (
            delete(FilterModel)
            .where(FilterModel.c.id == _id)
            .returning(FilterModel)
        )
        result = self.session.scalars(stmt)
        self.session.commit()
        logger.info("Data removed successfully.")
        return result.first()

    def insert_filter(self, value: dict) -> FilterModel:
        stmt = insert(FilterModel).values(value).returning(FilterModel)
        result = self.session.scalars(stmt)
        self.session.commit()
        logger.info("Data successfully saved.")
        return result.first()

    def add_filter(self, value: dict) -> FilterModel:
        model = FilterModel(**value)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        logger.info("Data successfully saved.")
        return model

    def update_filter(self, _id: str, value: dict) -> Optional[FilterModel]:
        stmt = (
            update(FilterModel)
            .where(FilterModel.id == _id)
            .values(value)
            .returning(FilterModel)
        )
        result = self.session.scalars(stmt)
        self.session.commit()
        logger.info("Data updated successfully.")
        return result.first()

    def toggle_filter(self, _id: str, action: bool) -> Optional[FilterModel]:
        stmt = (
            update(FilterModel)
            .where(FilterModel.id == _id)
            .values({FilterModel.is_active: action})
            .returning(FilterModel)
        )
        result = self.session.scalars(stmt)
        self.session.commit()
        logger.info("Status updated successfully.")
        return result.first()

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[FilterModel]:
        stmt = select(FilterModel).where(FilterModel.id == _id)
        if is_active:
            stmt = stmt.where(FilterModel.is_active == is_active)
        return self.session.scalars(stmt).first()

    def select_all(self, is_active: bool | None = None) -> List[FilterModel]:
        stmt = select(FilterModel)
        if is_active:
            stmt = stmt.where(FilterModel.is_active == is_active)
        return self.session.scalars(stmt).all()
