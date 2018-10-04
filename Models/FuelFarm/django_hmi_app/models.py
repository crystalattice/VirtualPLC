import math

from django.db import models


class Valve(models.Model):
    name = models.TextField()
    _position = models.IntegerField()
    Cv = models.FloatField()
    flow_in = models.FloatField()
    deltaP = models.FloatField()
    flow_out = models.FloatField()
    press_in = models.FloatField()
    press_out = models.FloatField()

    def calc_coeff(self, diameter):
        self.Cv = 15 * math.pow(diameter, 2)
        self.save()

    def press_drop(self, flow_out, spec_grav=1.0):
        try:
            x = (flow_out / self.Cv)
            self.deltaP = math.pow(x, 2) * spec_grav
            self.save()
        except ZeroDivisionError:
            return "The valve coefficient must be > 0."

    def valve_flow_out(self, flow_coeff, press_drop, spec_grav=1.0):
        try:
            if flow_coeff <= 0 or press_drop <= 0:
                raise ValueError("Input values must be > 0.")
            else:
                x = spec_grav / press_drop
                self.flow_out = flow_coeff / math.sqrt(x)
                self.save()
                return self.flow_out
        except ValueError:
            raise  # Re-raise error for testing

    def get_press_out(self, press_in):
        if press_in:
            self.press_in = press_in  # In case the valve initialization didn't include it, or the value has changed
            self.save()
        self.press_drop(self.flow_out)
        self.save()
        self.press_out = self.press_in - self.deltaP
        self.save()

    @property
    def position(self):
        return self._position
    