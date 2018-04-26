#!/bin/python

"""
VirtualPLC-pump.py

Purpose: Creates a generic Pump class for PLC-controlled SCADA systems.

Classes:
    Pump: Generic superclass
    CentrifPump: Pump subclass; provides for a variable displacement pump
    PositiveDisplacement: Pump subclass; provides for a positive displacement pump

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

    Displacement is the amount of fluid pushed through the pump per second.
    Horsepower coefficient is the slope of the equivalent pump curve.

    Variables:
        name
        flow_rate
        head
        outlet_pressure
        speed
        hp
        displacement
        hp_coeff
        wattage

    Methods:
        set_speed()
        cls_read_speed()
        cls_read_press()
        cls_read_flow()
        cls_read_power()
        hp_to_watts()
    """
    def __init__(self, name="", flow_rate=0.0, pump_head_in=0.0, press_out=0.0, pump_speed=0, displacement=0.0):
        """Set initial parameters.

        :param name: Instance name
        :param flow_rate: Flow rate from the pump (gpm)
        :param pump_head_in: Necessary pump head into the pump (feet)
        :param press_out: Pressure created by the pump (psi)
        :param pump_speed: Rotational speed of the pump (rpm)
        :param displacement: Amount of fluid pumped per second
        """
        self.name = name
        self.flow_rate = float(flow_rate)
        self.head = float(pump_head_in)
        self.outlet_pressure = float(press_out)
        self.speed = pump_speed
        self.displacement = float(displacement)
        self.wattage = self.pump_power(self.flow_rate, self.diff_press(self.head, self.outlet_pressure))
# TODO: Move pump-specific parameters to their appropriate classes

    @staticmethod
    def set_speed(new_speed):
        """Change the pump speed.

        :param new_speed: Requested speed for the pump
        :except TypeError
        :except ValueError
        :return: Pump speed
        """
        try:
            if type(new_speed) != int:
                raise TypeError("Integer values only.")
            elif new_speed < 0:
                raise ValueError("Speed must be 0 or greater.")
        except TypeError:
            raise  # Re-raise error for testing
        except ValueError:
            raise  # Re-raise error for testing
        else:
            return new_speed

    def cls_read_speed(self):
        """Get the current speed of the pump."""
        return self.speed

    def cls_read_press(self):
        """Get the current outlet pressure of the pump."""
        return self.outlet_pressure

    def cls_read_flow(self):
        """Get the current outlet flow rate of the pump."""
        return self.flow_rate

    def cls_read_power(self):
        """Get the current power draw of the pump."""
        return self.wattage

    def pump_power(self, flow_rate, diff_head, fluid_spec_weight=62.4, efficiency=0.6):
        """Calculate pump power in kW.

        :param flow_rate: System flow rate
        :param diff_head: Change in pressure across pump
        :param fluid_spec_weight: Specific weight of fluid; default assumes water
        :param efficiency: Pump efficiency
        :return: Pump power requirement, in kW
        """
        gravity = 32.174  # ft/s^2
        hyd_power = (flow_rate * fluid_spec_weight * gravity * diff_head) / 3.6e6
        self.wattage = hyd_power / efficiency
        return self.wattage

    @staticmethod
    def press_to_ft(press):
        """Convert psi to feet of differential head."""
        ft = press * 47.6
        return ft

    def diff_press(self, in_press, out_press):
        """Calculate differential head across pump, in feet."""
        in_press_ft = self.press_to_ft(in_press)
        out_press_ft = self.press_to_ft(out_press)
        delta_p = out_press_ft - in_press_ft
        return delta_p


