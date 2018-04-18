#!/bin/python

"""
VirtualPLC-valve.py

Purpose: Creates a generic Valve class for PLC-controlled SCADA systems. Two subclasses provide on/off valves and
throttle valves for system use.

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

    Default parameters: initial valve position

    Base methods: Read valve position and changing the position.
    """
    def __init__(self, sys_flow_in=100.0, position=0, flow_coeff=30.0, drop=15.0):
        """Initialize valve"""
        self.position = position
        self.Cv = flow_coeff # Assume 2 inch, valve wide open
        self.deltaP = drop  # Default assumes valve wide open
        self.flow_in = sys_flow_in  # Flow rate to valve in gpm (doesn't guarantee flow past valve)
        self.flow_out = 0.0

    def calc_coeff(self, diameter):
        """Roughly calculate Cv based on valve diameter.

        :param float Valve diameter
        :return float Valve flow coefficient
        """
        coeff = 15 * math.pow(diameter, 2)
        return coeff

    def press_drop(self, flow, spec_grav=1.0):
        """Calculate the pressure drop across a valve, given a flow rate.

        Pressure drop = ((system flow rate / valve coefficient) ** 2) * spec. gravity of fluid

        Cv of valve and flow rate of system must be known.

        Specific gravity of water is 1.

        :param float Fluid specific gravity
        :return float Pressure drop (psi)
        """
        x = (flow / self.Cv)
        self.deltaP = math.pow(x, 2) * spec_grav

    def sys_flow_rate(self, flow_coeff, press_drop, spec_grav=1.0):
        """Calculate the system flow rate through a valve, given a pressure drop.

        Flow rate = valve coefficient / sqrt(spec. grav. / press. drop)

        :param float Pressure drop (psi)
        :param float Fluid specific gravity
        :return float System flow rate
        """
        x = spec_grav / press_drop
        self.flow_out = flow_coeff / math.sqrt(x)


    def cls_get_position(self):
        """Get position of valve, in percent open.

        :return int value of position
        """
        return self.position

    def cls_change_position(self, new_position):
        """Change the valve's position.

        If new position is not an integer, an error is raised.

        :param new_position Value indicating valve's position.
        :except TypeError Exception if non-integer value used
        """
        try:
            if type(new_position) != int:
                raise TypeError
        except TypeError:
            return "Integer values only."
        else:
            self.position = new_position

    def open(self):
        """Open the valve

        :return str Indicates valve is open
        """
        self.cls_change_position(100)
        return "The valve is open."

    def close(self):
        """Close the valve

        :return str Indicates valve is closed
        """
        self.cls_change_position(0)
        return "The valve is closed."


class Gate(Valve):
    """Simple open/closed valve"""
    def read_position(self):
        """Identify the status of the valve.

        :return string The open/closed status of the valve.
        """
        if self.cls_get_position() == 0:
            return "The valve is closed."
        elif self.cls_get_position() == 100:
            return "The valve is open."
        else:   # bad condition
            return "Warning! The valve is partially open."

    def turn_handle(self, new_position):
        """Change the status of the valve.
        
        :param int New valve position
        """
        if new_position == 0:
            print(self.close())
        elif new_position == 100:
            print(self.open())
        else:
            return "Warning: Invalid valve position."


class Globe(Valve):
    """Throttling valve"""
    def read_position(self):
        """Identify the status of the valve.

        :return string The percent open of the valve.
        """
        return "The valve is {position}% open.".format(position=self.cls_get_position())

    def turn_handle(self, new_position):
        """Change the status of the valve.
        
        :param int New valve position
        """
        self.cls_change_position(new_position)
        if self.cls_get_position() == 0:
            self.flow_out = 0.0
            self.deltaP = 0.0
        else:
            self.flow_out = self.flow_in + (self.flow_in * self.position / 100)
            self.press_drop(self.flow_out)

        # print("Valve changed position to {position}% open".format(position=self.position))
        # print("The flow rate after the valve is {flow} gpm.".format(flow=self.flow_out))
        # print("The pressure drop across the valve is {press} psi.".format(press=self.deltaP))

    def open(self):
        """Open the valve

        :return str Indicates valve is open
        """
        self.turn_handle(100)

    def close(self):
        """Close the valve

        :return str Indicates valve is closed
        """
        self.turn_handle(0)


class Relief(Valve):
    """Pressure relieving valve"""
    def read_position(self):
        """Identify the status of the valve.

        :return string The open/closed status of the valve.
        """
        if self.cls_get_position() == 0:
            return "The valve is closed."
        elif self.cls_get_position() == 100:
            return "The valve is open."
        else:   # bad condition
            return "Warning! The valve is partially open."

    def set_open_pressure(self, open_set):
        """Set the pressure setpoint where the valve opens.

        :param int Opening set point
        """
        self.setpoint_open = open_set

    def set_blowdown(self, close_set):
        """Set the pressure setpoint where the valve closes.

        :param int Closing set point
        """
        self.setpoint_close = close_set

    def high_press_open(self, press_in):
        """Open the valve if pressure is too high.

        :param float Valve input pressure
        """
        if press_in > self.setpoint_open:
            self.open()

    def low_press_close(self, press_in):
        """Close the valve when pressure lowers.

        :param float Valve input press
        """
        if press_in <= self.setpoint_close:
            self.close()
