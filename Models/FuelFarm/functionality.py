#!/usr/bin/env python3
"""
FuelFarm_functionality.py

Purpose: Ensure valve/pump changes are passed to the rest of the system.

Author: Cody Jackson

Date: 6/18/18
#################################
Version 0.1
    Initial build
"""
import utility_formulas
import Models.FuelFarm.components as ffc


# Gate valve 1
def gate1_open():
    ffc.gate1.open()
    ffc.gate3.press_in = ffc.gate1.press_out
    ffc.gate3.flow_in = ffc.gate1.flow_out
    ffc.gate5.press_in = ffc.gate1.press_out
    ffc.gate5.flow_in = ffc.gate1.flow_out


def gate1_close():
    ffc.gate1.close()
    ffc.gate3.press_in = 0.0
    ffc.gate3.flow_in = 0.0
    ffc.gate5.press_in = 0.0
    ffc.gate5.flow_in = 0.0


# Gate valve 2
def gate2_open():
    ffc.gate2.open()
    ffc.gate4.press_in = ffc.gate2.press_out
    ffc.gate4.flow_in = ffc.gate2.flow_out
    ffc.gate7.press_in = ffc.gate2.press_out
    ffc.gate7.flow_in = ffc.gate2.flow_out


def gate2_close():
    ffc.gate2.close()
    ffc.gate4.press_in = 0.0
    ffc.gate4.flow_in = 0.0
    ffc.gate7.press_in = 0.0
    ffc.gate7.flow_in = 0.0


# Gate valve 3
def gate3_open():
    ffc.gate3.open()
    ffc.gate6.press_in = ffc.gate3.press_out
    ffc.gate6.flow_in = ffc.gate3.flow_out
    ffc.gate4.press_in = ffc.gate3.press_out
    ffc.gate4.flow_in = ffc.gate3.flow_out


def gate3_close():
    ffc.gate3.close()
    ffc.gate6.press_in = 0.0
    ffc.gate6.flow_in = 0.0
    ffc.gate4.press_in = 0.0
    ffc.gate4.flow_in = 0.0


# Gate valve 4
def gate4_open():
    ffc.gate4.open()
    ffc.gate6.press_in = ffc.gate4.press_out
    ffc.gate6.flow_in = ffc.gate4.flow_out
    ffc.gate3.press_in = ffc.gate4.press_out
    ffc.gate3.flow_in = ffc.gate4.flow_out


def gate4_close():
    ffc.gate4.close()
    ffc.gate6.press_in = 0.0
    ffc.gate6.flow_in = 0.0
    ffc.gate3.press_in = 0.0
    ffc.gate3.flow_in = 0.0
