#!/bin/python

"""
Simple_piping_demo.py

Purpose: Creates a simple, closed-loop piping system, comprised of two pumps (one variable and one positive
displacement), each with inlet and outlet gate valves and a throttle valve, and a pressure relief valve on the outlet of
the positive displacement pump. Assumes 2 inch piping.

Author: Cody Jackson

Date: 4/26/18
#################################
Version 0.1
    Initial build
"""
# Valve parameters: name="", sys_flow_in=0.0, position=0, flow_coeff=0.0, drop=0.0, open_press=0, close_press=0
# Pump parameters: name="", flow_rate=0.0, pump_head_in=0.0, press_out=0.0, pump_speed=0, displacement=0.0
from pump.pump import CentrifPump, PositiveDisplacement
from valve.valve import Gate, Globe, Relief


# Pump 1 group (centrifugal)
in_valve1 = Gate("Centrifugal Pump inlet", flow_coeff=90)
out_valve1 = Gate("Centrifugal Pump outlet", flow_coeff=90)
centrif_pump1 = CentrifPump("Centrifugal Pump", pump_head_in=20)
throttle1 = Globe("Centrifugal Pump throttle", flow_coeff=30)

# Pump 2 group (gear)
in_valve2 = Gate("Gear Pump inlet", flow_coeff=270)
out_valve2 = Gate("Gear Pump outlet", flow_coeff=270)
gear_pump1 = PositiveDisplacement("Gear Pump", displacement=0.096, pump_head_in=throttle1.press_out, press_out=10)
throttle2 = Globe("Gear Pump throttle", flow_coeff=30)
relief1 = Relief("Gear Pump relief", flow_coeff=0.71, open_press=150, close_press=125)

gate_valves = [in_valve1, out_valve1, in_valve2, out_valve2]
globe_valves = [throttle1, throttle2]


def initial_state():
    """Confirm zero state."""
    print("***Gate Valves***")
    for valve in gate_valves:
        print(valve.read_position())

    print("\n***Globe Valves***")
    for valve in globe_valves:
        print(valve.read_position())

    print("\n***Relief Valve***")
    print(relief1.read_position())

    print("\n***Centrifugal Pump***")
    print(centrif_pump1.get_speed())
    print(centrif_pump1.get_flowrate())
    print(centrif_pump1.get_pressure())
    print(centrif_pump1.get_power())

    print("\n***Gear Pump***")
    print(gear_pump1.get_speed())
    print(gear_pump1.get_flowrate())
    print(gear_pump1.get_pressure())
    print(gear_pump1.get_power())


def open_gates():
    """"Open all gate valves."""
    print("***Open shut-off valves***")
    for valve in gate_valves:
        valve.open()
        print(valve.read_position())


def set_globe_valves(percent):
    """Open both throttle valves the same value."""
    print("\n***Set throttle valves***")
    for valve in globe_valves:
        valve.turn_handle(percent)
        print(valve.read_position())


def start_centrif_pump(speed, flow, press_out):
    print("***Start centrifugal pump***")
    centrif_pump1.start_pump(speed, flow, press_out)
    print(centrif_pump1.get_speed())
    print(centrif_pump1.get_flowrate())
    print(centrif_pump1.get_pressure())
    print(centrif_pump1.get_power())


def start_gear_pump(speed):
    print("\n***Start gear pump***")
    gear_pump1.adjust_speed(speed)
    print(gear_pump1.get_speed())
    print(gear_pump1.get_flowrate())
    print(gear_pump1.get_pressure())
    print(gear_pump1.get_power())


if __name__ == "__main__":
    print("INITIAL CONDITIONS")
    initial_state()

    print("\nOPEN VALVES")
    open_gates()
    set_globe_valves(100)

    print("\nSTART PUMPS")
    start_centrif_pump(1750, 75, 7.5)
    start_gear_pump(100)
