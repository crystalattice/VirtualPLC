import pytest
from pump.pump import Pump


class TestPumpSpeed:
    def test_speed_control_expected(self):
        p = Pump("", 100, 300, 70, 45, .25)
        p.speed_control(750)
        assert p.cls_read_speed() == 750

    def test_speed_control_zero(self):
        p = Pump("", 100, 300, 70, 45, .25)
        p.speed_control(0)
        assert p.cls_read_speed() == 0

    def test_speed_control_neg(self):
        p = Pump("", 100, 300, 70, 45, .25)
        with pytest.raises(ValueError) as excinfo:
            p.speed_control(-10)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Speed must be 0 or greater."

    def test_speed_control_non_int(self):
        p = Pump("", 100, 300, 70, 45, .25)
        with pytest.raises(TypeError) as excinfo:
            p.speed_control(12.5)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Integer values only."

class TestPumpLaws:
    def test_pump_laws_expected(self):
        p = Pump("", 100, 300, 70, 45, .25)
        p.pump_laws(100)
        assert p.flow_rate == 222.22222222222223
        assert p.outlet_pressure == 345.67901234567904
        assert p.power == 2.743484224965707

    def test_pump_laws_zero(self):
        p = Pump("", 100, 300, 70, 45, .25)
        p.pump_laws(0)
        assert p.flow_rate == 0.0
        assert p.outlet_pressure == 0.0
        assert p.power == 0.0

    def test_pump_laws_neg(self):
        p = Pump("", 100, 300, 70, 45, .25)
        with pytest.raises(ValueError) as excinfo:
            p.speed_control(-120)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Speed must be 0 or greater."

    def test_pump_laws_non_int(self):
        p = Pump("", 100, 300, 70, 45, .25)
        with pytest.raises(TypeError) as excinfo:
            p.speed_control(85.3)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Integer values only."

class TestPumpReadSpeed:
    def test_cls_read_speed_expected(self):
        p = Pump("", 100, 300, 70, 45, .25)
        assert p.cls_read_speed() == 45

class TestPumpReadPress:
    def test_cls_read_press(self):
        p = Pump("", 100, 300, 70, 45, .25)
        assert p.cls_read_press() == 70.0

class TestPumpReadFlow:
    def test_cls_read_flow(self):
        p = Pump("", 100, 300, 70, 45, .25)
        assert p.cls_read_flow() == 100.0

class TestPumpReadPower:
    def test_cls_read_power(self):
        p = Pump("", 100, 300, 70, 45, .25)
        assert p.cls_read_power() == 0.25
