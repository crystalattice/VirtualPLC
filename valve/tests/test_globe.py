from ..valve import Globe


class TestGlobe():
    def test_read_position(self):
        g = Globe()
        assert g.read_position() == "The valve is 0% open."

    def test_turn_handle(self):
        g = Globe()
        g.turn_handle(40)
        assert g.read_position() == "The valve is 40% open."

    def test_open(self):
        g = Globe()
        g.open()
        assert g.read_position() == "The valve is 100% open."

    def test_close(self):
        g = Globe()
        g.close()
        assert g.read_position() == "The valve is 0% open."
