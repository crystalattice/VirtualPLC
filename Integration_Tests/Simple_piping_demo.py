#!/bin/python

"""
Simple_piping_demo.py

Purpose: Creates a simple, closed-loop piping system, comprised of two pumps (one variable and one positive
displacement), each with inlet and outlet gate valves and a throttle valve, and a pressure relief valve on the outlet of
the positive displacement pump. Assumes 2 inch piping and a tank at the inlet of gate valve 1 that is 6 inches above the
valve and has 10 feet of piping.

Author: Cody Jackson

Date: 4/26/18
#################################
Version 0.1
    Initial build
"""
# Valve parameters: name="", sys_flow_in=0.0, position=0, flow_coeff=0.0, open_press=0, close_press=0
# Pump parameters: name="", flow_rate=0.0, pump_head_in=0.0, press_out=0.0, pump_speed=0, displacement=0.0
from pump.pump import CentrifPump, PositiveDisplacement
from valve.valve import Gate, Globe, Relief


# Pump 1 group (centrifugal)
centrif_pump1 = CentrifPump("Centrifugal Pump", pump_head_in=20)
out_valve1 = Gate("Centrifugal Pump outlet", flow_coeff=90, sys_flow_in=centrif_pump1.get_flow())
throttle1 = Globe("Centrifugal Pump throttle", flow_coeff=30, sys_flow_in=centrif_pump1.get_flow())
in_valve2 = Gate("Gear Pump inlet", flow_coeff=270, sys_flow_in=centrif_pump1.get_flow())


# Pump 2 group (gear)
gear_pump1 = PositiveDisplacement("Gear Pump", displacement=0.096, pump_head_in=throttle1.press_out, press_out=10)
out_valve2 = Gate("Gear Pump outlet", flow_coeff=270, sys_flow_in=gear_pump1.get_flow())
throttle2 = Globe("Gear Pump throttle", flow_coeff=30, sys_flow_in=gear_pump1.get_flow())
relief1 = Relief("Gear Pump relief", flow_coeff=0.71, open_press=150, close_press=125, sys_flow_in=gear_pump1.get_flow())
in_valve1 = Gate("Centrifugal Pump inlet", flow_coeff=90, sys_flow_in=48, press_in=2.6)


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
    print(centrif_pump1.get_speed_str())
    print(centrif_pump1.get_flow_str())
    print(centrif_pump1.get_press_str())
    print(centrif_pump1.get_power_str())

    print("\n***Gear Pump***")
    print(gear_pump1.get_speed_str())
    print(gear_pump1.get_flow_str())
    print(gear_pump1.get_press_str())
    print(gear_pump1.get_power_str())


def open_gates():
    """"Open all gate valves."""
    print("***Open shut-off valves***")
    for valve in gate_valves:
        valve.open()
        print(valve.read_position())


def get_gate_delta():
    """Check the pressure drop across the gate valves."""
    print("\n***Gate valve press drop***")
    centrif_out_gate = out_valve1.press_drop(centrif_pump1.get_flow())  # Input = centrif pump
    gear_in_gate = in_valve2.press_drop(throttle1.flow_out)  # Input = centrif pump throttle
    gear_out_gate = out_valve2.press_drop(gear_pump1.get_flow())  # Input = gear pump
    centrif_in_gate = in_valve1.press_drop(48)  # Input = Gravity drain flow rate

    print("Centrif Pump inlet: {:.2f}".format(centrif_in_gate))
    print("Centrif Pump outlet: {:.2f}".format(centrif_out_gate))
    print("Gear Pump inlet: {:.2f}".format(gear_in_gate))
    print("Gear Pump outlet: {:.2f}".format(gear_out_gate))


