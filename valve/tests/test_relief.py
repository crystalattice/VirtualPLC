from ..valve import Relief


class TestRelief():
    def test_read_position(self):
        r = Relief()
        assert r.read_position() == "The valve is closed."

    def test_set_open_pressure(self):
        r = Relief()
        r.set_open_pressure(25)
        assert r.setpoint_open == 25

    def test_set_blowdown(self):
        r = Relief()
        r.set_blowdown(10)
        assert r.setpoint_close == 10

    def test_valve_operation(self):
        r = Relief(open_press=25, close_press=23)
        r.valve_operation(25)
        assert r.read_position() == "The valve is open."
        r.valve_operation(23)
        assert r.read_position() == "The valve is closed."
