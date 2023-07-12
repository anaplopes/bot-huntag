from typing import List, Optional

from sqlalchemy import insert, select, update

from src.database.connection import ConnectionDatabase
from src.models.kit import KitModel
from src.utils.logger import logger


class KitRepository:
    def __init__(self) -> None:
        self.db = ConnectionDatabase().get_session()

    def insert_control(self, value: dict) -> KitModel:
        stmt = insert(KitModel).values(value).returning(KitModel)
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Data successfully saved.")
        return result.first()

    def add_control(self, value: dict) -> KitModel:
        model = KitModel(**value)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        logger.info("Data successfully saved.")
        return model

    def update_control(self, _id: str, value: dict) -> Optional[KitModel]:
        stmt = (
            update(KitModel)
            .where(KitModel.id == _id)
            .values(value)
            .returning(KitModel)
        )
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Data updated successfully.")
        return result.first()

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[KitModel]:
        stmt = select(KitModel).where(KitModel.id == _id)
        if is_active:
            stmt = stmt.where(KitModel.is_active == is_active)
        return self.db.scalars(stmt).first()

    def select_by_fileid(self, file_id: str) -> Optional[KitModel]:
        stmt = select(KitModel).where(KitModel.file_id == file_id)
        return self.db.scalars(stmt).first()

    def select_all(self) -> List[KitModel]:
        stmt = select(KitModel)
        return self.session.scalars(stmt).all()
