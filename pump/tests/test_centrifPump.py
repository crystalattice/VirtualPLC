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
        p = CentrifPump(hp=0.12)
        assert p.get_power() == "The power usage for the pump is 89.48398464 W."


class TestChangeSpeed:
    def test_adjust_speed_expected(self):
        p = CentrifPump("", 100, 12, 45, 300, 0.12, 0, 0)
        p.adjust_speed(500)
        assert p.get_speed() == "The pump is running at 500 rpm."
        assert p.get_flowrate() == "The pump output flow rate is 166.66666666666669 gpm."
        assert p.get_pressure() == "The pump pressure is 125.00000000000001 psi."
        assert p.get_power() == "The power usage for the pump is 414.2777066666668 W."

    def test_adjust_speed_neg(self):
        p = CentrifPump("", 100, 12, 45, 300, 0.12, 0, 0)
        with pytest.raises(ValueError) as excinfo:
            p.adjust_speed(-100)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Speed must be 0 or greater."

    def test_adjust_speed_zero(self):
        p = CentrifPump("", 100, 12, 45, 300, 0.12, 0, 0)
        p.adjust_speed(0)
        assert p.get_speed() == "The pump is stopped."
        assert p.get_flowrate() == "The pump output flow rate is 0.0 gpm."
        assert p.get_pressure() == "The pump pressure is 0.0 psi."
        assert p.get_power() == "The power usage for the pump is 0.0 W."

    def test_adjust_speed_non_int(self):
        p = CentrifPump("", 100, 12, 45, 300, 0.12, 0, 0)
        with pytest.raises(TypeError) as excinfo:
            p.adjust_speed("a")
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Integer values only."


class TestPumpLaws:
    def test_pump_laws_expected(self):
        p = CentrifPump("", 100, 12, 45, 300, 0.12, 0, 0)
        p.pump_laws(100)
        assert p.flow_rate == 33.33333333333333
        assert p.outlet_pressure == 5.0
        assert p.wattage == 3.3142216533333326

    def test_pump_laws_zero(self):
        p = CentrifPump("", 100, 12, 45, 300, 0.12, 0, 0)
        p.pump_laws(0)
        assert p.flow_rate == 0.0
        assert p.outlet_pressure == 0.0
        assert p.wattage == 0.0

    def test_pump_laws_neg(self):
        p = CentrifPump("", 100, 12, 45, 300, 0.12, 0, 0)
        with pytest.raises(ValueError) as excinfo:
            p.set_speed(-120)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Speed must be 0 or greater."

    def test_pump_laws_non_int(self):
        p = CentrifPump("", 100, 12, 45, 300, 0.12, 0, 0)
        with pytest.raises(TypeError) as excinfo:
            p.set_speed(85.3)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Integer values only."