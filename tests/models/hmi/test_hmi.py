import Models.FuelFarm.components as ffc
import Models.FuelFarm.functionality as fff
import Models.FuelFarm.hmi.hmilayout as hmi


class TestLineup1:
    """Gate 1, Gate 5, Pump 1"""
    @classmethod
    def setup_class(cls):
        fff.gate1_open()
        fff.gate5_open()
        fff.pump1_on()

    def test_gate1(self):
        assert hmi.components.gate1.position == 100
        assert "{:.2f}".format(hmi.components.gate1.press_in) == "13.11"
        assert "{:.2f}".format(hmi.components.gate1.flow_in) == "19542.87"
        assert "{:.2f}".format(hmi.components.gate1.press_out) == "13.11"
        assert "{:.2f}".format(hmi.components.gate1.flow_out) == "19542.87"

    def test_gate5(self):
        assert hmi.components.gate5.position == 100
        assert "{:.2f}".format(hmi.components.gate5.press_in) == "13.11"
        assert "{:.2f}".format(hmi.components.gate5.flow_in) == "19542.87"
        assert "{:.2f}".format(hmi.components.gate5.press_out) == "13.11"
        assert "{:.2f}".format(hmi.components.gate5.flow_out) == "19542.87"

    def test_pump1(self):
        assert hmi.components.pump1.speed == 1480
        assert "{:.2f}".format(hmi.components.pump1.power) == "0.88"
        assert "{:.2f}".format(hmi.components.pump1.outlet_pressure) == "50.00"
        assert "{:.2f}".format(hmi.components.pump1.flow) == "355.20"
