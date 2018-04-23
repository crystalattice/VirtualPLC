import pytest
from pump.pump import CentrifPump


class TestPumpSpeed():
    def test_get_speed_expected(self):
        p = CentrifPump(pump_speed=450)
        assert p.get_speed() == "The pump is running at 450 rpm."

    def test_get_speed_zero(self):
        p = CentrifPump(pump_speed=0)
        assert p.get_speed() == "The pump is stopped."


class TestFlowrate:
    def test_get_flowrate(self):
        p = CentrifPump(flow_rate=100.0)
        assert p.get_flowrate() == "The pump output flow rate is 100.0 gpm."


class TestPressure:
    def test_get_pressure(self):
        p = CentrifPump(press_out=55.5)
        assert p.get_pressure() == "The pump pressure is 55.5 psi."


class TestPower:
    def test_get_power(self):
        p = CentrifPump(power=0.12)
        assert p.get_power() == "The power usage for the pump is 0.12 kW."


class TestChangeSpeed:
    def test_change_speed_expected(self):
        p = CentrifPump("", 100, 300, 70, 45, .25)
        p.change_speed(500)
        assert p.get_speed() == "The pump is running at 500 rpm."
        assert p.get_flowrate() == "The pump output flow rate is 1111.111111111111 gpm."
        assert p.get_pressure() == "The pump pressure is 8641.975308641975 psi."
        assert p.get_power() == "The power usage for the pump is 342.9355281207133 kW."

    def test_change_speed_neg(self):
        p = CentrifPump("", 100, 300, 70, 45, .25)
        with pytest.raises(ValueError) as excinfo:
            p.change_speed(-100)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Speed must be 0 or greater."

    def test_change_speed_zero(self):
        p = CentrifPump("", 100, 300, 70, 45, .25)
        p.change_speed(0)
        assert p.get_speed() == "The pump is stopped."
        assert p.get_flowrate() == "The pump output flow rate is 0.0 gpm."
        assert p.get_pressure() == "The pump pressure is 0.0 psi."
        assert p.get_power() == "The power usage for the pump is 0.0 kW."

    def test_change_speed_non_int(self):
        p = CentrifPump("", 100, 300, 70, 45, .25)
        with pytest.raises(TypeError) as excinfo:
            p.change_speed("a")
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Integer values only."