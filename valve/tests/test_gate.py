from ..valve import Gate


class TestGate():
    def test_read_position(self):
        g = Gate()
        assert g.read_position() == "The valve is closed."
        g.open()
        assert g.read_position() == "The valve is open."
        g.cls_change_position(50)
        assert g.read_position() == "Warning! The valve is partially open."

    def test_turn_handle(self):
        g = Gate()
        g.turn_handle(100)
        assert g.read_position() == "The valve is open."
        g.turn_handle(0)
        assert g.read_position() == "The valve is closed."
        assert g.turn_handle(50) == "Warning: Invalid valve position."
