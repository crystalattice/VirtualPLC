import pytest
import Models.FuelFarm.components as ffc
import Models.FuelFarm.functionality as fff


class TestTank:
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
        assert ffc.tank1.flow_out == 0.0

    def test_tank_neg(self):
        ffc.tank1.level = -10
        assert ffc.tank1.level == 0.0
        assert ffc.tank1.static_tank_press == 0.0
        assert ffc.tank1.flow_out == 0.0

    def test_tank_str(self):
        with pytest.raises(TypeError) as excinfo:
            ffc.tank1.level = "a"
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Numeric values only."


class TestGate1:
    @staticmethod
    def test_gate1_closed():
        fff.gate1_close()
        assert ffc.gate1.position == 0
        assert ffc.gate1.flow_in == 19542.86939891452
        assert ffc.gate1.press_in == 13.109851301499999
        assert ffc.gate1.flow_out == 0.0
        assert ffc.gate1.press_out == 0.0

    @staticmethod
    def test_gate1_open():
        fff.gate1_open()
        assert ffc.gate1.position == 100
        assert ffc.gate1.flow_in == 19542.86939891452
        assert ffc.gate1.press_in == 13.109851301499999
        assert ffc.gate1.flow_out == 19542.86939891452
        assert ffc.gate1.press_out == 13.109851301499999


class TestGate2:
    @staticmethod
    def test_gate2_closed():
        fff.gate2_close()
        assert ffc.gate2.position == 0
        assert ffc.gate2.flow_in == 19542.86939891452
        assert ffc.gate2.press_in == 13.109851301499999
        assert ffc.gate2.flow_out == 0.0
        assert ffc.gate2.press_out == 0.0

    @staticmethod
    def test_gate2_open():
        fff.gate2_open()
        assert ffc.gate2.position == 100
        assert ffc.gate2.flow_in == 19542.86939891452
        assert ffc.gate2.press_in == 13.109851301499999
        assert ffc.gate2.flow_out == 19542.86939891452
        assert ffc.gate2.press_out == 13.109851301499999


class TestGate3:
    def test_gate3_no_flow(self):
        fff.gate1_close()
        fff.gate4_close()
        assert ffc.gate1.position == 0
        assert ffc.gate4.position == 0
        assert ffc.gate3.flow_in == 0.0
        assert ffc.gate3.press_in == 0.0
        assert ffc.gate3.flow_out == 0.0
        assert ffc.gate3.press_out == 0.0

    def test_gate3_flow_in(self):
        fff.gate2_close()
        assert ffc.gate2.position == 0
        assert ffc.gate2.flow_out == 0.0
        assert ffc.gate2.press_out == 0.0

        fff.gate4_close()
        assert ffc.gate4.position == 0
        assert ffc.gate4.press_out == 0.0
        assert ffc.gate4.flow_out == 0.0

        fff.gate1_open()
        assert ffc.gate1.position == 100
        assert ffc.gate1.flow_out == 19542.86939891452
        assert ffc.gate1.press_out == 13.109851301499999

        fff.gate3_close()
        assert ffc.gate3.flow_in == 19542.86939891452
        assert ffc.gate3.press_in == 13.109851301499999
        assert ffc.gate3.flow_out == 0.0
        assert ffc.gate3.press_out == 0.0

        fff.gate1_close()
        assert ffc.gate1.position == 0
        assert ffc.gate1.flow_out == 0.0
        assert ffc.gate1.press_out == 0.0
        assert ffc.gate3.flow_in == 0.0
        assert ffc.gate3.press_in == 0.0
        assert ffc.gate3.flow_out == 0.0
        assert ffc.gate3.press_out == 0.0

    def test_gate3_operation(self):
        fff.gate1_open()
        assert ffc.gate1.position == 100
        assert ffc.gate1.flow_out == 19542.86939891452
        assert ffc.gate1.press_out == 13.109851301499999

        fff.gate2_close()
        assert ffc.gate2.position == 0
        assert ffc.gate2.flow_out == 0.0
        assert ffc.gate2.press_out == 0.0

        fff.gate4_close()
        assert ffc.gate4.position == 0
        assert ffc.gate4.press_out == 0.0
        assert ffc.gate4.flow_out == 0.0

        fff.gate3_open()
        assert ffc.gate3.position == 100
        assert ffc.gate3.flow_in == 19542.86939891452
        assert ffc.gate3.press_in == 13.109851301499999
        assert ffc.gate3.flow_out == 19542.86939891452
        assert ffc.gate3.press_out == 13.109851301499999

        fff.gate6_close()
        assert ffc.gate6.flow_in == 19542.86939891452
        assert ffc.gate6.press_in == 13.109851301499999
        assert ffc.gate4.flow_in == 19542.86939891452
        assert ffc.gate4.press_in == 13.109851301499999

        fff.gate3_close()
        assert ffc.gate3.position == 0
        assert ffc.gate3.flow_out == 0.0
        assert ffc.gate3.press_out == 0.0
        assert ffc.gate6.flow_in == 0.0
        assert ffc.gate6.press_in == 0.0
        assert ffc.gate4.flow_in == 0.0
        assert ffc.gate4.press_in == 0.0

    def test_gate3_gate4(self):
        fff.gate1_open()
        assert ffc.gate1.position == 100
        assert ffc.gate1.flow_out == 19542.86939891452
        assert ffc.gate1.press_out == 13.109851301499999

        fff.gate2_open()
        assert ffc.gate2.position == 100
        assert ffc.gate2.flow_out == 19542.86939891452
        assert ffc.gate2.press_out == 13.109851301499999

        fff.gate4_open()
        assert ffc.gate4.position == 100
        assert ffc.gate4.flow_in == 19542.86939891452
        assert ffc.gate4.press_in == 13.109851301499999
        assert ffc.gate4.flow_out == 19542.86939891452
        assert ffc.gate4.press_out == 13.109851301499999

        fff.gate3_open()
        assert ffc.gate3.position == 100
        assert ffc.gate3.flow_in == 19542.86939891452
        assert ffc.gate3.press_in == 13.109851301499999
        assert ffc.gate3.flow_out == 19542.86939891452
        assert ffc.gate3.press_out == 13.109851301499999
        assert ffc.gate6.flow_in == 39085.73879782904
        assert ffc.gate6.press_in == 13.109851301499999

        fff.gate3_close()
        assert ffc.gate3.position == 0
        assert ffc.gate3.flow_out == 0.0
        assert ffc.gate3.press_out == 0.0
        assert ffc.gate6.flow_in == 19542.86939891452
        assert ffc.gate6.press_in == 13.109851301499999
        assert ffc.gate4.flow_in == 19542.86939891452
        assert ffc.gate4.press_in == 13.109851301499999


