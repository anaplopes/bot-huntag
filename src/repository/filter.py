from typing import List, Optional

from sqlalchemy import delete, insert, select, update

from src.database.connection import DatabaseConnection
from src.model.filter import FilterModel
from utils.logger import logger


class FilterRepository:
    def __init__(self) -> None:
        self.db = DatabaseConnection().get_session()

    def delete_filter(self, _id: str) -> FilterModel:
        stmt = (
            delete(FilterModel)
            .where(FilterModel.c.id == _id)
            .returning(FilterModel)
        )
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Dado removido com sucesso.")
        return result.first()

    def insert_filter(self, value: dict) -> FilterModel:
        stmt = insert(FilterModel).values(value).returning(FilterModel)
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Dado inserido com sucesso.")
        return result.first()

    def add_filter(self, value: dict) -> FilterModel:
        model = FilterModel(**value)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        logger.info("Dado salvo com sucesso.")
        return model

    def update_filter(self, _id: str, value: dict) -> Optional[FilterModel]:
        stmt = (
            update(FilterModel)
            .where(FilterModel.id == _id)
            .values(value)
            .returning(FilterModel)
        )
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Dado atualizado com sucesso.")
        return result.first()

    def toggle_filter(self, _id: str, action: bool) -> Optional[FilterModel]:
        stmt = (
            update(FilterModel)
            .where(FilterModel.id == _id)
            .values({FilterModel.is_active: action})
            .returning(FilterModel)
        )
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Status atualizado com sucesso.")
        return result.first()

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[FilterModel]:
        stmt = select(FilterModel).where(FilterModel.id == _id)
        if is_active:
            stmt = stmt.where(FilterModel.is_active == is_active)
        return self.db.scalars(stmt).first()

    def select_all(self) -> List[FilterModel]:
        stmt = select(FilterModel)
        return self.db.scalars(stmt).all()
