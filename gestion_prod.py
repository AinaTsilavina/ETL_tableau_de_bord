from db.database import SessionLocal
from models.prod import Prod


def add_prod(efficience, effimoyen, date, retouche, second_choix):
    session = SessionLocal()
    try:
        prod = Prod(chaine=efficience, effimoyen= effimoyen, date = date, retouche= retouche, second_choix= second_choix)
        session.add(prod)
        session.commit()
        print("prod ajoutés avec succès !")
    finally:
        session.close()

def update_prod(efficience, effimoyen, date, retouche, second_choix):
    session = SessionLocal()
    try:
        prod = session.query(Prod).filter(Prod.date == date).first()
        if prod:
            prod.efficience = efficience
            prod.effimoyen = effimoyen
            prod.retouche = retouche
            prod.second_choix = second_choix
            session.commit()
            print(f"{prod.id} mis à jour avec succès !")
        else:
            add_prod(efficience, effimoyen, date, retouche, second_choix)
    finally:
        session.close()

def get_prod():
    session = SessionLocal()
    try:
        prod = session.query(Prod).all()
        for production in prod:
            print(f"DATE: {production.date}, EFF: {production.efficience}, MOYENNE: {production.effimoyen}, RETOUCHE: {production.retouche}, 2nd_CHOIX: {production.second_choix}")
    finally:
        session.close()