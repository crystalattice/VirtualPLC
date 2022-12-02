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
    density: float = Column(Float)
    spec_gravity: float = Column(Float)
    outlet_slope: float = Column(Float)
    static_tank_press: float = Column(Float)
    outlet_pipe_diam: float = Column(Float)
    outlet_pipe_coeff: float = Column(Float)
    gravity_flow: float = Column(Float)


class GateValves(Base):
    """Create a database table for gate valves"""
    pass