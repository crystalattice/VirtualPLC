from .create_db import Base, Tanks, GateValves, GlobeValves, ReliefValves
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db_test.db")
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

tanks = session.query(Tanks).all()
for tank in tanks:
    # print(tank.name, tank.level, tank.density, tank.gravity_flow, tank.spec_gravity, tank.static_tank_press,
    #       tank.outlet_slope, tank.outlet_pipe_coeff, tank.outlet_pipe_diam)
    print(tank.name)

tank = session.query(Tanks).first()
print("\n" + tank.name)

gate = session.query(GateValves).first()
print("\n" + gate.name)