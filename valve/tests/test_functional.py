import utility_formulas

from pump.pump import CentrifPump, PositiveDisplacement
from valve.valve import Gate, Globe, Relief

"""Assumes valves in series, with the first supplied by a tank 10 feet above the valve with a pipe length of 6 feet.
Water level is 4 feet above tank bottom; total water head = 14 feet.
"""

valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
              press_in=utility_formulas.static_press(14))
pump1 = CentrifPump("Pump 1")
throttle1 = Globe("Throttle 2", position=100, flow_coeff=21)
valve2 = Gate("Valve 2", flow_coeff=200)


def test_grav_flow():
    flow_rate = utility_formulas.gravity_flow_rate(2, 1.67)
    assert flow_rate == 319.28008077388426


def test_static_press():
    press = utility_formulas.static_press(14)
    assert press == 6.0606060606060606


def test_v1_input_press():
    assert valve1.press_in == 6.0606060606060606


def test_v1_input_flow():
    assert valve1.flow_in == 319.28008077388426


def test_v1_press_drop():
    press_diff = valve1.press_drop(valve1.flow_in)
    assert press_diff == 2.5484942494744516


def test_v1_output_flow():
    out_flow = valve1.valve_flow_out(valve1.Cv, valve1.deltaP)
    assert out_flow == 319.28008077388426


def test_v1_press_out():
    press_out = valve1.get_press_out(valve1.press_in)
    assert press_out == 3.512111811131609


def test_pump1_input_press():
    pump1.head_in = utility_formulas.press_to_head(valve1.press_out)
    assert pump1.head_in == 8.101304720057573


def test_pump1_start_pump():
    pump1.start_pump(1750, 50, 16)
    assert pump1.speed == 1750
    assert pump1.flow_rate_out == 50
    assert pump1.outlet_pressure == 16
    assert pump1.wattage == 0.11777800491229948


def test_t1_input_press():
    throttle1.press_in = pump1.outlet_pressure
    assert throttle1.press_in == 16


def test_t1_input_flow():
    throttle1.flow_in = pump1.flow_rate_out
    assert throttle1.flow_in == 50.0


def test_t1_press_drop():
    press_diff = throttle1.press_drop(throttle1.flow_in)
    assert press_diff == 5.668934240362812


def test_t1_output_flow():
    out_flow = throttle1.valve_flow_out(throttle1.Cv, throttle1.deltaP)
    assert out_flow == 50.0


def test_t1_press_out():
    press_out = throttle1.get_press_out(throttle1.press_in)
    assert press_out == 10.331065759637188


def test_v2_input_press():
    valve2.press_in = throttle1.press_out
    assert valve2.press_in == 10.331065759637188


def test_v2_input_flow():
    valve2.flow_in = throttle1.flow_out
    assert valve2.flow_in == 50.0


def test_v2_press_drop():
    press_diff = valve2.press_drop(valve2.flow_in)
    assert press_diff == 0.0625


def test_v2_output_flow():
    out_flow = valve2.valve_flow_out(valve2.Cv, valve2.deltaP)
    assert out_flow == 50.0


def test_v2_press_out():
    press_out = valve2.get_press_out(valve2.press_in)
    assert press_out == 10.268565759637188