class TestGate4:
    def test_gate4_no_flow(self):
        fff.gate1_close()
        fff.gate2_close()
        fff.gate3_close()
        fff.gate4_close()
        assert ffc.gate1.position == 0
        assert ffc.gate2.position == 0
        assert ffc.gate4.position == 0
        assert ffc.gate3.position == 0
        assert ffc.gate4.flow_in == 0.0
        assert ffc.gate4.press_in == 0.0
        assert ffc.gate4.flow_out == 0.0
        assert ffc.gate4.press_out == 0.0

    def test_gate4_flow_in(self):
        fff.gate1_close()
        fff.gate2_open()
        fff.gate3_close()
        assert ffc.gate1.position == 0
        assert ffc.gate2.position == 100
        assert ffc.gate3.position == 0
        assert ffc.gate4.flow_in == 19542.86939891452
        assert ffc.gate4.press_in == 13.109851301499999
        assert ffc.gate4.flow_out == 0.0
        assert ffc.gate4.press_out == 0.0
        fff.gate2_close()
        assert ffc.gate2.position == 0
        assert ffc.gate4.flow_in == 0.0
        assert ffc.gate4.press_in == 0.0
        assert ffc.gate4.flow_out == 0.0
        assert ffc.gate4.press_out == 0.0

    def test_gate4_operation(self):
        fff.gate1_close()
        fff.gate3_close()
        fff.gate2_open()
        fff.gate4_open()
        assert ffc.gate1.position == 0
        assert ffc.gate2.position == 100
        assert ffc.gate3.position == 0
        assert ffc.gate4.position == 100
        assert ffc.gate4.flow_in == 19542.86939891452
        assert ffc.gate4.press_in == 13.109851301499999
        assert ffc.gate4.flow_out == 19542.86939891452
        assert ffc.gate4.press_out == 13.109851301499999
        assert ffc.gate6.flow_in == 19542.86939891452
        assert ffc.gate6.press_in == 13.109851301499999
        assert ffc.gate3.flow_in == 19542.86939891452
        assert ffc.gate3.press_in == 13.109851301499999
        fff.gate4_close()
        assert ffc.gate4.position == 0
        assert ffc.gate4.flow_out == 0.0
        assert ffc.gate4.press_out == 0.0
        assert ffc.gate6.flow_in == 0.0
        assert ffc.gate6.press_in == 0.0
        assert ffc.gate3.flow_in == 0.0
        assert ffc.gate3.press_in == 0.0

    def test_gate4_gate3(self):
        fff.gate1_open()
        fff.gate2_open()
        fff.gate3_open()
        fff.gate4_open()
        assert ffc.gate1.position == 100
        assert ffc.gate2.position == 100
        assert ffc.gate3.position == 100
        assert ffc.gate4.position == 100
        assert ffc.gate4.flow_in == 19542.86939891452
        assert ffc.gate4.press_in == 13.109851301499999
        assert ffc.gate4.flow_out == 19542.86939891452
        assert ffc.gate4.press_out == 13.109851301499999
        assert ffc.gate6.flow_in == 39085.73879782904
        assert ffc.gate6.press_in == 13.109851301499999
        assert ffc.gate3.flow_in == 19542.86939891452
        assert ffc.gate3.press_in == 13.109851301499999
        fff.gate4_close()
        assert ffc.gate4.position == 0
        assert ffc.gate4.flow_out == 0.0
        assert ffc.gate4.press_out == 0.0
        assert ffc.gate6.flow_in == 19542.86939891452
        assert ffc.gate6.press_in == 13.109851301499999
        assert ffc.gate3.flow_in == 19542.86939891452
        assert ffc.gate3.press_in == 13.109851301499999


