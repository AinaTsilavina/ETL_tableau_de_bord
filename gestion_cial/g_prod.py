from sqlalchemy.exc import SQLAlchemyError
from db.database import SessionLocal
from models.commercial import Prod
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert

class GProd:
    def __init__(self):
        self.db = SessionLocal()

    def get_prod(self):
        try:
            productions = self.db.query(Prod).all()
            return productions
        except SQLAlchemyError as e:
            print(e)
            return None

    def add_prod(self, df):
        try:
            prod = [{"prod": p.Prod,
                     "moyenne": p.Moyenne,
                     "date": p.Date,
                     "client_id": p.IDClient} for p in df.itertuples()]
            stmt = sqlite_upsert(Prod).values(prod)
            stmt = stmt.on_conflict_do_update(
                index_elements=["date", "client_id"], set_=dict(prod=stmt.excluded.prod, moyenne=stmt.excluded.moyenne)
            )
            self.db.execute(stmt)
            self.db.commit()
            self.db.close()
            print("Prod updated")
        except Exception as e:
            print(e)