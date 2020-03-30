#!/usr/bin/env python3
"""
VirtualPLC tank.py

Purpose: Creates a generic Tank class for PLC-controlled SCADA systems.

Author: Cody Jackson

Date: 5/28/18
#################################
Version 0.1
    Initial build
"""
import utility_formulas
import numbers

from dataclasses import dataclass


@dataclass
class Tank:
    """Generic storage tank. Default numbers assume water is the liquid.

    Coefficient values from https://www.engineeringtoolbox.com/hazen-williams-coefficients-d_798.html
    """
    name: str = ""
    level: float = 0.0
    fluid_density: float = 1.94
    spec_gravity: float = 1.0
    outlet_diam: float = 0.0
    outlet_slope: float = 0.0
    tank_press: float = 0.0
    flow_out: float = 0.0
    pipe_diam: float = outlet_diam
    pipe_slope: float = outlet_slope
    pipe_coeff: int = 140  # Assume steel pipe

    @property
    def static_tank_press(self):
        """Return hydrostatic tank pressure."""
        return self.tank_press

    @static_tank_press.setter
    def static_tank_press(self, level):
        """Calculate the static fluid pressure based on tank level."""
        try:
            if not isinstance(level, numbers.Number):
                raise TypeError("Numeric values only.")
            elif level <= 0:
                self.tank_press = 0.0
            else:
                self.tank_press = utility_formulas.static_press(self.tank_level, self.fluid_density)
        except TypeError:
            raise  # Re-raise for testing

    @property
    def tank_level(self):
        """Return fluid level in tank."""
        return self.level

    @tank_level.setter
    def tank_level(self, level):
        """Set the level in the tank."""
        try:
            if not isinstance(level, numbers.Number):
                raise TypeError("Numeric values only.")
            elif level <= 0:
                self.level = 0.0
            else:
                self.level = level
        except TypeError:
            raise  # Re-raise error for testing
        finally:
            self.static_tank_press = self.tank_level
            self.gravity_flow(self.pipe_diam, self.pipe_slope, self.pipe_coeff)

    def gravity_flow(self, diameter, slope, pipe_coeff):
        if self.tank_level > 0:
            self.flow_out = utility_formulas.gravity_flow_rate(diameter, slope, pipe_coeff)
        else:
            self.flow_out = 0.0


if __name__ == "__main__":
    tank1 = Tank("tank1", 10)
    print(tank1.tank_level)
    tank1.static_tank_press = tank1.tank_level
    print(tank1.static_tank_press)
    tank1.tank_level = 8.0
    print(tank1.tank_level)
    tank1.static_tank_press = tank1.tank_level
    print(tank1.static_tank_press)
    tank1.tank_level = "a"
    print(tank1.tank_level)