class TestGate5:
    def test_gate5_tank1(self):
        fff.gate1_open()
        assert ffc.gate1.position == 100
        assert ffc.gate1.flow_out == 19542.86939891452
        assert ffc.gate1.press_out == 13.109851301499999

        fff.gate2_close()
        assert ffc.gate2.position == 0
        assert ffc.gate2.flow_out == 0.0
        assert ffc.gate2.press_out == 0.0

        fff.gate3_close()
        assert ffc.gate3.position == 0
        assert ffc.gate3.flow_in == 19542.86939891452
        assert ffc.gate3.press_in == 13.109851301499999
        assert ffc.gate3.flow_out == 0.0
        assert ffc.gate3.press_out == 0.0

        fff.gate4_close()
        assert ffc.gate4.position == 0
        assert ffc.gate4.flow_in == 0.0
        assert ffc.gate4.press_in == 0.0
        assert ffc.gate4.flow_out == 0.0
        assert ffc.gate4.press_out == 0.0

        fff.gate5_open()
        assert ffc.gate5.position == 100
        assert ffc.gate5.flow_in == 19542.86939891452
        assert ffc.gate5.press_in == 13.109851301499999
        assert ffc.gate5.flow_out == 19542.86939891452
        assert ffc.gate5.press_out == 13.109851301499999
        assert ffc.pump1.head_in == 30.24018195875

        fff.gate1_close()
        assert ffc.gate1.position == 0
        assert ffc.gate1.flow_out == 0.0
        assert ffc.gate1.press_out == 0.0

        assert ffc.gate3.position == 0
        assert ffc.gate3.flow_in == 0.0
        assert ffc.gate3.press_in == 0.0
        assert ffc.gate3.flow_out == 0.0
        assert ffc.gate3.press_out == 0.0

        fff.gate5_open()  # Resets values
        assert ffc.gate5.position == 100
        assert ffc.gate5.flow_in == 0.0
        assert ffc.gate5.press_in == 0.0
        assert ffc.gate5.flow_out == 0.0
        assert ffc.gate5.press_out == 0.0
        assert ffc.pump1.head_in == 0.0

    def test_gate5_tank2(self):
        fff.gate1_close()
        assert ffc.gate1.position == 0
        assert ffc.gate1.flow_out == 0.0
        assert ffc.gate1.press_out == 0.0

        fff.gate2_open()
        assert ffc.gate2.position == 100
        assert ffc.gate2.flow_out == 19542.86939891452
        assert ffc.gate2.press_out == 13.109851301499999

        fff.gate4_open()
        assert ffc.gate4.position == 100
        assert ffc.gate4.flow_in == 19542.86939891452
        assert ffc.gate4.press_in == 13.109851301499999
        assert ffc.gate4.flow_out == 19542.86939891452
        assert ffc.gate4.press_out == 13.109851301499999

        fff.gate3_open()
        assert ffc.gate3.position == 100
        assert ffc.gate3.flow_in == 19542.86939891452
        assert ffc.gate3.press_in == 13.109851301499999
        assert ffc.gate3.flow_out == 19542.86939891452
        assert ffc.gate3.press_out == 13.109851301499999
        assert ffc.gate6.flow_in == 39085.73879782904
        assert ffc.gate6.press_in == 13.109851301499999

        fff.gate5_open()
        assert ffc.gate5.position == 100
        assert ffc.gate5.flow_in == 19542.86939891452
        assert ffc.gate5.press_in == 13.109851301499999
        assert ffc.gate5.flow_out == 19542.86939891452
        assert ffc.gate5.press_out == 13.109851301499999
        assert ffc.pump1.head_in == 30.24018195875

        fff.gate2_close()
        assert ffc.gate2.position == 0
        assert ffc.gate2.flow_out == 0.0
        assert ffc.gate2.press_out == 0.0

        fff.gate4_open()
        fff.gate3_open()  # Resets output values
        assert ffc.gate3.position == 100
        assert ffc.gate3.flow_in == 0.0
        assert ffc.gate3.press_in == 0.0
        assert ffc.gate3.flow_out == 0.0
        assert ffc.gate3.press_out == 0.0

        assert ffc.gate4.position == 100
        assert ffc.gate4.flow_in == 0.0
        assert ffc.gate4.press_in == 0.0
        assert ffc.gate4.flow_out == 0.0
        assert ffc.gate4.press_out == 0.0

        assert ffc.gate6.flow_in == 0.0
        assert ffc.gate6.press_in == 0.0
