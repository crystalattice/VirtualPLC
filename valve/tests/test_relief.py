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

    def test_high_press_open(self):
        r = Relief()
        r.set_open_pressure(25)
        r.high_press_open(25)
        assert r.read_position() == "The valve is open."

    def test_low_press_close(self):
        r = Relief()
        r.set_blowdown(10)
        r.low_press_close(10)
        assert r.read_position() == "The valve is closed."
