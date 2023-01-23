from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .create_db import Tanks, GateValves, GlobeValves, ReliefValves, Base

engine = create_engine("sqlite:///db_test.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

tank1 = Tanks(name="tank1", level=10)
tank2 = Tanks(name="tank2", level=5)
gate1 = GateValves(name="Pump Inlet", position="open")

items = (tank1, tank2, gate1)
session.add_all(items)
session.commit()
