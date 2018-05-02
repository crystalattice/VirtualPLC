#!/bin/python

import math


def gravity_flow_rate(diameter, slope, rough_coeff=140):
    """Calculates fluid flow due to gravity.

    Based on the Hazen-Williams equation (https://en.wikipedia.org/wiki/Hazen–Williams_equation). Assumes a 2 inch,
    polyethylene pipe.
    """
    coeff = math.pow(rough_coeff, 1.852)
    diam = math.pow(diameter, 4.8704)
    flow = ((coeff * diam * slope) / 4.52) ** (1.0 / 1.852)
    return flow


print(gravity_flow_rate(2, 0.6))
