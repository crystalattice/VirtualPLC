import pytest
from pump.pump import PositiveDisplacement


class TestSpeed:
    def test_get_speed(self):
        p = PositiveDisplacement()
        assert p.get_speed() == "The pump is stopped."


class TestFlow:
    def test_get_flowrate(self):
        p = PositiveDisplacement(flow_rate=35)
        assert p.get_flowrate() == "The pump outlet flow rate is 35.0 gpm."


class TestPress:
    def test_get_pressure(self):
        p = PositiveDisplacement(press_out=24.5)
        assert p.get_pressure() == "The pump pressure is 24.5 psi."


class TestPower:
    def test_get_power(self):
        p = PositiveDisplacement(power=0.45)
        assert p.get_power() == "The power usage for the pump is 0.45 kW."


class TestSpeedChange:
    def test_change_speed_expected(self):
        p = PositiveDisplacement()
        p.adjust_speed(25)

