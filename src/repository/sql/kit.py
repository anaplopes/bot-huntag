from typing import List, Optional

from sqlalchemy import insert, select, update

from src.database.connection_sql import ConnectionSQLDatabase
from src.models.sql.kit import KitModelSQL
from src.utils.conflog import logger


class KitSQLRepository:
    def __init__(self) -> None:
        self.db = ConnectionSQLDatabase().get_session()

    def insert_kit(self, value: list) -> KitModelSQL:
        stmt = insert(KitModelSQL).values(value).returning(KitModelSQL)
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("All kits successfully saved.")
        return result.first()

    def add_kit(self, value: dict) -> KitModelSQL:
        model = KitModelSQL(**value)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        logger.info("Kit successfully saved.")
        return model

    def update_kit(self, kit_id: int, value: dict) -> Optional[KitModelSQL]:
        stmt = (
            update(KitModelSQL)
            .where(KitModelSQL.kit_id == kit_id)
            .values(value)
            .returning(KitModelSQL)
        )
        result = self.db.scalars(stmt)
        self.db.commit()
        logger.info("Kit updated successfully.")
        return result.first()

    def select_by_id(
        self, kit_id: int, is_active: bool | None = None
    ) -> Optional[KitModelSQL]:
        stmt = select(KitModelSQL).where(KitModelSQL.kit_id == kit_id)
        return self.db.scalars(stmt).first()

    def select_all(self) -> List[KitModelSQL]:
        stmt = select(KitModelSQL)
        return self.session.scalars(stmt).all()
