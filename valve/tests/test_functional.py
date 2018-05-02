from valve.valve import Gate, Globe, Relief

"""Assumes valves in series, with the first supplied by a tank 6 feet above the valve with a pipe length of 10 feet.

Gravity flow rate from http://www.calctool.org/CALC/eng/civil/hazen-williams_g
"""


class TestFirstValve:
    def test_input_flow(self):
        valve1 = Gate("Valve 1", flow_coeff=90, sys_flow_in=48, press_in=2.6)
        assert valve1.press_in == 2.6

    def test_press_drop(self):
        valve1 = Gate("Valve 1", flow_coeff=90, sys_flow_in=48, press_in=2.6)
        press_diff = valve1.press_drop(valve1.flow_in)
        assert press_diff == 0.28444444444444444

    def test_output_flow(self):
        valve1 = Gate("Valve 1", flow_coeff=90, sys_flow_in=48, press_in=2.6)
        out_flow = valve1.get_press_out(valve1.press_in)
        assert out_flow == 2.3155555555555556


class TestSecondValve:
    def test_input_flow(self):
        valve1 = Gate("Valve 1", flow_coeff=90, sys_flow_in=48, press_in=2.6)
        valve2 = Globe("Valve 2", )
        assert valve1.press_in == 2.6

    def test_press_drop(self):
        valve1 = Gate("Valve 1", flow_coeff=90, sys_flow_in=48, press_in=2.6)
        press_diff = valve1.press_drop(valve1.flow_in)
        assert press_diff == 0.28444444444444444

    def test_output_flow(self):
        valve1 = Gate("Valve 1", flow_coeff=90, sys_flow_in=48, press_in=2.6)
        out_flow = valve1.get_press_out(valve1.press_in)
        assert out_flow == 2.3155555555555556