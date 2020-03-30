#!/usr/bin/env python3
"""
VirtualPLC pump.py

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
import numbers
import utility_formulas

GRAVITY = 9.81  # m/s^2


class Pump:
    """Generic class for pumps.

    Displacement is the amount of fluid pushed through the pump per second.
    Horsepower coefficient is the slope of the equivalent pump curve.

    Variables: name, flow_rate_out, pump_head_in, press_out, pump_speed

    Methods: set_speed(), cls_read_speed(), cls_read_press(), cls_read_flow(), cls_read_power(), hp_to_watts()
    """

    def __init__(self, name: str = "", flow_rate_out: float = 0.0, pump_head_in: float = 0.0, press_out: float = 0.0,
                 pump_speed: int = 0) -> None:
        """Set initial parameters.

        :param name: Instance name
        :param flow_rate_out: Flow rate from the pump (gpm)
        :param pump_head_in: Necessary pump head into the pump (feet)
        :param press_out: Pressure created by the pump (psi)
        :param pump_speed: Rotational speed of the pump (rpm)
        """
        self.name: str = name
        self.__flow_rate_out: float = flow_rate_out
        self.head_in: float = pump_head_in
        self.__outlet_pressure: float = press_out
        self.__speed: int = pump_speed
        self.__wattage: float = self.pump_power(self.__flow_rate_out,
                                                self.diff_press_psi(self.head_in, self.outlet_pressure))

    @property
    def speed(self):
        """Get the current speed of the pump."""
        return self.__speed

    @speed.setter
    def speed(self, new_speed):
        """Change the pump speed.

        :param new_speed: Requested speed for the pump

        :except TypeError: Non-integer value provided
        :except ValueError: Speed < 0

        :return: Pump speed
        :rtype: int
        """
        try:
            if not isinstance(new_speed, numbers.Number):
                raise TypeError("Numeric values only.")
            elif new_speed < 0:
                raise ValueError("Speed must be 0 or greater.")
            else:
                self.__speed = new_speed
        except TypeError:
            raise  # Re-raise error for testing
        except ValueError:
            raise  # Re-raise error for testing

    @property
    def outlet_pressure(self):
        """Get the current outlet pressure of the pump."""
        return self.__outlet_pressure

    @outlet_pressure.setter
    def outlet_pressure(self, press):
        """Set the pump outlet pressure."""
        self.__outlet_pressure = press

    @property
    def flow(self):
        """Get the current outlet flow rate of the pump."""
        return self.__flow_rate_out

    @flow.setter
    def flow(self, flow_rate):
        """Set the pump outlet flow."""
        self.__flow_rate_out = flow_rate

    @property
    def power(self):
        """Get the current power draw of the pump."""
        return self.__wattage

    @power.setter
    def power(self, power):
        """Set the pump power."""
        self.__wattage = power

    def pump_power(self, flow_rate: float, diff_head: float, fluid_spec_weight: float = 62.4) -> float:
        """Calculate pump power in kW.

        Formula from https://www.engineeringtoolbox.com/pumps-power-d_505.html.
        Because imperial values are converted to metric, the calculation isn't exactly the formula listed on the site;
        view the site's source code to see the formula used.

        :param flow_rate: System flow rate, in gpm
        :param diff_head: Change in pressure across pump, in feet
        :param fluid_spec_weight: Specific weight of fluid; default assumes water

        :return: Pump power requirement, in kW
        :rtype: float
        """
        flow_rate = flow_rate / 15852
        density: float = fluid_spec_weight / 0.0624
        head: float = diff_head / 3.2808
        hyd_power: float = (100 * (flow_rate * density * GRAVITY * head) / 1000) / 100
        self.power = hyd_power
        return self.power

    @staticmethod
    def diff_press_ft(in_press_ft: int, out_press_ft: int) -> float:
        """Calculate differential head across pump, converted from feet."""
        in_press = utility_formulas.head_to_press(in_press_ft)
        out_press = utility_formulas.head_to_press(out_press_ft)
        delta_p = out_press - in_press
        return delta_p

    @staticmethod
    def diff_press_psi(press_in: float, press_out: float) -> float:
        """Calculate differential pump head."""
        delta_p: float = abs(press_out - press_in)  # Account for Pout < Pin
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

    def get_speed_str(self) -> str:
        """Get the current speed of the pump, in rpm."""
        if self.speed == 0:
            return "The pump is stopped."
        else:
            return f"The pump is running at {self.speed} rpm."

    def get_flow_str(self) -> str:
        """Get the current flow rate of the pump."""
        return f"The pump output flow rate is {self.flow} gpm."

    def get_press_str(self) -> str:
        """Get the current output pressure for the pump."""
        return f"The pump pressure is {self.outlet_pressure:.2f} psi."

    def get_power_str(self) -> str:
        """Get the current power draw for the pump."""
        return f"The power usage for the pump is {self.power:.2f} kW."

    def adjust_speed(self, new_speed: int) -> None:
        """Defines pump characteristics that are based on pump speed.

        Only applies to variable displacement (centrifugal) pumps. Variable names match pump law equations.

        :param new_speed: Requested (new) speed of the pump

        :return: Pump speed, flow rate, outlet pressure, and power
        :rtype: tuple
        """
        n2: int = new_speed  # Validate input

        if self.speed == 0:  # Pump initially stopped
            n1: int = 1
        else:
            n1 = self.speed
        v1: float = self.flow
        hp1: float = self.outlet_pressure

        self.flow = v1 * (n2 / n1)  # New flow rate
        self.outlet_pressure = hp1 * math.pow((n2 / n1), 2)  # New outlet pressure
        self.speed = n2  # Replace old speed with new value
        delta_p: float = self.diff_press_psi(self.head_in, utility_formulas.press_to_head(self.outlet_pressure))
        self.power = self.pump_power(self.flow, delta_p)

    def start_pump(self, speed: int, flow: float, out_press: float = 0.0, out_ft: float = 0.0) -> tuple:
        """System characteristics when a pump is initially started.

        Assumes all valves fully open, i.e. maximum flow rate.

        :param speed: Pump speed
        :param flow: Max flow rate, in gpm
        :param out_press: Pump pressure at max flow, in psi
        :param out_ft: Output head pressure, in feet

        :return: Pump speed, flow rate, outlet pressure, and power
        :rtype: tuple
        """
        self.speed = speed
        self.flow = flow
        if out_press > 0.0:
            self.outlet_pressure = out_press
        elif out_ft > 0.0:
            self.outlet_pressure = utility_formulas.head_to_press(out_ft)
        else:
            return "Outlet pump pressure required."
        delta_p = self.outlet_pressure - utility_formulas.head_to_press(self.head_in)
        self.power = self.pump_power(self.flow, delta_p)

        return self.speed, self.flow, self.outlet_pressure, self.power


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

    def __init__(self, name="", flow_rate_out=0.0, pump_head_in=0.0, press_out=0.0, pump_speed=0,
                 displacement: float = 0.0):
        super(PositiveDisplacement, self).__init__(name, flow_rate_out, pump_head_in, press_out, pump_speed)
        self.displacement: float = displacement

    def get_speed_str(self) -> str:
        """Get the current speed of the pump, in rpm."""
        if self.speed == 0:
                return "The pump is stopped."
        else:
            return f"The pump is running at {self.speed} rpm."

    def get_flow_str(self) -> str:
        """Get the current flow rate of the pump."""
        return f"The pump outlet flow rate is {self.flow} gpm."

    def get_press_str(self) -> str:
        """Get the current output pressure for the pump."""
        return f"The pump pressure is {self.outlet_pressure} psi."

    def get_power_str(self) -> str:
        """Get the current power draw for the pump."""
        return f"The power usage for the pump is {self.power:.2f} kW."

    def adjust_speed(self, new_speed: int) -> None:
        """Modify the speed of the pump, assuming constant outlet pressure.

        Affects the outlet flow rate and power requirements for the pump.

        :param new_speed: New pump speed

        :return: Flow rate, pump power, and new speed
        :rtype: tuple
        """
        self.speed = new_speed
        press_in = utility_formulas.head_to_press(self.head_in)

        self.flow = self.speed * self.displacement
        self.power = self.pump_power(self.flow, self.diff_press_psi(press_in, self.outlet_pressure))
# TODO: Account for different flow rates based on outlet pressure


if __name__ == "__main__":
    # Functional test_valves
    # name="", flow_rate=0.0, pump_head_in=0.0, press_out=0.0, pump_speed=0, hp=0.0, displacement=0.0
    pump1 = CentrifPump("Pumpy", 75, 12, 25, 125)
    print("{} created.".format(pump1.name))
    print(pump1.get_speed_str())
    print(pump1.get_flow_str())
    print(pump1.get_power_str())
    print(pump1.get_press_str())
    pump1.adjust_speed(50)
    print(pump1.get_speed_str())
    print(pump1.get_flow_str())
    print(pump1.get_power_str())
    print(pump1.get_press_str())
    pump1.adjust_speed(0)
    print(pump1.get_speed_str())
    print(pump1.get_flow_str())
    print(pump1.get_power_str())
    print(pump1.get_press_str())

    pump2 = PositiveDisplacement("Grumpy", 100, 0, 200, 300, 0.15)
    print("\n{} created.".format(pump2.name))
    print(pump2.get_speed_str())
    print(pump2.get_flow_str())
    print(pump2.get_power_str())
    pump2.adjust_speed(50)
    print(pump2.get_speed_str())
    print(pump2.get_flow_str())
    print(pump2.get_power_str())
    pump2.adjust_speed(0)
    print(pump2.get_speed_str())
    print(pump2.get_flow_str())
    print(pump2.get_power_str())

    p = Pump(name="", flow_rate_out=100, pump_head_in=12, press_out=45, pump_speed=300)
