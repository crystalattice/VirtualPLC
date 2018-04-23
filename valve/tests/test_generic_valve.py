import pytest
from ..valve import Valve


class TestValveCoeff:
    # self.Cv = 15 * math.pow(diameter, 2)
    def test_calc_coeff_expected(self):
        v = Valve()
        v.calc_coeff(2)
        assert v.Cv == 60.0

    def test_calc_coeff_neg(self):
        v= Valve()
        v.calc_coeff(-2)
        assert v.Cv == 60.0

    def test_calc_coeff_zero(self):
        v = Valve()
        v.calc_coeff(0)
        assert v.Cv == 0.0

    def test_calc_coeff_str(self):
        """Checks for correct Exception thrown if non-number argument used"""
        v = Valve()
        with pytest.raises(TypeError):
            v.calc_coeff("a")

class TestValvePress:
    # x = (flow / self.Cv)
    # self.deltaP = math.pow(x, 2) * spec_grav
    def test_press_drop_expected(self):
        v = Valve()
        v.press_drop(100)
        assert v.deltaP == 11.111111111111112

    def test_press_drop_zero(self):
        v = Valve()
        v.press_drop(0)
        assert v.deltaP == 0

    def test_press_drop_neg(self):
        v = Valve()
        v.press_drop(-100)
        assert v.deltaP == 11.111111111111112

    def test_press_drop_str(self):
        """Checks for correct Exception thrown if non-number argument used"""
        v = Valve()
        with pytest.raises(TypeError):
            v.deltaP("a")

class TestValveFlow:
    # x = spec_grav / press_drop
    # self.flow_out = flow_coeff / math.sqrt(x)
    def test_sys_flow_rate_expected(self):
        v = Valve()
        v.sys_flow_rate(v.Cv, v.deltaP)
        assert v.flow_out == 116.18950038622252

    def test_sys_flow_rate_zero_coeff(self):
        v = Valve(flow_coeff=0.0)
        v.sys_flow_rate(v.Cv, v.deltaP)
        assert v.flow_out == 0.0

    def test_sys_flow_rate_zero_press(self):
        v = Valve(drop=0.0)
        with pytest.raises(ZeroDivisionError):
            v.sys_flow_rate(v.Cv, v.deltaP)

    def test_sys_flow_rate_neg_coeff(self):
        v = Valve(flow_coeff=-30.0)
        with pytest.raises(ValueError) as excinfo:
            v.sys_flow_rate(v.Cv, v.deltaP)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Input values must be > 0."

    def test_sys_flow_rate_neg_press(self):
        v = Valve(drop=-30.0)
        with pytest.raises(ValueError) as excinfo:
            v.sys_flow_rate(v.Cv, v.deltaP)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Input values must be > 0."

    def test_sys_flow_rate_str_press(self):
        v = Valve(drop="a")
        with pytest.raises(TypeError):
            v.sys_flow_rate(v.Cv, v.deltaP)

    def test_sys_flow_rate_str_coeff(self):
        v = Valve(flow_coeff="a")
        with pytest.raises(TypeError):
            v.sys_flow_rate(v.Cv, v.deltaP)

class TestValvePosition:
    def test_cls_get_position(self):
        v = Valve()
        assert v.cls_get_position() == 0

    def test_cls_change_position(self):
        v = Valve()
        v.cls_change_position(100)
        assert v.cls_get_position() == 100

    def test_open(self):
        v = Valve()
        v.open()
        assert v.cls_get_position() == 100

    def test_close(self):
        v = Valve(position=100)
        v.close()
        assert v.cls_get_position() == 0