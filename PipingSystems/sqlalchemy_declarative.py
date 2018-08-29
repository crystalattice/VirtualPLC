from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Pump(Base):
    __tablename__ = "pump"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    flow_out = Column(Float)
    press_in = Column(Float)
    press_out = Column(Float)
    speed = Column(Integer)
    power = Column(Float)
    displacement = Column(Float)


class Valve(Base):
    __tablename__ = "valve"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(Integer)
    coeff = Column(Float)
    flow_in = Column(Float)
    deltaP = Column(Float)
    flow_out = Column(Float)
    press_in = Column(Float)
    press_out = Column(Float)
    open_setpt = Column(Integer)
    close_setpt = Column(Integer)


class Tank(Base):
    __tablename__ = "tank"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(Float)
    fluid_density = Column(Float)
    spec_gravity = Column(Float)
    press_out = Column(Float)
    pipe_diam = Column(Float)
    pipe_slope = Column(Float)
    pipe_coeff = Column(Float)


engine = create_engine("sqlite:///pipe_scenario.db")

Base.metadata.create_all(engine)
