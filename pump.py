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
    def __init__(self, flow_rate, pump_head_in, press_out, pump_speed, power):
        """Set initial parameters.

        :param int Flow rate (gpm)
        :param int Input pump head (feet)
        :param int Output pressure (psi)
        :param int Pump speed (rpm)
        :param float Power (kw)
        """
        self.flow_rate = flow_rate
        self.head = pump_head_in
        self.outlet_pressure = press_out
        self.speed = pump_speed
        self.power = power

    def cls_speed_control(cls, new_speed):
        """Change the pump speed."""
        try:
            cls.speed = new_speed
            if type(cls.speed) != int:
                raise TypeError
        except TypeError:
            return "Integer values only."
        else:
            return "Pump speed changed to {speed}%".format(speed=cls.speed)

    def cls_pump_laws(cls, old_speed, new_speed, old_flow_rate, old_press_out, old_pump_power):
        """Defines pump characteristics that are based on pump speed.

        Only applies to variable displacement (centrifugal) pumps. Variable names match pump law equations.

        :param int Pump speed
        :return tuple Volumetric flow rate, pump head, and pressure
        """
        cls.n1 = old_speed
        cls.n2 = new_speed
        cls.V1 = old_flow_rate
        cls.Hp1 = old_press_out
        cls.P1 = old_pump_power

        cls.V2 = cls.V1 * (cls.n2 / cls.n1)  # New flow rate
        cls.Hp2 = cls.Hp1 * math.pow((cls.n2 / cls.n1), 2)  # New outlet pressure
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

    def cls_read_power(self):
        """Get the current power draw of the pump.

        :return float Power requirement
        """
        return self.power


class Centrif_Pump(Pump):
    """Defines a variable-displacement, centrifugal-style pump."""
    def __init__(self):
        """Set default pump parameters."""
        super().__init__(flow_rate=1000, pump_head_in=25, press_out=45, pump_speed=5000, power=1.5)

    def get_speed(self):
        """Get the current speed of the pump

        :return int Current rotational speed, in rpm
        """
        return "The pump is running at {speed} rpm.".format(speed=self.cls_read_speed())

    def get_flowrate(self):
        """Get the current flow rate of the pump

        :return int Current flow rate, in gpm
        """
        return "The pump is pushing {flow} gpm.".format(flow=self.cls_read_flow())

    def get_pressure(self):
        """Get the current output pressure for the pump.

        :return int Current outlet pressure, in psi
        """
        return "The pump pressure is {press} psi.".format(press=self.cls_read_press())

    def get_power(self):
        """Get the current power draw for the pump.

        :return float Current power requirement, in kW
        """
        return "The power usage for the pump is {pow} kW.".format(pow=self.cls_read_power())

    
