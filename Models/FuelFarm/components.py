#!/usr/bin/env python3
"""
FuelFarm.py

Purpose: Simulate an aviation fuel storage and transfer system.

Author: Cody Jackson

Date: 6/12/18
#################################
Version 0.1
    Initial build
"""
import utility_formulas

from PipingSystems.pump import pump
from PipingSystems.valve import valve
from PipingSystems.storage_tank import tank

# Constants
DENSITY = 1.629869
SPEC_GRAVITY = 0.840

# Storage tanks
# Assumes 36 ft tall tank w/ 1 million gallon capacity = 27778 gallons per foot
# Assumes 16 inch diam transfer piping
tank1 = tank.Tank("Tank 1", level=36.0, fluid_density=DENSITY, spec_gravity=SPEC_GRAVITY)
tank1.static_tank_press = tank1.level
tank1.flow_out = utility_formulas.gravity_flow_rate(diameter=16, slope=0.25, rough_coeff=140)

tank2 = tank.Tank("Tank 2", level=36.0, fluid_density=DENSITY, spec_gravity=SPEC_GRAVITY)
tank2.static_tank_press = tank1.level
tank2.flow_out = utility_formulas.gravity_flow_rate(diameter=16, slope=0.25, rough_coeff=140)

# Tank-pump connections
# Assumes 16 inch pipe connection
gate1 = valve.Gate("Gate valve 1", sys_flow_in=tank1.flow_out, press_in=tank1.static_tank_press)
gate1.calc_coeff(16)

gate2 = valve.Gate("Gate valve 2", sys_flow_in=tank2.flow_out, press_in=tank2.static_tank_press)
gate2.calc_coeff(16)

gate3 = valve.Gate("Gate valve 3", sys_flow_in=gate1.flow_out, press_in=gate1.press_out)
gate3.calc_coeff(16)

gate4 = valve.Gate("Gate valve 4", sys_flow_in=gate2.flow_out, press_in=gate2.press_out)
gate4.calc_coeff(16)

gate5 = valve.Gate("Gate valve 5", sys_flow_in=gate1.flow_out, press_in=gate1.press_out)
gate5.calc_coeff(16)

gate6 = valve.Gate("Gate valve 6", sys_flow_in=gate3.flow_out + gate4.flow_out,
                   press_in=gate3.press_out + gate4.press_out)
gate6.calc_coeff(16)

gate7 = valve.Gate("Gate valve 7", sys_flow_in=gate2.flow_out, press_in=gate2.press_out)
gate7.calc_coeff(16)

# Fuel pumps
pump1 = pump.PositiveDisplacement("Pump 1", flow_rate_out=0.0, pump_head_in=0.0, press_out=0.0, pump_speed=0,
                                  displacement=0)


if __name__ == "__main__":
    print("Tank 1")
    print(tank1.level)
    print(tank1.static_tank_press)
    print(tank1.flow_out)

    print("\nTank 2")
    print(tank2.level)
    print(tank2.static_tank_press)
    print(tank2.flow_out)

    print("\nGate 1")
    print(gate1.Cv)
    print(gate1.flow_out)
    print(gate1.press_in)
    print(gate1.press_out)
    gate1.open()
    print(gate1.flow_out)
    print(gate1.press_out)

    print("\nGate 3")
    print(gate3.flow_out)
    print(gate3.press_in)
    print(gate3.press_out)
    gate3.press_in = gate1.press_out
    gate3.flow_in = gate1.flow_out
    print(gate3.flow_out)
    print(gate3.press_in)
    print(gate3.press_out)
    gate3.open()
    print(gate3.flow_out)
    print(gate3.press_in)
    print(gate3.press_out)

    print("\nGate 4")
    print(gate4.flow_out)
    print(gate4.press_in)
    print(gate4.press_out)
    gate2.open()
    gate4.press_in = gate2.press_out
    gate4.flow_in = gate2.flow_out
    print(gate4.flow_out)
    print(gate4.press_in)
    print(gate4.press_out)
    gate4.open()
    print(gate4.flow_out)
    print(gate4.press_in)
    print(gate4.press_out)

    print("\nGate 6")
    print(gate6.flow_out)
    print(gate6.press_in)
    print(gate6.press_out)
    gate6.press_in = gate3.press_out + gate4.press_out
    gate6.flow_in = gate3.flow_out + gate4.flow_out

    print(gate6.flow_out)
    print(gate6.press_in)
    print(gate6.press_out)
    gate6.open()
    print(gate6.flow_out)
    print(gate6.press_in)
    print(gate6.press_out)
    gate4.close()
    gate6.press_in = gate3.press_out + gate4.press_out
    gate6.flow_in = gate3.flow_out + gate4.flow_out
    gate6.press_out = gate6.press_in
    gate6.flow_out = gate6.flow_in
    print("Gate 4 closed")
    print(gate6.flow_out)
    print(gate6.press_in)
    print(gate6.press_out)
