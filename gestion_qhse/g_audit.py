from db.database import SessionLocal
from models.qhse import Audit
from dataframe import df_Qhse2




class GestionAudit:

    def __init__(self):
        self.session = SessionLocal()
        # self.certificat = df_Qhse()["certification"]
        self.legende = df_Qhse2()["legende"]
        self.dataExterne = df_Qhse2()["audit"]

    def get_audit(self):
        try:
            audits = self.session.query(Audit).all()
            for audit in audits:
                for k, v in audit.__dict__.items():
                    if k != "_sa_instance_state" : print(f"{k}: {v}", end=" ")
                print(end="\n")
        finally:
            self.session.close()

    def add_audit(self):
        try:
            audits = []
            # print(self.dataExterne)
            for audit in self.dataExterne.itertuples():
                audit_query = self.session.query(Audit).filter(Audit.type == audit.type, Audit.date == audit.date, Audit.certificat_id == audit.certificat ).first()
                print(audit.type,audit.certificat,audit.date)
                if audit_query:
                    # print(audit_query.type, audit_query.certificat_id, audit_query.date)
                    audit_query.service = audit.service
                    audit_query.resultat_id = audit.resultat
                    print("update", audit_query.type, audit_query.date, audit_query.certificat_id)
                else:
                    self.session.add(Audit(type = audit.type
                              , date = audit.date
                              , service = audit.service
                              , certificat_id = audit.certificat
                              , resultat_id = audit.resultat))
                    print("insert",audit.type, audit.date, audit.certificat)
                self.session.commit()
                self.session.close()
            print("Data insert")
        except:
            print('Error in insert value !')

    def update_audit(self,type_audit, date_audit, service, certificat_id, resultat_audit):
        try:
            audit_query = self.session.query(Audit).filter(Audit.type == type_audit, Audit.date == date_audit, Audit.certificat_id == certificat_id ).First()
            if audit_query:
                audit_query.service = service
                audit_query.resultat_id = resultat_audit
                self.session.commit()
            else:
                self.add_audit(type_audit, date_audit, service, certificat_id, resultat_audit)
        except:
            print('Error in update value !')

    def close_session(self):
        self.session.close()
