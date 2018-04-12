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


class Valve:
    """Generic class for valves.

    Default parameters: initial valve position

    Base methods: Read valve position and changing the position.
    """
    def __init__(self, position):
        """Initialize valve"""
        self.position = position

    def cls_get_position(self):
        """Get position of valve, in percent open.

        :return int value of position
        """
        return self.position

    def cls_change_position(self, new_position):
        """Change the valve's position.

        If new position is not an integer, an error is raised.

        :param new_position Value indicating valve's position.
        """
        try:
            if type(new_position) != int:
                raise TypeError
        except TypeError:
            return "Integer values only."
        else:
            self.position = new_position
            return "Valve changed position to {position}% open".format(position=self.position)

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
    def __init__(self):
        """Set new valve to closed"""
        super().__init__(0)

    def read_position(self):
        """Identify the status of the valve.

        :return string The open/closed status of the valve.
        """
        if self.cls_get_position() == 0:
            return "The valve is closed."
        elif self.cls_get_position() == 100:
            return "The valve is open."
        else:   # bad condition
            return "Warning: The valve is partially open."

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
    def __init__(self):
        """Set new valve to closed."""
        super().__init__(0)

    def read_position(self):
        """Identify the status of the valve.

        :return string The percent open of the valve.
        """
        return "The valve is {position}% open.".format(position=self.cls_get_position())

    def turn_handle(self, new_position):
        """Change the status of the valve.
        
        :param int New valve position
        """
        print(self.cls_change_position(new_position))