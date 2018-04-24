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
        p = PositiveDisplacement(hp=0.45)
        assert p.get_power() == "The power usage for the pump is 335.5649424 W."


class TestHpCoeff:
    def test_set_hp_coeff(self):
        p = PositiveDisplacement(pump_speed=120, hp=0.12)
        assert p.set_hp_coeff() == 0.001


class TestAdjustSpeed:
    def test_adjust_speed_expected(self):
        p = PositiveDisplacement("", 100, 0, 0, 75, 10, 0.09, 0.2)
        p.adjust_speed(25)
        assert p.flow_rate == 2.25
        assert p.wattage == 3728.4993600000003
        assert p.speed == 25

