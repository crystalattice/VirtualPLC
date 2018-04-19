from ..pump import Pump


class TestPump():
    def test_speed_control(self):
        p = Pump()
        p.speed_control(750)
        assert p.cls_read_speed() == 750

    def test_pump_laws(self):
        p = Pump()
        p.pump_laws(100, 300, 70, 45, .25)
        assert p.flow_rate == 210.0
        assert p.press_out == 405.0
        assert p.power == 6.7

    def test_cls_read_speed(self):
        p = Pump()
        assert p.cls_read_speed() == 0

    def test_cls_read_press(self):
        p = Pump()
        assert p.cls_read_press() == 0.0

    def test_cls_read_flow(self):
        p = Pump()
        assert p.cls_read_flow() == 0.0

    def test_cls_read_power(self):
        p = Pump()
        assert p.cls_read_power() == 0.0
