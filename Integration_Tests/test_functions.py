import utility_formulas

from pump.pump import CentrifPump, PositiveDisplacement
from valve.valve import Gate, Globe, Relief

"""Assumes valves in series, with the first supplied by a tank 10 feet above the valve with a pipe length of 6 feet.
Water level is 4 feet above tank bottom; total water head = 14 feet.
"""

valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
              press_in=utility_formulas.static_press(14))
pump1 = CentrifPump("Pump 1")
throttle1 = Globe("Throttle 1", position=100, flow_coeff=21)
valve2 = Gate("Valve 2", flow_coeff=200)
valve3 = Gate("Valve 3", flow_coeff=200)
pump2 = PositiveDisplacement("Gear Pump", displacement=0.096, press_out=30)
relief1 = Relief("Relief 1", open_press=60, close_press=55)
recirc1 = Globe("Throttle 2", position=100, flow_coeff=21)
valve4 = Gate("Valve 4", flow_coeff=200)


# Utility functions
def test_grav_flow():
    flow_rate = utility_formulas.gravity_flow_rate(2, 1.67)
    assert flow_rate == 319.28008077388426


def test_static_press():
    press = utility_formulas.static_press(14)
    assert press == 6.0606060606060606


# Gate Valve 1
def test_v1_input_press():
    assert valve1.press_in == 6.0606060606060606


def test_v1_input_flow():
    assert valve1.flow_out == 319.28008077388426


def test_v1_press_drop():
    press_diff = valve1.press_drop(valve1.flow_out)
    assert press_diff == 2.5484942494744516


def test_v1_output_flow():
    out_flow = valve1.valve_flow_out(valve1.Cv, valve1.deltaP)
    assert out_flow == 319.28008077388426


def test_v1_press_out():
    press_out = valve1.get_press_out(valve1.press_in)
    assert press_out == 3.512111811131609


# Centrifugal Pump
def test_pump1_input_press():
    pump1.head_in = utility_formulas.press_to_head(valve1.press_out)
    assert pump1.head_in == 8.101304720057573


def test_pump1_start_pump():
    pump1.start_pump(1750, 50, 16)
    assert pump1.speed == 1750
    assert pump1.flow_rate_out == 50
    assert pump1.outlet_pressure == 16
    assert pump1.wattage == 0.11777800491229948


# Globe valve 1
def test_t1_input_press():
    throttle1.press_in = pump1.outlet_pressure
    assert throttle1.press_in == 16


def test_t1_input_flow():
    throttle1.flow_out = pump1.flow_rate_out
    assert throttle1.flow_out == 50.0


def test_t1_press_drop():
    press_diff = throttle1.press_drop(throttle1.flow_out)
    assert press_diff == 5.668934240362812


def test_t1_output_flow():
    out_flow = throttle1.valve_flow_out(throttle1.Cv, throttle1.deltaP)
    assert out_flow == 50.0


def test_t1_press_out():
    press_out = throttle1.get_press_out(throttle1.press_in)
    assert press_out == 10.331065759637188


# Gate Valve 2
def test_v2_input_press():
    valve2.press_in = throttle1.press_out
    assert valve2.press_in == 10.331065759637188


def test_v2_input_flow():
    valve2.flow_out = throttle1.flow_out
    assert valve2.flow_out == 50.0


def test_v2_press_drop():
    press_diff = valve2.press_drop(valve2.flow_out)
    assert press_diff == 0.0625


def test_v2_output_flow():
    out_flow = valve2.valve_flow_out(valve2.Cv, valve2.deltaP)
    assert out_flow == 50.0


def test_v2_press_out():
    press_out = valve2.get_press_out(valve2.press_in)
    assert press_out == 10.268565759637188


# Gate Valve 3
def test_v3_input_press():
    valve3.press_in = valve2.press_out
    assert valve3.press_in == 10.268565759637188


def test_v3_input_flow():
    valve3.flow_out = valve2.flow_out
    assert valve3.flow_out == 50.0


def test_v3_press_drop():
    press_diff = valve3.press_drop(valve3.flow_out)
    assert press_diff == 0.0625


def test_v3_output_flow():
    out_flow = valve3.valve_flow_out(valve3.Cv, valve3.deltaP)
    assert out_flow == 50.0


def test_v3_press_out():
    press_out = valve3.get_press_out(valve3.press_in)
    assert press_out == 10.206065759637188


# Gear Pump
def test_pump2_input_press():
    pump2.head_in = utility_formulas.press_to_head(valve3.press_out)
    assert pump2.head_in == 23.542088964737797


def test_pump2_output():
    pump2.adjust_speed(300)
    assert pump2.speed == 300
    assert pump2.flow_rate_out == 28.8
    assert pump2.wattage == 0.10753003776038036


# Relief Valve 1
def test_relief1_input_press():
    relief1.press_in = pump2.outlet_pressure
    assert relief1.press_in == 30


# Globe Valve 2
def test_t2_input_press():
    recirc1.press_in = pump2.outlet_pressure
    assert recirc1.press_in == 30


def test_t2_input_flow():
    recirc1.flow_out = pump2.flow_rate_out
    assert recirc1.flow_out == 28.8


def test_2_press_drop():
    press_diff = recirc1.press_drop(recirc1.flow_out)
    assert press_diff == 1.8808163265306124


def test_t2_output_flow():
    out_flow = recirc1.valve_flow_out(recirc1.Cv, recirc1.deltaP)
    assert out_flow == 28.8


def test_t2_press_out():
    press_out = recirc1.get_press_out(recirc1.press_in)
    assert press_out == 28.119183673469387


# Gate Valve 4
def test_v4_input_press():
    valve4.press_in = recirc1.press_out
    assert valve4.press_in == 28.119183673469387


def test_v4_input_flow():
    valve4.flow_out = recirc1.flow_out
    assert valve4.flow_out == 28.8


def test_v4_press_drop():
    press_diff = valve4.press_drop(valve4.flow_out)
    assert press_diff == 0.020736000000000004


def test_v4_output_flow():
    out_flow = valve4.valve_flow_out(valve4.Cv, valve4.deltaP)
    assert out_flow == 28.800000000000004


def test_v4_press_out():
    press_out = valve4.get_press_out(valve4.press_in)
    assert press_out == 28.098447673469387
