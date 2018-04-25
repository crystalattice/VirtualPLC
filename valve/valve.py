#!/bin/python

"""
VirtualPLC-valve.py

Purpose: Creates a generic Valve class for PLC-controlled SCADA systems.

Classes:
    Valve: Generic superclass
    Gate: Valve subclass; provides for an open/close valve
    Globe: Valve subclass; provides for a throttling valve
    Relief: Valve subclass; provides for a pressure-operated open/close valve

Author: Cody Jackson

Date: 4/9/18
#################################
Version 0.1
    Initial build
"""
# from pymodbus.client.sync import ModbusTcpClient
import math


class Valve:
    """Generic class for valves.

    Cv is the valve flow coefficient: number of gallons per minute at 60F through a fully open valve with a press. drop
    of 1 psi. For valves 1 inch or less in diameter, Cv is typically < 5.

    Variables: name, position, Cv, deltaP, flow_in, flow_out, setpoint_open, setpoint_close

    Methods:
        calc_coeff()
        press_drop()
        sys_flow_rate()
        cls_get_position()
        cls_change_position()
        open()
        close()
    """

    def __init__(self, name="", sys_flow_in=0.0, position=0, flow_coeff=0.0, drop=0.0, open_press=0, close_press=0):
        """Initialize valve."""
        self.name = name
        self.position = int(position)  # Represents percent open
        self.Cv = float(flow_coeff)  # Assume 2 inch, valve wide open
        self.deltaP = float(drop)  # Default assumes valve wide open
        self.flow_in = float(sys_flow_in)  # Flow rate to valve in gpm (doesn't guarantee flow past valve)
        self.flow_out = 0.0
        self.setpoint_open = open_press
        self.setpoint_close = close_press

    def calc_coeff(self, diameter):
        """Roughly calculate Cv based on valve diameter.

        :param diameter: Valve diameter
        :return: Update valve flow coefficient
        """
        self.Cv = 15 * math.pow(diameter, 2)

    def press_drop(self, flow, spec_grav=1.0):
        """Calculate the pressure drop across a valve, given a flow rate.

        Pressure drop = ((system flow rate / valve coefficient) ** 2) * spec. gravity of fluid

        Cv of valve and flow rate of system must be known.

        Specific gravity of water is 1.

        :param flow: System flow rate
        :param spec_grav: Fluid specific gravity
        :except ZeroDivisionError
        :return: Update pressure drop across valve
        """
        try:
            x = (flow / self.Cv)
            self.deltaP = math.pow(x, 2) * spec_grav
        except ZeroDivisionError:
            return "The valve coefficient must be > 0."

    def sys_flow_rate(self, flow_coeff, press_drop, spec_grav=1.0):
        """Calculate the system flow rate through a valve, given a pressure drop.

        Flow rate = valve coefficient / sqrt(spec. grav. / press. drop)

        :param flow_coeff: Valve flow coefficient
        :param press_drop: Pressure drop (psi)
        :param spec_grav: Fluid specific gravity
        :except ValueError
        :return: Update system flow rate
        """
        try:
            if flow_coeff <= 0 or press_drop <= 0:
                raise ValueError("Input values must be > 0.")
            else:
                x = spec_grav / press_drop
                self.flow_out = flow_coeff / math.sqrt(x)
        except ValueError:
            raise  # Re-raise error for testing

    def cls_get_position(self):
        """Get position of valve, in percent open."""
        return self.position

    def cls_change_position(self, new_position):
        """Change the valve's position.

        If new position is not an integer, an error is raised.

        :param new_position: Value indicating valve's position.
        :except TypeError Exception if non-integer value used
        :return Update valve position
        """
        try:
            if type(new_position) != int:
                raise TypeError
        except TypeError:
            return "Integer values only."
        else:
            self.position = new_position

    def open(self):
        """Open the valve"""
        self.cls_change_position(100)

    def close(self):
        """Close the valve"""
        self.cls_change_position(0)


