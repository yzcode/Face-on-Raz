# _*_ coding: utf-8 _*_

from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship,backref
from db import engine,Base

class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    file_hash = Column(String(40))
    face_id = Column(Integer)
    cof = Column(Float)


class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    file_hash = Column(String(40))
    face_hash = Column(String(40))


class Trustlib(Base):
    __tablename__ = "trustlibs"

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    desc = Column(String(100))


class FaceBind(Base):
    __tablename__ = "facebinds"

    id = Column(Integer, primary_key=True)
    trust_id = Column(Integer)
    face_id = Column(Integer)


