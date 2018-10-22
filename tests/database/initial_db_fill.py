import sys
sys.path.extend(["/home/cody/PycharmProjects/VirtualPLC"])
from Utilities import utility_formulas

from PipingSystems.valve.valve import Gate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .create_test_db import Valve, Base

engine = create_engine("sqlite:///piping_test.db")  # Link to test DB
Base.metadata.bind = engine  # Bind engine to Base class metadata to access declaratives

DBSession = sessionmaker(bind=engine)  # Create DB session to talk to DB and establish data staging area
session = DBSession()  # Allows for session.commit() and session.rollback()

# Gate Valve 1
# valve1 = Gate("Valve 1", position=100, flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
#               press_in=utility_formulas.static_press(14))
# valve1.flow_out = valve1.flow_in
# valve1.press_drop(valve1.flow_out)
# valve1.get_press_out(valve1.press_in)

valve1_db = Valve(name="Valve 1", position=100, coeff=200, flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                  press_in=utility_formulas.static_press(14), flow_out=utility_formulas.gravity_flow_rate(2, 1.67),
                  deltaP=Gate.press_drop())
