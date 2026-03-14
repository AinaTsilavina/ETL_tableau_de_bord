from db.database import SessionLocal
from models.commercial import Client
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert


class GClient:
    def __init__(self):
        self.db = SessionLocal()

    def get_client(self):
        try:
            clients = self.db.query(Client).all()
            for client in clients:
                for k, v in client.__dict__.items():
                    if k != "_sa_instance_state" : print(f"{k}: {v}", end=" ")
                print(end="\n")
        finally:
            self.db.close()

    def add_client(self, data):
        try:
            client_add = [{"id":cl.num_client, "nom":cl.client} for cl in data.itertuples()]
            stmt = sqlite_upsert(Client).values(client_add)
            on_conflict_update = stmt.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(nom=stmt.excluded.nom)
            )
            self.db.execute(on_conflict_update)
            self.db.commit()
            self.db.close()
            print(f"Clients added")
        except Exception as e:
            print(e)

