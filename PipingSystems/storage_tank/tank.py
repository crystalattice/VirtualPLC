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


class Tank:
    """Generic storage tank."""
    def __init__(self, name="", level=0.0, fluid_density=1.94, spec_gravity=1.0):
        self.name = name
        self.__level = level  # feet
        self.fluid_density = fluid_density
        self.spec_grav = spec_gravity
        self.tank_press = 0.0

    def static_tank_press(self):
        """Calculate the static fluid pressure based on tank level."""
        self.tank_press = utility_formulas.head_to_press(self.level, self.spec_grav)
        return self.tank_press

    @property
    def level(self):
        """Return fluid level in tank."""
        return self.__level

    @level.setter
    def level(self, level):
        """Set the level in the tank."""
        self.__level = level


if __name__ == "__main__":
    tank1 = Tank("tank1", 10)
    print(tank1.level)
    tank1.level = 8.0
    print(tank1.level)
