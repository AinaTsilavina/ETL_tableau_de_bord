from sqlalchemy.exc import SQLAlchemyError

from db.database import SessionLocal
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from models.gpec import GpecParticipant


class GGpecParticipant:
    def __init__(self):
        self.db = SessionLocal()

    def get_participant(self):
        try:
            participants = self.db.query(GpecParticipant).all()
            return participants
        except SQLAlchemyError as e:
            print(e)
            return None

    def add_participant(self, participant):
        try:
            participants = [{"mle" : p.Mle,
                            "nom" : p.NOM,
                            "prenom" : p.PRENOM,
                            "fonction" : p.FONCTIONS,
                            "depart" : p.DEPARTEMENTS,
                            "type_id" : p.TYPE} for p in participant.itertuples()]
            stmt = sqlite_upsert(GpecParticipant).values(participants)
            on_conflict_update = stmt.on_conflict_do_update(
                index_elements=["mle"],
                set_=dict( nom= stmt.excluded.nom, prenom= stmt.excluded.prenom,fonction=stmt.excluded.fonction, depart=stmt.excluded.depart, type_id= stmt.excluded.type_id),
            )
            self.db.execute(on_conflict_update)
            self.db.commit()
            self.db.close()
            print(f"Participants added")
        except SQLAlchemyError as e:
            print(e)