class CentrifPump(Pump):
    """Defines a variable-displacement, centrifugal-style pump.

    Subclasses Pump.

    Methods:
        get_speed()
        get_flowrate()
        get_pressure()
        get_power()
        adjust_speed()
        pump_laws()
    """

    def get_speed(self):
        """Get the current speed of the pump, in rpm."""
        if self.cls_read_speed() == 0:
                return "The pump is stopped."
        else:
            return "The pump is running at {speed} rpm.".format(speed=self.cls_read_speed())

    def get_flowrate(self):
        """Get the current flow rate of the pump."""
        return "The pump output flow rate is {flow} gpm.".format(flow=self.cls_read_flow())

    def get_pressure(self):
        """Get the current output pressure for the pump."""
        return "The pump pressure is {press:.2f} psi.".format(press=self.cls_read_press())

    def get_power(self):
        """Get the current power draw for the pump."""
        return "The power usage for the pump is {pow:.2f} kW.".format(pow=self.cls_read_power())

    def adjust_speed(self, new_speed):
        """Modify the speed of the pump.

        Affects the outlet flow rate, outlet pressure, and power requirements for the pump.

        :param new_speed: New pump speed
        :return: Updates flow rate, output pressure, and pump power requirement
        """
        self.speed, self.flow_rate, self.outlet_pressure, self.wattage = self.pump_laws(new_speed)

    def pump_laws(self, new_speed):
        """Defines pump characteristics that are based on pump speed.

        Only applies to variable displacement (centrifugal) pumps. Variable names match pump law equations.

        :param new_speed: Requested (new) speed of the pump
        :return: Pump speed, flow rate, outlet pressure, and power
        """
        n2 = self.set_speed(new_speed)  # Validate input

        if self.speed == 0:  # Pump initially stopped
            n1 = 1
        else:
            n1 = self.speed
        v1 = self.flow_rate
        hp1 = self.outlet_pressure

        self.flow_rate = v1 * (n2 / n1)  # New flow rate
        self.outlet_pressure = hp1 * math.pow((n2 / n1), 2)  # New outlet pressure
        self.speed = n2  # Replace old speed with new value
        delta_p = self.diff_press(self.head, self.outlet_pressure)
        self.wattage = abs(self.pump_power(self.flow_rate, delta_p))  # Account for negative differential

        return self.speed, self.flow_rate, self.outlet_pressure, self.wattage


class PositiveDisplacement(Pump):
    """Defines a positive-displacement pump.

    Subclasses Pump.

    Methods:
        get_speed()
        get_flowrate()
        get_pressure()
        get_power()
        set_hp_coeff()
        adjust_speed()
    """

    def get_speed(self):
        """Get the current speed of the pump, in rpm."""
        if self.cls_read_speed() == 0:
                return "The pump is stopped."
        else:
            return "The pump is running at {speed} rpm.".format(speed=self.cls_read_speed())

    def get_flowrate(self):
        """Get the current flow rate of the pump."""
        return "The pump outlet flow rate is {flow} gpm.".format(flow=self.cls_read_flow())

    def get_pressure(self):
        """Get the current output pressure for the pump."""
        return "The pump pressure is {press:.2f} psi.".format(press=self.cls_read_press())

    def get_power(self):
        """Get the current power draw for the pump."""
        return "The power usage for the pump is {pow:.2f} kW.".format(pow=self.cls_read_power())

    def adjust_speed(self, new_speed):
        """Modify the speed of the pump, assuming constant outlet pressure.

        Affects the outlet flow rate and power requirements for the pump.

        :param new_speed: New pump speed
        :return: Flow rate, pump power, and new speed
        """
        self.speed = self.set_speed(new_speed)

        self.flow_rate = self.speed * self.displacement
        self.wattage = self.pump_power(self.flow_rate, self.diff_press(self.head, self.outlet_pressure))

        return self.flow_rate, self.wattage, self.speed


if __name__ == "__main__":
    # Functional tests
    # name="", flow_rate=0.0, pump_head_in=0.0, press_out=0.0, pump_speed=0, hp=0.0, displacement=0.0
    pump1 = CentrifPump("Pumpy", 75, 12, 25, 125, 0.03)
    print("{} created.".format(pump1.name))
    print(pump1.get_speed())
    print(pump1.get_flowrate())
    print(pump1.get_power())
    print(pump1.get_pressure())
    pump1.adjust_speed(50)
    print(pump1.get_speed())
    print(pump1.get_flowrate())
    print(pump1.get_power())
    print(pump1.get_pressure())
    pump1.adjust_speed(0)
    print(pump1.get_speed())
    print(pump1.get_flowrate())
    print(pump1.get_power())
    print(pump1.get_pressure())

    pump2 = PositiveDisplacement("Grumpy", 100, 0, 200, 300, 0.15)
    print("\n{} created.".format(pump2.name))
    print(pump2.get_speed())
    print(pump2.get_flowrate())
    print(pump2.get_power())
    pump2.adjust_speed(50)
    print(pump2.get_speed())
    print(pump2.get_flowrate())
    print(pump2.get_power())
    pump2.adjust_speed(0)
    print(pump2.get_speed())
    print(pump2.get_flowrate())
    print(pump2.get_power())

    p = Pump(name="", flow_rate=100, pump_head_in=12, press_out=45, pump_speed=300, displacement=0)
