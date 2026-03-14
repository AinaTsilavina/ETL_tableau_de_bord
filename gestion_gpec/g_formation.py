from sqlalchemy.exc import SQLAlchemyError

from db.database import SessionLocal
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from models.gpec import GpecFormation


class GGpecFormation:
    def __init__(self):
        self.db = SessionLocal()

    def get_formation(self):
        formation = None
        try:
            formation = self.db.query(GpecFormation).all()
        finally:
            self.db.close()
            return formation


    def add_formation(self, data):
        try:
            formations = [{
                "intitule": f.INTITULE
            } for f in data.itertuples()]
            stmt = sqlite_upsert(GpecFormation).values(formations)
            on_conflict_nothing = stmt.on_conflict_do_nothing(
                index_elements=["intitule"],
            )
            self.db.execute(on_conflict_nothing)
            self.db.commit()
            self.db.close()
            print(f"Formations added")
            return True
        except SQLAlchemyError as e:
            print(e)
            return False



