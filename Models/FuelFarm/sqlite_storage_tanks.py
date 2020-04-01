from collections import namedtuple
from typing import NamedTuple, Any, Type

from sqlalchemy import create_engine, Column, String, Boolean, Integer, Float
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session

Base: DeclarativeMeta = declarative_base()
engine: Engine = create_engine("sqlite:///../../Tables/storage_tanks.db")
Base.metadata.bind = engine
db_session: sessionmaker = sessionmaker(bind=engine)
session: Session = db_session()


class StorageTanks(Base):
    """Create SQLAlchemy structure for DB

    The tablename needs to match the table name previously created.
    The column names need to match the names assigned in the table.
    """
    __tablename__: str = "storage_tanks"
    index: int = Column(Integer, primary_key=True)
    tank_name: str = Column(String, default="")
    tank_level: float = Column(Float, default=0.0)
    outlet_diameter: float = Column(Float, default=0.0)
    outlet_slope: float = Column(Float, default=0.0)
    static_pressure: float = Column(Float, default=0.0)
    gravity_flow_rate: float = Column(Float, default=0.0)
    fluid_density: float = Column(Float, default=1.94)
    fluid_spec_gravity: float = Column(Float, default=1.0)
    outlet_coeff: int = Column(Integer, default=140)
    outlet_flow_rate: float = Column(Float, default=0.0)


def get_tank_data(tank_index: int) -> NamedTuple:
    """Get the parameters for indicated tank."""
    TankParams: Type[NamedTuple] = namedtuple("Tanks", ["Tank Name",
                                                        "Tank Level",
                                                        "Outlet Diameter",
                                                        "Outlet Slope",
                                                        "Hydrostatic Pressure",
                                                        "Gravitational Flow Rate",
                                                        "Fluid Density",
                                                        "Fluid Specific Gravity",
                                                        "Outlet Pipe Coefficient",
                                                        "Outlet Flow Rate"
                                                        ]
                                              )

    tp = TankParams(
        session.query(StorageTanks.tank_name).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.tank_level).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.outlet_diameter).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.outlet_slope).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.static_pressure).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.gravity_flow_rate).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.fluid_density).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.fluid_spec_gravity).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.outlet_coeff).filter(StorageTanks.index == tank_index),
        session.query(StorageTanks.outlet_flow_rate).filter(StorageTanks.index == tank_index)
    )
    return tp


def add_new_tank(tank_name: str = "", tank_level: float = 0.0, diam_out: float = 0.0,
                 slope_out: float = 0.0, static_press: float = 0.0, grav_flow: float = 0.0, fluid_density: float = 0.0,
                 fluid_spec_gravity: float = 0.0, pipe_out_coeff: int = 0, pipe_out_flow: float = 0.0) -> None:
    """Set the parameters for an individual tank"""
    new_tank = StorageTanks(tank_name=tank_name, tank_level=tank_level, outlet_diameter=diam_out, outlet_slope=slope_out,
                            static_pressure=static_press, gravity_flow_rate=grav_flow, fluid_density=fluid_density,
                            fluid_spec_gravity=fluid_spec_gravity, outlet_coeff=pipe_out_coeff,
                            outlet_flow_rate=pipe_out_flow)
    session.add(new_tank)
    session.commit()
    
    
def get_all_tanks() -> list:
    """Get list of all tanks in the system"""
    tanks_list = []
    tanks = session.query(StorageTanks).all()
    for tank in tanks:
        tanks_list.append(tank)
        
    return tanks_list


def get_tank_index(tank_name: str) -> int:
    """Get the index value for a given tank name"""
    index_value = session.query(StorageTanks.index).filter(StorageTanks.tank_name == tank_name)
    return index_value


def del_tank_entry(index: int) -> None:
    """Remove specific tank entry from database"""
    session.delete(StorageTanks.index == index)
    session.commit()
