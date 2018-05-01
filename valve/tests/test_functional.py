from valve.valve import Gate, Globe, Relief

"""Assumes valves in series, with the first supplied by a tank 6 feet above the valve with a pipe length of 10 feet.

Gravity flow rate from http://www.calctool.org/CALC/eng/civil/hazen-williams_g
"""


class TestFirstGate:
    def test_input_flow(self):
        valve1 = Gate("Valve 1", flow_coeff=90, sys_flow_in=48)
        assert valve1.press_in == 2.6
