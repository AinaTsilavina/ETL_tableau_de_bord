from db.database import Base


class GpecFormation(Base):
    __table__ = Base.metadata.tables['gpec_formation']

class GpecParticipant(Base):
    __table__ = Base.metadata.tables['gpec_participant']

class GpecSession(Base):
    __table__ = Base.metadata.tables['gpec_session']

class GpecSessionParticipant(Base):
    __table__ = Base.metadata.tables['gpec_session_participant']

class GpecType(Base):
    __table__ = Base.metadata.tables['gpec_type']