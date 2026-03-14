from settings import PATH_DB
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine




class Base(DeclarativeBase):
    pass

# Création de l'engine (SQLite)
DATABASE_URL = PATH_DB["db"]

engine = create_engine(DATABASE_URL, echo=True)
#configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.reflect(engine)

def get_session():
    """Créer une session pour les opérations sur la base."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

