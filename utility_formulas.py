# !/usr/bin/env python3
"""
General formulas used when calculating flow rates and pressure. Assumes fluid is liquid and not gas.
"""

import math
from typing import Any

GRAVITY: float = 32.174  # ft/s^2
WATER_SPEC_WEIGHT: float = 62.4  # lb/ft^3
WATER_DENSITY: float = 1.94  # slugs/ft^3
WATER_SPEC_GRAV: float = 1.0


def gravity_flow_rate(diameter: float, slope: float, rough_coeff: float = 140) -> float:
    """Calculates approximate fluid flow due to gravity.

    Should be within 5% of actual value.

    Based on the Hazen-Williams equation (https://en.wikipedia.org/wiki/Hazen–Williams_equation). Assumes a 2 inch,
    polyethylene pipe.

    :param diameter: Pipe diameter, in inches
    :param slope: Slope of pipe, from reservoir to measure point
    :param rough_coeff: Roughness coefficient of pipe

    :return: Approximate fluid flow rate, in gpm
    """
    coeff: float = math.pow(rough_coeff, 1.852)
    diam: float = math.pow(diameter, 4.8704)
    root_flow: float = math.sqrt(((coeff * diam * slope) / 4.52))
    return root_flow


def static_press(height: float, density: float = WATER_DENSITY) -> float:
    """Calculate static pressure for any fluid.

    :param height: Fluid height, in feet
    :param density: Fluid density. Default assumes water.

    :return: Fluid pressure, in psi
    """
    press: float = density * GRAVITY * height / 144
    return press


def press_to_head(press: float, spec_grav: float = WATER_SPEC_GRAV) -> float:
    """Calculate fluid head from pressure.

    :param press: Fluid pressure, in psi
    :param spec_grav: Specific gravity of fluid

    :return: Fluid head, in feet
    """
    head: float = (74.215 * press) / (spec_grav * GRAVITY)
    return head


def head_to_press(head: float, spec_grav: float = WATER_SPEC_GRAV) -> float:
    """Calculate pressure from fluid head.

    :param head: Fluid head, in feet
    :param spec_grav: Specific gravity of fluid

    :return: Fluid pressure, in psi
    """
    press: float = (spec_grav * GRAVITY * head) / 74.215
    return press


if __name__ == "__main__":
    print(f"Gravity flow rate (gpm) @ 2in and 0.6 slope = {gravity_flow_rate(2, 0.6)}")
    print(f"Static pressure (psi) @ 150ft = {static_press(150)}")
    print(f"Head pressure (feet) @ 65psi = {press_to_head(65.0)}")
    print(f"Pressure (psi) @ 150ft = {head_to_press(150)}")
