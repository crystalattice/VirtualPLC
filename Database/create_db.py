#!/usr/bin/env python3
"""
Create SQLAlchemy environment for model
"""
from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tanks(Base):
    """Create a database table for storage tanks"""
    __tablename__ = "tanks"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=250), nullable=False)
    level: float = Column(Float)
    density: float = Column(Float, default=1.94)
    spec_gravity: float = Column(Float, default=1.0)
    outlet_slope: float = Column(Float, default=0.0)
    static_tank_press: float = Column(Float, default=0.0)
    outlet_pipe_diam: float = Column(Float, default=0.0)
    outlet_pipe_coeff: float = Column(Float, default=140)
    gravity_flow: float = Column(Float)


class GateValves(Base):
    """Create a database table for gate valves"""
    __tablename__ = "gate_valves"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=250), nullable=False)
    position: str = Column(String(length=10))


class GlobeValves(Base):
    """Create a database table for globe valves"""
    __tablename__ = "globe_valves"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=250), nullable=False)
    flow_coeff: int = Column(Integer)
    press_in: int = Column(Integer)
    sys_flow_in: int = Column(Integer)
    position: str = Column(String(length=10))


class ReliefValves(Base):
    """Create a database table for relief valves"""
    __tablename__ = "relief_valves"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=250), nullable=False)
    open_press: int = Column(Integer)
    close_press: int = Column(Integer)
    position: str = Column(String(length=10))


engine = create_engine("sqlite:///db_test.db")
Base.metadata.create_all(engine)
