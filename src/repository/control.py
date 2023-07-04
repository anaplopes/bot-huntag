from typing import List, Optional

from sqlalchemy import insert, select, update

from src.database.connection import DatabaseConnection
from src.model.control import ControlModel
from utils.logger import logger


class ControlRepository:
    def __init__(self) -> None:
        self.db = DatabaseConnection().get_session()

    def insert_control(self, value: dict) -> ControlModel:
        stmt = insert(ControlModel).values(value).returning(ControlModel)
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Dado inserido com sucesso.")
        return result.first()

    def add_control(self, value: dict) -> ControlModel:
        model = ControlModel(**value)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        logger.info("Dado salvo com sucesso.")
        return model

    def update_control(self, _id: str, value: dict) -> Optional[ControlModel]:
        stmt = (
            update(ControlModel)
            .where(ControlModel.id == _id)
            .values(value)
            .returning(ControlModel)
        )
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Dado atualizado com sucesso.")
        return result.first()

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[ControlModel]:
        stmt = select(ControlModel).where(ControlModel.id == _id)
        if is_active:
            stmt = stmt.where(ControlModel.is_active == is_active)
        return self.db.scalars(stmt).first()

    def select_all(self) -> List[ControlModel]:
        stmt = select(ControlModel)
        return self.db.scalars(stmt).all()
