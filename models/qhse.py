from db.database import Base


class Certification(Base):
    __table__ = Base.metadata.tables["qhse_certification"]

class Legende(Base):
    __table__ = Base.metadata.tables["qhse_legende"]

class Audit(Base):
    __table__ = Base.metadata.tables["qhse_audit"]


class Non_conformite(Base):
    __table__ = Base.metadata.tables["qhse_non_conformite"]