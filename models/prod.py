from db.database import Base


class Prod(Base):
    __table__ = Base.metadata.tables["production_production"]


class Chaine(Base):
    __table__ = Base.metadata.tables["production_chaine"]

class InfoChaine(Base):
    __table__ = Base.metadata.tables["production_info_chaine"]