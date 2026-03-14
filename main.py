# This is a sample Python script.
from dataframe import df_Famille, df_solde_cmd, df_prod_solde, df_gpec

from gestion_famille import *

from gestion_gpec.g_formation import GGpecFormation
from gestion_gpec.g_session import GGpecSession
from gestion_gpec.g_type import GGpecType
from gestion_gpec.g_participant import GGpecParticipant
from gestion_gpec.g_session_participant import GGpecSessionParticipant

from gestion_qhse.g_audit import GestionAudit
from gestion_qhse.g_non_conformite import GestionNonConformite
from gestion_chaine import GestionInfoChaine, GestionProdChaine

from gestion_cial.g_client import GClient
from gestion_cial.g_solde_cmd import GSoldeCmd
from gestion_cial.g_prod import GProd



# Menu principal
if __name__ == "__main__":
    audit = GestionAudit()
    infochaine = GestionInfoChaine()
    prod_chaine = GestionProdChaine()

    nc = GestionNonConformite()

    # for famille in df_Famille().itertuples():
    #     update_famille(famille.id, famille.chaine, famille.references, famille.moyenne)

    # Mise à jour tables production
    infochaine.add_chaine()
    prod_chaine.add_pord()

    # Mise à jour tables qhse
    audit.add_audit()
    nc.update_Non_conformite()

    # Mise à jour tables solde_cme
   
    client = GClient()
    client.get_client()
    solde = GSoldeCmd()
    print("DEBUG solde: ", solde)
    prod = GProd()
    data_solde = df_solde_cmd()
    data_prod = df_prod_solde()

    client.add_client(data_solde)
    solde.add_solde(data_solde)
    prod.add_prod(data_prod)

    # Mise à jour tables gpec
    # instanciation
    gpec = df_gpec()
    type = GGpecType()
    participant = GGpecParticipant()
    formation = GGpecFormation()
    session = GGpecSession()
    sessionParticipant = GGpecSessionParticipant()

    print("here-------------------")
    # opérations
    state = False
    for i in range(10):
        state = formation.add_formation(gpec["formation"])
        print("execution :",i+1)
        if state is True:
            break
        if i == 9:
            print("data Formation insert error!")
    if state is True:
        session.set_formation()
        session.add_session(gpec["sessions"])
        type.add_type(gpec["type"])
        participant.add_participant(gpec["participant"])
        sessionParticipant.add_session_participant(gpec["sessionsParticipant"])









