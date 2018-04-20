import pytest
from ..valve import Valve


class TestValve:
    def test_calc_coeff_works(self):
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

    def test_press_drop(self):
        v = Valve()
        v.press_drop(100)
        assert v.deltaP == 11.111111111111112

    def test_sys_flow_rate(self):
        v = Valve()
        v.sys_flow_rate(v.Cv, v.deltaP)
        assert v.flow_out == 116.18950038622252

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
