#!/bin/python

"""
VirtualPLC-pump.py

Purpose: Creates a generic Pump class for PLC-controlled SCADA systems. Subclassed into variable and positive
displacement pumps.

Author: Cody Jackson

Date: 4/12/18
#################################
Version 0.1
    Initial build
"""
# from pymodbus.client.sync import ModbusTcpClient

class Pump:
    """Generic class for pumps.

    Default parameters: Volumetric flow rate, required head pressure, outlet pressure, pump speed

    Provides base methods to change pump speed control, read the pump speed, read the outlet pressure and flow rate.
    """
    def __init__(self, flow_rate, pump_head, press_out, pump_speed):
        """Set initial parameters."""
        self.flow_rate = flow_rate
        self.head = pump_head
        self.outlet_pressure = press_out
        self.speed = pump_speed

    def speed_control(self, new_speed):
        """Change the pump speed."""
        try:
            self.speed = new_speed
            if type(self.position) != int:
                raise TypeError
        except TypeError:
            return "Integer values only."
        else:
            return "Valve changed position to {position}% open".format(position=self.position)