from db.database import Base


class Client(Base):
    __table__ = Base.metadata.tables["commercial_client"]

class Prod(Base):
    __table__ = Base.metadata.tables["commercial_production"]

class Solde_cmd(Base):
    __table__ = Base.metadata.tables["commercial_solde_cmd"]
