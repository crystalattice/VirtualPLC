"""Same as test_parameters.py, except it checks values after throttle valve 1 is turned."""
from initial_conditions import *


# Turn Globe Valve 1
def test_throttle1_50_percent():
    throttle1.turn_handle(50)
    assert throttle1.press_in == 16.0
    assert throttle1.flow_in == 50.0
    assert throttle1.position == 50
    assert throttle1.deltaP == 1.417233560090703
    assert throttle1.flow_out == 25.0
    assert throttle1.press_out == 14.582766439909298


def test_valve2():
    valve2.flow_in = throttle1.flow_out
    valve2.flow_out = valve2.flow_in
    valve2.press_in = throttle1.press_out
    valve2.press_drop(valve2.flow_out)
    valve2.get_press_out(valve2.press_in)
    assert valve2.press_in == 14.582766439909298
    assert valve2.flow_in == 25.0
    assert valve2.deltaP == 0.015625
    assert valve2.press_out == 14.567141439909298
    assert valve2.flow_out == 25.0


def test_valve3():
    valve3.flow_in = valve2.flow_out
    valve3.flow_out = valve3.flow_in
    valve3.press_in = valve2.press_out
    valve3.press_drop(valve3.flow_out)
    valve3.get_press_out(valve3.press_in)
    assert valve3.press_in == 14.567141439909298
    assert valve3.flow_in == 25.0
    assert valve3.deltaP == 0.015625
    assert valve3.press_out == 14.551516439909298
    assert valve3.flow_out == 25.0


def test_gear_pump():
    pump2.head_in = utility_formulas.press_to_head(valve3.press_out)
    assert pump2.head_in == 33.5656366192537