import math

from django.db import models


class Valve(models.Model):
    name = models.TextField()
    _position = models.IntegerField(db_column="position")
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

    @position.setter
    def position(self, new_position):
        try:
            if type(new_position) != int:
                raise TypeError("Integer values only.")
            else:
                self.__position = new_position
                self.save()
        except TypeError:
            raise  # Re-raise for testing

    def open(self):
        self.__position = 100
        self.flow_out = self.flow_in
        self.press_out = self.press_in
        self.save()

    def close(self):
        self.__position = 0
        self.flow_out = 0
        self.press_out = 0
        self.deltaP = 0
        self.save()


class Gate(Valve):
    def read_position(self):
        if self.position == 0:
            return "{name} is closed.".format(name=self.name)
        elif self.position == 100:
            return "{name} is open.".format(name=self.name)
        else:  # bad condition
            return "Warning! {name} is partially open.".format(name=self.name)

    def turn_handle(self, new_position):
        if new_position == 0:
            self.close()
        elif new_position == 100:
            self.open()
        else:  # Shouldn't get here
            return "Warning: Invalid valve position."


class Globe(Valve):
    def read_position(self):
        return "{name} is {position}% open.".format(name=self.name, position=self.position)

    def turn_handle(self, new_position):
        if new_position == 100:
            self.open()
        elif new_position == 0:
            self.close()
        else:
            self.position = new_position
            self.flow_out = self.flow_in * self.position / 100
            self.press_drop(self.flow_out)
            self.get_press_out(self.press_in)
            self.save()


class Relief(Valve):
    def __init__(self, name="", sys_flow_in=0.0, sys_flow_out=0.0, drop=0.0, position=0, flow_coeff=0.0,
                 press_in=0.0, open_press=0, close_press=0):
        super(Relief, self).__init__(name, sys_flow_in, sys_flow_out, drop, position, flow_coeff, press_in)
        self.setpoint_open = open_press
        self.setpoint_close = close_press

    def read_position(self):
        if self.position == 0:
            return "{name} is closed.".format(name=self.name)
        elif self.position == 100:
            return "{name} is open.".format(name=self.name)
        else:  # bad condition
            return "Warning! {name} is partially open.".format(name=self.name)

    def set_open_pressure(self, open_set):
        self.setpoint_open = open_set
        self.save()

    def read_open_pressure(self):
        return self.setpoint_open

    def read_close_pressure(self):
        return self.setpoint_close

    def set_close_press(self, close_set):
        self.setpoint_close = close_set
        self.save()

    def valve_operation(self, press_in):
        if press_in >= self.setpoint_open:
            self.open()
        elif press_in <= self.setpoint_close:
            self.close()
