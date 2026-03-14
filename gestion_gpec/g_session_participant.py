from sqlalchemy.exc import SQLAlchemyError

from db.database import SessionLocal
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from models.gpec import GpecSessionParticipant

class GGpecSessionParticipant:
    def __init__(self):
        self.db = SessionLocal()

    def get_session_participant(self):
        return self.db.query(GpecSessionParticipant).all()

    def add_session_participant(self, data):
        try:
            sessions_participants = [{
                "session_id": d.CODE,
                "participant_id": d.Mle
            } for d in data.itertuples()]
            stmt = sqlite_upsert(GpecSessionParticipant).values(sessions_participants)
            on_conflict_nothing = stmt.on_conflict_do_nothing(
                index_elements=["session_id", "participant_id"],
            )
            self.db.execute(on_conflict_nothing)
            self.db.commit()
            self.db.close()
            print(f"Sessions_Participants added")
        except SQLAlchemyError as e:
            print(e)