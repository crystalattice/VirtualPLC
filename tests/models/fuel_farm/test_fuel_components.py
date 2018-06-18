import pytest
import Models.FuelFarm.components as ffc


class TestComponents:
    def test_tank_full(self):
        assert ffc.tank1.level == 36.0
        assert ffc.tank1.static_tank_press == 13.109851301499999
        assert ffc.tank1.flow_out == 19542.86939891452

    def test_tank_half(self):
        ffc.tank1.level = 18
        assert ffc.tank1.level == 18.0
        assert ffc.tank1.static_tank_press == 6.5549256507499996
        assert ffc.tank1.flow_out == 19542.86939891452

    def test_tank_empty(self):
        ffc.tank1.level = 0
        assert ffc.tank1.level == 0.0
        assert ffc.tank1.static_tank_press == 0.0

    def test_tank_neg(self):
        ffc.tank1.level = -10
        assert ffc.tank1.level == 0.0
        assert ffc.tank1.static_tank_press == 0.0

    def test_tank_str(self):
        with pytest.raises(TypeError) as excinfo:
            ffc.tank1.level = "a"
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Numeric values only."

