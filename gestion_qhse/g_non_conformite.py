from db.database import SessionLocal
from models.qhse import Audit, Non_conformite
from dataframe import df_Qhse2


class GestionNonConformite:

    def __init__(self):
        self.session = SessionLocal()
        self.dataExterne = df_Qhse2()["NC"]

    def get_Non_conformite(self):
        try:
            Non_conformites = self.session.query(Non_conformite).all()
            for Non_conforme in Non_conformites:
                for k, v in Non_conforme.__dict__.items():
                    if k != "_sa_instance_state" : print(f"{k}: {v}", end=" ")
                print(end="\n")
        finally:
            self.session.close()

    def add_Non_conformite(self, nc):
        # print(nc.type, nc.certificat, nc.date, nc.nc, nc.nombre)
        audit_query = self.session.query(Audit).filter(Audit.type == nc.type, Audit.date == nc.date,
                                                       Audit.certificat_id == nc.certificat).first()
        if audit_query:
            self.session.add(Non_conformite(
                type = nc.nc,
                nombre = nc.nombre,
                audit_id = audit_query.id
            ))
            self.session.commit()
            self.session.close()
            print("NC insert")
        else:
            print("Audit not yet created !")

    def update_Non_conformite(self):

        for nc in self.dataExterne.itertuples():
            audit_query = self.session.query(Audit).filter(Audit.type == nc.type, Audit.date == nc.date,
                                                           Audit.certificat_id == nc.certificat).first()
            print("Non conformite:",audit_query.id, nc)
            if audit_query:
                nc_query = self.session.query(Non_conformite).filter(Non_conformite.audit_id == audit_query.id, Non_conformite.type == nc.nc).first()
                print("Ruesultat: ",nc_query)
                if nc_query:
                    nc_query.nombre = nc.nombre
                    self.session.commit()
                    print("NC update")
                else:
                    # pass
                    self.add_Non_conformite(nc)
        self.close_session()


    def close_session(self):
        self.session.close()
