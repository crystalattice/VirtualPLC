from valve.valve import Gate, Globe, Relief, Valve
import utility_formulas

"""Assumes valves in series, with the first supplied by a tank 6 feet above the valve with a pipe length of 10 feet.

Gravity flow rate from http://www.calctool.org/CALC/eng/civil/hazen-williams_g
"""


class GravityFlow:
    @staticmethod
    def test_grav_flow():
        flow_rate = utility_formulas.gravity_flow_rate(2, 1.67)
        assert flow_rate == 319.28008077388426

    @staticmethod
    def test_static_press():
        press = utility_formulas.static_press(14)
        assert press == 6.0606060606060606


class TestFirstValve:
    def test_input_press(self):
        valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                      press_in=utility_formulas.static_press(14))
        assert valve1.press_in == 6.0606060606060606

    def test_input_flow(self):
        valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                      press_in=utility_formulas.static_press(14))
        assert valve1.flow_in == 319.28008077388426

    def test_press_drop(self):
        valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                      press_in=utility_formulas.static_press(14))
        press_diff = valve1.press_drop(valve1.flow_in)
        assert press_diff == 2.5484942494744516

    def test_output_flow(self):
        valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                      press_in=utility_formulas.static_press(14))
        out_flow = valve1.valve_flow_out(valve1.Cv, valve1.deltaP)
        assert out_flow == 319.28008077388426

    def test_press_out(self):
        valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                      press_in=utility_formulas.static_press(14))
        press_out = valve1.press_in - valve1.press_drop(valve1.flow_in)
        assert press_out == 3.512111811131609


class TestSecondValve:
    def test_input_press(self):
        valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                      press_in=utility_formulas.static_press(14))
        valve2 = Globe("Valve 2", sys_flow_in=valve1.flow_out, press_in=valve1.press_out)
        assert valve2.press_in == 4.0445598845598845

    def test_press_drop(self):
        valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                      press_in=utility_formulas.static_press(14))
        press_diff = valve1.press_drop(valve1.flow_in)
        assert press_diff == 0.28444444444444444

    def test_output_flow(self):
        valve1 = Gate("Valve 1", flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
                      press_in=utility_formulas.static_press(14))
        out_flow = valve1.get_press_out(valve1.press_in)
        assert out_flow == 2.3155555555555556