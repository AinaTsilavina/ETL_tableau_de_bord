# from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import DeclarativeBase
from db.database import Base


class Famille(Base):
    __table__ = Base.metadata.tables["planning_famille"]
