import pytest
from pump.pump import Pump


class TestPumpSpeed:
    def test_speed_control_expected(self):
        p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
        speed = p.set_speed(750)
        assert speed == 750

    def test_speed_control_zero(self):
        p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
        speed = p.set_speed(0)
        assert speed == 0

    def test_speed_control_neg(self):
        p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
        with pytest.raises(ValueError) as excinfo:
            p.set_speed(-10)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Speed must be 0 or greater."

    def test_speed_control_non_int(self):
        p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
        with pytest.raises(TypeError) as excinfo:
            p.set_speed(12.5)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Integer values only."


class TestPumpReadSpeed:
    def test_cls_read_speed_expected(self):
        p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
        assert p.get_speed() == 300


class TestPumpReadPress:
    def test_cls_read_press(self):
        p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
        assert p.get_press() == 45.0


class TestPumpReadFlow:
    def test_cls_read_flow(self):
        p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
        assert p.get_flow() == 100.0


class TestPumpReadPower:
    def test_cls_read_power(self):
        # self.wattage = self.pump_power(self.flow_rate, self.diff_press(self.head, self.outlet_pressure))
        p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
        assert p.get_power() == 0.6224710060377437
