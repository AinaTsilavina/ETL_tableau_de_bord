from sqlalchemy.exc import SQLAlchemyError

from db.database import SessionLocal
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from models.gpec import GpecType


class GGpecType:
    def __init__(self):
        self.db = SessionLocal()

    def get_type(self):
        try:
            types = self.db.query(GpecType).all()
            return types
        except SQLAlchemyError as e:
            print(e)
            return None

    def add_type(self, data):
        try:
            types = [{
                "id": t.id_type,
                "nom": t.TYPE } for t in data.itertuples()]
            stmt = sqlite_upsert(GpecType).values(types)
            on_conflict_update = stmt.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(nom=stmt.excluded.nom)
            )
            self.db.execute(on_conflict_update)
            self.db.commit()
            self.db.close()
            print(f"Types added")

        except SQLAlchemyError as e:
            print(e)

