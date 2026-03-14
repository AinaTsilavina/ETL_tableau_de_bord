from db.database import Base, engine, SessionLocal
from models.planning import Famille


def add_famille(id, chaine, references, moyenne):
    session = SessionLocal()
    try:
        famille = Famille(id=id, chaine=chaine, references=references, moyenne=moyenne)
        session.add(famille)
        session.commit()
        print("famille ajoutés avec succès !")
    finally:
        session.close()

def update_famille(id, chaine, references, moyenne):
    session = SessionLocal()
    try:
        famille = session.query(Famille).filter(Famille.id == id).first()
        if famille:
            famille.chaine = chaine
            famille.references = references
            famille.moyenne = moyenne
            session.commit()
            print(f"{id} mis à jour avec succès !")
        else:
            add_famille(id, chaine, references, moyenne)
    finally:
        session.close()

def get_familles():
    session = SessionLocal()
    try:
        familles = session.query(Famille).all()
        for famille in familles:
            print(f"CHAINE: {famille.chaine}, ID: {famille.id}, REF: {famille.references}, Moyenne: {famille.moyenne}")
    finally:
        session.close()