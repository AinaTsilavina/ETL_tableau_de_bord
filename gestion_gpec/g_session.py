from sqlalchemy.exc import SQLAlchemyError

from db.database import SessionLocal
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from models.gpec import GpecSession
from gestion_gpec.g_formation import GGpecFormation

class GGpecSession:
    def __init__(self):
        self.db = SessionLocal()
        self._formation = None
        self.set_formation()

    #GETTER
    def get_session(self):
        session = None
        try:
            session = self.db.query(GpecSession).all()
        finally:
            self.db.close()

        return session

    def set_formation(self):
        formation = GGpecFormation()
        self._formation = formation.get_formation()
        # print([(f.id, f.intitule) for f in self._formation])

    @property
    def formation(self):
        return self._formation

    def _search_id_formation(self, data):
        data["INTITULE"] = data["INTITULE"].replace({f.intitule: str(f.id) for f in self._formation})
        # print(data["INTITULE"])
        return data

    def add_session(self, data):
#       repointage des id formations sur le data
        if self._formation is not None:
            data = self._search_id_formation(data)

            try:
                sessions = [{
                    "code": d.CODE,
                    "groupe": d.GROUPE,
                    "d_debut": d.DATE_DEBUT,
                    "d_fin" : d.DATE_FIN,
                    "h_debut": d.HEURE_DEBUT,
                    "h_fin": d.HEURE_FIN,
                    "salle": d.SALLE,
                    "remarque": d.REMARQUE,
                    "formation_id": d.INTITULE,
                }for d in data.itertuples()]
                stmt = sqlite_upsert(GpecSession).values(sessions)
                on_conflict_update = stmt.on_conflict_do_update(
                    index_elements=["code"],
                    set_=dict(groupe=stmt.excluded.groupe, formation_id = stmt.excluded.formation_id,
                              d_debut=stmt.excluded.d_debut, d_fin=stmt.excluded.d_fin,
                              h_debut=stmt.excluded.h_debut, h_fin=stmt.excluded.h_fin,
                            salle= stmt.excluded.salle, remarque= stmt.excluded.remarque),
                )
                self.db.execute(on_conflict_update)
                self.db.commit()
                self.db.close()
                print(f"Sessions added")
            except SQLAlchemyError as e:
                print(e)

