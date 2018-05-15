#!/usr/bin/env python3
"""
VirtualPLC user_creation_script.py

Purpose: Allow for automated creation of a piping model from user input. Assumes a drawing of the model has already
been made to allow correct mapping of inputs and outputs.

Classes:

Author: Cody Jackson

Date: 5/15/18
###############################
Version 0.1
    Initial build
"""
import utility_formulas
from valve.valve import *
from pump.pump import *


def request_component():
    """Ask user to provide new piping component."""
    new_item = int(input("Enter the number of the component that should be added: Valve = 1, Pump = 2"))
    if new_item == 1:
        valve()
    elif new_item == 2:
        pump()
    else:
        print("Invalid selection. Please enter '1' or '2'.")


def valve():
    """Determine the type of valve to create."""
    valve_type = int(input("What type of valve should be created? Gate = 1, Globe = 2, Relief = 3"))
    if valve_type == 1:
        gate_valve()
    elif valve_type == 2:
        globe_valve()
    elif valve_type == 3:
        relief_valve()
    else:
        print("Invalid selection. Please enter '1', '2', or '3'.")


def gate_valve():
    """Create a gate valve."""
    gate_name = input("Please provide the name for this valve: ")
    gate_position = input("Is the valve open or closed? ")
    gate_cv = float(input("What is the flow coefficient of the valve? "))
    gate_precede_component = int(input("What is feeding into this valve? Tank = 1, Valve = 2, Pump = 3"))
    if gate_precede_component == 1:
        gate_tank_diam = float(input("What is the diameter of the pipe from the tank, in inches? "))
        gate_tank_static = float(input("What is the fluid height above the valve? "))
        gate_tank_slope = float(input("What is the slope of the pipe from the tank to the valve?"))
    gate_flow_in = input("What is the flow rate into the valve, in gallons per minute? ")
    gate_press_in = input("What is the inlet pressure of the valve? ")