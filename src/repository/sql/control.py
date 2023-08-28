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
        logger.info("All controls successfully saved.")
        return result.first()

    def add_control(self, value: dict) -> ControlModelSQL:
        model = ControlModelSQL(**value)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        logger.info("Control successfully saved.")
        return model

    def update_control(
        self, control_id: str, value: dict
    ) -> Optional[ControlModelSQL]:
        stmt = (
            update(ControlModelSQL)
            .where(ControlModelSQL.id == control_id)
            .values(value)
            .returning(ControlModelSQL)
        )
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Control updated successfully.")
        return result.first()

    def select_by_status(
        self, kit_id: int, kit_creation_date: str, action: str, status: str
    ) -> Optional[ControlModelSQL]:
        stmt = select(ControlModelSQL).where(
            ControlModelSQL.kit_id == kit_id,
            ControlModelSQL.kit_creation_date == kit_creation_date,
            ControlModelSQL.action == action,
            ControlModelSQL.status == status,
        )
        return self.db.scalars(stmt).first()

    def select_by_id(self, control_id: str) -> Optional[ControlModelSQL]:
        stmt = select(ControlModelSQL).where(ControlModelSQL.id == control_id)
        return self.db.scalars(stmt).first()

    def select_all(self) -> List[ControlModelSQL]:
        stmt = select(ControlModelSQL)
        return self.session.scalars(stmt).all()
