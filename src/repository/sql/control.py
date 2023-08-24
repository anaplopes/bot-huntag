from typing import List, Optional

from sqlalchemy import insert, select, update

from src.database.connection_sql import ConnectionSQLDatabase
from src.models.sql.control import ControlModelSQL
from src.utils.conflog import logger


class ControlSQLRepository:
    def __init__(self) -> None:
        self.db = ConnectionSQLDatabase().get_session()

    def insert_control(self, value: list) -> ControlModelSQL:
        stmt = insert(ControlModelSQL).values(value).returning(ControlModelSQL)
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Data successfully saved.")
        return result.first()

    def add_control(self, value: dict) -> ControlModelSQL:
        model = ControlModelSQL(**value)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        logger.info("Data successfully saved.")
        return model

    def update_control(
        self, _id: str, value: dict
    ) -> Optional[ControlModelSQL]:
        stmt = (
            update(ControlModelSQL)
            .where(ControlModelSQL.id == _id)
            .values(value)
            .returning(ControlModelSQL)
        )
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Data updated successfully.")
        return result.first()

    def select_by_id(
        self, _id: str, is_active: bool | None = None
    ) -> Optional[ControlModelSQL]:
        stmt = select(ControlModelSQL).where(ControlModelSQL.id == _id)
        if is_active:
            stmt = stmt.where(ControlModelSQL.is_active == is_active)
        return self.db.scalars(stmt).first()

    def select_all(self) -> List[ControlModelSQL]:
        stmt = select(ControlModelSQL)
        return self.session.scalars(stmt).all()