class Gate(Valve):
    """Open/closed valve.

    Subclasses Valve.

    Methods:
        read_position(): Extends cls_get_position()
        turn_handle(): Extends open() & close()
    """

    def read_position(self):
        """Identify the status of the valve.

        :return: The open/closed status of the valve.
        """
        if self.cls_get_position() == 0:
            return "The valve is closed."
        elif self.cls_get_position() == 100:
            return "The valve is open."
        else:  # bad condition
            return "Warning! The valve is partially open."

    def turn_handle(self, new_position):
        """Change the status of the valve.
        
        :param new_position: New valve position
        :return: Update valve position
        """
        if new_position == 0:
            self.close()
        elif new_position == 100:
            self.open()
        else:  # Shouldn't get here
            return "Warning: Invalid valve position."


class Globe(Valve):
    """Throttling valve.

    Subclasses Valve.

    Methods:
        read_position(): Extends cls_get_position()
        turn_handle(): Extends cls_change_position() & cls_get_position()
    """

    def read_position(self):
        """Identify the position of the valve."""
        return "The valve is {position}% open.".format(position=self.cls_get_position())

    def turn_handle(self, new_position):
        """Change the status of the valve.
        
        :param new_position: New valve position
        :return: Update outlet flow rate and valve pressure drop
        """
        self.cls_change_position(new_position)
        if self.cls_get_position() == 0:
            self.flow_out = 0.0
            self.deltaP = 0.0
        else:
            self.flow_out = self.flow_in + (self.flow_in * self.position / 100)
            self.press_drop(self.flow_out)


class Relief(Valve):
    """Pressure relieving valve.

    Subclasses Valve.

    Methods:
        read_position(): Extends cls_get_position()
        set_open_pressure()
        set_blowdown()
        read_open_pressure()
        read_close_pressure()
        valve_operation()
    """

    def read_position(self):
        """Identify the status of the valve.

        :return: The open/closed status of the valve.
        """
        if self.cls_get_position() == 0:
            return "The valve is closed."
        elif self.cls_get_position() == 100:
            return "The valve is open."
        else:   # bad condition
            return "Warning! The valve is partially open."

    def set_open_pressure(self, open_set):
        """Set the pressure setpoint where the valve opens.

        :param: open_set: Opening set point
        :return: Update the opening set point
        """
        self.setpoint_open = open_set

    def read_open_pressure(self):
        """Read the high pressure setpoint."""
        return self.setpoint_open

    def read_close_pressure(self):
        """Read the low pressure setpoint."""
        return self.setpoint_close

    def set_blowdown(self, close_set):
        """Set the pressure setpoint where the valve closes.

        :param close_set: Closing set point
        :return: Update the closing set point
        """
        self.setpoint_close = close_set

    def valve_operation(self, press_in):
        """Open the valve if pressure is too high; close the valve when pressure lowers.

        :param press_in: Valve input pressure
        :return: Update valve position
        """
        if press_in >= self.setpoint_open:
            self.open()
        elif press_in <= self.setpoint_close:
            self.close()


if __name__ == "__main__":
    # Functional tests
    gate1 = Gate("Pump inlet")
    print("{} created".format(gate1.name))
    print(gate1.read_position())
    gate1.turn_handle(100)
    print(gate1.read_position())
    gate1.close()
    print(gate1.read_position())
    gate1.open()
    print(gate1.read_position())

    globe1 = Globe("\nThrottle valve")
    print("{} created".format(globe1.name))
    print(globe1.read_position())
    globe1.open()
    print(globe1.read_position())
    globe1.close()
    print(globe1.read_position())
    globe1.turn_handle(40)
    print(globe1.read_position())

    relief1 = Relief("\nPressure relief", open_press=25, close_press=20)
    print("{} created".format(relief1.name))
    print(relief1.read_position())
    print("The open setpoint is {} psi.".format(relief1.read_open_pressure()))
    print("The close setpoint is {} psi.".format(relief1.read_close_pressure()))
    relief1.set_open_pressure(75)
    relief1.set_blowdown(73)
    print("The open setpoint is {} psi.".format(relief1.read_open_pressure()))
    print("The close setpoint is {} psi.".format(relief1.read_close_pressure()))
    relief1.valve_operation(75)
    print(relief1.read_position())
    relief1.valve_operation(73)
    print(relief1.read_position())