def get_gate_press_out():
    """Check the outlet pressure of gate valves."""
    print("\n***Gate valve outlet press***")
    centrif_out_gate = out_valve1.get_press_out(centrif_pump1.outlet_pressure)  # Input = centrif pump outlet
    gear_in_gate = in_valve2.get_press_out(throttle1.press_out)  # Input = centrif pump throttle
    gear_out_gate = out_valve2.get_press_out(gear_pump1.outlet_pressure)  # Input = gear pump outlet
    centrif_in_gate = in_valve1.get_press_out(throttle2.press_out)   # Input = gear pump throttle

    print("Centrif Pump inlet: {:.2f}".format(centrif_in_gate))
    print("Centrif Pump outlet: {:.2f}".format(centrif_out_gate))
    print("Gear Pump inlet: {:.2f}".format(gear_in_gate))
    print("Gear Pump outlet: {:.2f}".format(gear_out_gate))


def set_globe_valves(percent):
    """Open both throttle valves the same value."""
    print("\n***Set throttle valves***")
    for valve in globe_valves:
        valve.turn_handle(percent)
        print(valve.read_position())


def get_globe_delta():
    """Check the pressure drop across the globe valves."""
    print("\n***Globe valve press drop***")
    centrif_throttle = throttle1.press_drop(out_valve1.flow_out)
    gear_throttle = throttle2.press_drop(out_valve2.flow_out)

    print("Centrif Pump throttle: {:.2f}".format(centrif_throttle))  # Input = centrif pump gate out
    print("Gear Pump throttle: {:.2f}".format(gear_throttle))  # Input = gear pump gate out


def get_globe_press_out():
    """Check the outlet pressure of the throttle valves."""
    print("\n***Globe valve outlet press")
    centrif_globe_out = throttle1.get_press_out(out_valve1.press_out)
    gear_globe_out = throttle2.get_press_out(out_valve2.press_out)

    print("Centrif Pump throttle: {:.2f}".format(centrif_globe_out)) # Input = centrif pump gate out
    print("Gear Pump throttle: {:.2f}".format(gear_globe_out))  # Input = gear pump gate out


def start_centrif_pump(speed, flow, press_out):
    print("***Start centrifugal pump***")
    centrif_pump1.start_pump(speed, flow, press_out)
    print(centrif_pump1.get_speed_str())
    print(centrif_pump1.get_flow_str())
    print(centrif_pump1.get_press_str())
    print(centrif_pump1.get_power_str())


def start_gear_pump(speed):
    print("\n***Start gear pump***")
    gear_pump1.adjust_speed(speed)
    print(gear_pump1.get_speed_str())
    print(gear_pump1.get_flow_str())
    print(gear_pump1.get_press_str())
    print(gear_pump1.get_power_str())


if __name__ == "__main__":
    print("INITIAL CONDITIONS")
    # initial_state()

    print("\nOPEN VALVES")
    open_gates()
    get_gate_delta()
    get_gate_press_out()
    set_globe_valves(100)
    get_globe_delta()
    get_globe_press_out()

    print("\nSTART PUMPS")
    start_centrif_pump(1750, 75, 7.5)
    start_gear_pump(100)
    get_gate_delta()
    get_gate_press_out()
    get_globe_delta()
    get_globe_press_out()

    print("\n")
    print("Gate 1 out: {}".format(in_valve1.press_out))
    print("Centrif pump in: {}".format(centrif_pump1.head_in))
    print("Centrif pump out: {}".format(centrif_pump1.outlet_pressure))
    print("Gate 2 in: {}".format(out_valve1.press_in))
    print("Gate 2 out: {}".format(out_valve1.press_out))
    print("Globe 1 in: {}".format(throttle1.press_in))
    print("Globe 1 out: {}".format(throttle1.press_out))
    print("Gate 3 in: {}".format(in_valve2.press_in))
    print("Gate 3 out: {}".format(in_valve2.press_out))
    print("Gear pump in: {}".format(gear_pump1.head_in))
    print("Gear pump out: {}".format(gear_pump1.outlet_pressure))
    print("Gate 4 in: {}".format(out_valve2.press_in))
    print("Gate 4 out: {}".format(out_valve2.press_out))
    print("Gate 1 in: {}".format(in_valve1.press_in))
