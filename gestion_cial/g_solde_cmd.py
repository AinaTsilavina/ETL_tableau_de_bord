import sqlite3
from db.database import SessionLocal
from models.commercial import Solde_cmd
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert


class GSoldeCmd:
    def __init__(self):
        self.db = SessionLocal()

    def get_solde(self):
        try:
            soldes = self.db.query(Solde_cmd).all()
            for solde in soldes:
                for k, v in solde.__dict__.items():
                    if k != "_sa_instance_state" : print(f"{k}: {v}", end=" ")
                print(end="\n")
        finally:
            self.db.close()


    def add_solde(self, data):

        try:
            solde = [{"client_id": cl.num_client,
                               "annee":cl.annee,
                               "semaine": cl.semaine,
                               "s_avion": cl.solde_avion,
                               "s_bateau": cl.solde_bateau,
                               "solde": cl.solde,
                               "cmd_mere": cl.cmd_mere} for cl in data.itertuples()]
            stmt = sqlite_upsert(Solde_cmd).values(solde)
            stmt = stmt.on_conflict_do_update(
                index_elements=["annee", "semaine", "client_id"], set_= dict(solde=stmt.excluded.solde, s_avion=stmt.excluded.s_avion, s_bateau=stmt.excluded.s_bateau)
            )
            self.db.execute(stmt)
            self.db.commit()
            print("Solde updated")
        except Exception as e :
            self.db.rollback()
        finally:
            self.db.close()



