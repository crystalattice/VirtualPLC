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
import math

# from pymodbus.client.sync import ModbusTcpClient


class Pump:
    """Generic class for pumps.

    Default parameters: Volumetric flow rate, required head pressure, outlet pressure, pump speed

    Provides base methods to change pump speed control, calculate changes to pump parameters based on speed changes,
    read the pump speed, outlet pressure, and flow rate.
    """
    def __init__(self, flow_rate, pump_head, press_out, pump_speed, power):
        """Set initial parameters."""
        self.flow_rate = flow_rate  #gallons per minute
        self.head = pump_head
        self.outlet_pressure = press_out
        self.speed = pump_speed  # rpm
        self.power = power

    def speed_control(cls, new_speed):
        """Change the pump speed."""
        try:
            cls.speed = new_speed
            if type(cls.speed) != int:
                raise TypeError
        except TypeError:
            return "Integer values only."
        else:
            return "Pump speed changed to {speed}%".format(speed=cls.speed)

    def pump_laws(cls, old_speed, new_speed, old_flow_rate, old_pump_head, old_pump_power):
        """Defines pump characteristics that are based on pump speed.

        Only applies to variable displacement (centrifugal) pumps. Variable names match pump law equations.

        :param int Pump speed
        :return tuple Volumetric flow rate, pump head, and pressure
        """
        cls.n1 = old_speed
        cls.n2 = new_speed
        cls.V1 = old_flow_rate
        cls.Hp1 = old_pump_head
        cls.P1 = old_pump_power

        cls.V2 = cls.V1 * (cls.n2 / cls.n1)  # New flow rate
        cls.Hp2 = cls.Hp1 * math.pow((cls.n2 / cls.n1), 2)  # New pump head
        cls.P2 = cls.P1 * math.pow((cls.n2 / cls.n1), 3)  # New pump power

        return cls.V2, cls.Hp2, cls.P2

    def cls_read_speed(self):
        """Get the current speed of the pump.

        :return int Pump speed
        """
        return self.speed

    def cls_read_press(self):
        """Get the current outlet pressure of the pump.

        :return int Outlet pressure
        """
        return self.outlet_pressure

    def cls_read_flow(self):
        """Get the current outlet flow rate of the pump.

        :return int Outlet flow rate
        """
        return self.flow_rate


class Centrif_Pump(Pump):
    """Defines a variable-displacement, centrifugal-style pump."""
    def __init__(self):
        """Set default pump parameters."""
        super.__init__()