import utility_formulas

from pump.pump import CentrifPump, PositiveDisplacement
from valve.valve import Gate, Globe, Relief

"""Same as test_parameters.py, except it checks values after throttle valves are turned."""

valve1 = Gate("Valve 1", position=100, flow_coeff=200, sys_flow_in=utility_formulas.gravity_flow_rate(2, 1.67),
              press_in=utility_formulas.static_press(14))
valve1.press_drop(valve1.flow_in)
valve1.valve_flow_out(valve1.Cv, valve1.deltaP)
valve1.get_press_out(valve1.press_in)

pump1 = CentrifPump("Pump 1", pump_head_in=utility_formulas.press_to_head(valve1.press_out))
pump1.start_pump(1750, 50, 16)

throttle1 = Globe("Throttle 1", position=100, flow_coeff=21, press_in=pump1.outlet_pressure,
                  sys_flow_in=pump1.flow_rate_out)
throttle1.press_drop(throttle1.flow_in)
throttle1.valve_flow_out(throttle1.Cv, throttle1.deltaP)
throttle1.get_press_out(throttle1.press_in)

valve2 = Gate("Valve 2", position=100, flow_coeff=200, press_in=throttle1.press_out, sys_flow_in=throttle1.flow_out)
valve2.press_drop(valve2.flow_in)
valve2.valve_flow_out(valve2.Cv, valve2.deltaP)
valve2.get_press_out(valve2.press_in)

valve3 = Gate("Valve 3", position=100, flow_coeff=200, press_in=valve2.press_out, sys_flow_in=valve2.flow_out)
valve3.press_drop(valve3.flow_in)
valve3.valve_flow_out(valve3.Cv, valve3.deltaP)
valve3.get_press_out(valve3.press_in)

pump2 = PositiveDisplacement("Gear Pump", displacement=0.096, press_out=30,
                             pump_head_in=utility_formulas.press_to_head(valve3.press_out))
pump2.adjust_speed(300)

relief1 = Relief("Relief 1", open_press=60, close_press=55, press_in=pump2.outlet_pressure)

throttle2 = Globe("Throttle 2", position=100, flow_coeff=21, press_in=pump2.outlet_pressure,
                  sys_flow_in=pump2.flow_rate_out)
throttle2.press_drop(throttle2.flow_in)
throttle2.valve_flow_out(throttle2.Cv, throttle2.deltaP)
throttle2.get_press_out(throttle2.press_in)

valve4 = Gate("Valve 4", position=100, flow_coeff=200, press_in=throttle2.press_out, sys_flow_in=throttle2.flow_out)
valve4.press_drop(valve4.flow_in)
valve4.valve_flow_out(valve4.Cv, valve4.deltaP)
valve4.get_press_out(valve4.press_in)


# # Utility functions
# def test_grav_flow():
#     flow_rate = utility_formulas.gravity_flow_rate(2, 1.67)
#     assert flow_rate == 319.28008077388426
#
#
# def test_static_press():
#     press = utility_formulas.static_press(14)
#     assert press == 6.0606060606060606
#
#
# # Gate Valve 1
# def test_v1_input_press():
#     assert valve1.press_in == 6.0606060606060606
#
#
# def test_v1_input_flow():
#     assert valve1.flow_in == 319.28008077388426
#
#
# def test_v1_press_drop():
#     assert valve1.deltaP == 2.5484942494744516
#
#
# def test_v1_output_flow():
#     assert valve1.flow_out == 319.28008077388426
#
#
# def test_v1_press_out():
#     assert valve1.press_out == 3.512111811131609
#
#
# # Centrifugal Pump
# def test_pump1_input_press():
#     assert pump1.head_in == 8.101304720057573
#
#
# def test_pump1_start_pump():
#     assert pump1.speed == 1750
#     assert pump1.flow_rate_out == 50
#     assert pump1.outlet_pressure == 16
#     assert pump1.wattage == 0.11777800491229948
#
#
# # Globe valve 1
# def test_t1_input_press():
#     assert throttle1.press_in == 16
#
#
# def test_t1_input_flow():
#     assert throttle1.flow_in == 50.0
#
#
# def test_t1_press_drop():
#     assert throttle1.deltaP == 5.668934240362812
#
#
# def test_t1_output_flow():
#     assert throttle1.flow_out == 50.0
#
#
# def test_t1_press_out():
#     assert throttle1.press_out == 10.331065759637188
#
#
# # Gate Valve 2
# def test_v2_input_press():
#     assert valve2.press_in == 10.331065759637188
#
#
# def test_v2_input_flow():
#     assert valve2.flow_in == 50.0
#
#
# def test_v2_press_drop():
#     assert valve2.deltaP == 0.0625
#
#
# def test_v2_output_flow():
#     assert valve2.flow_out == 50.0
#
#
# def test_v2_press_out():
#     assert valve2.press_out == 10.268565759637188
#
#
# # Gate Valve 3
# def test_v3_input_press():
#     assert valve3.press_in == 10.268565759637188
#
#
# def test_v3_input_flow():
#     assert valve3.flow_in == 50.0
#
#
# def test_v3_press_drop():
#     assert valve3.deltaP == 0.0625
#
#
# def test_v3_output_flow():
#     assert valve3.flow_out == 50.0
#
#
# def test_v3_press_out():
#     assert valve3.press_out == 10.206065759637188
#
#
# # Gear Pump
# def test_pump2_input_press():
#     assert pump2.head_in == 23.542088964737797
#
#
# def test_pump2_output():
#     assert pump2.speed == 300
#     assert pump2.flow_rate_out == 28.8
#     assert pump2.wattage == 0.10753003776038036
#
#
# # Relief Valve 1
# def test_relief1_input_press():
#     assert relief1.press_in == 30
#
#
# # Globe Valve 2
# def test_t2_input_press():
#     assert throttle2.press_in == 30
#
#
# def test_t2_input_flow():
#     assert throttle2.flow_in == 28.8
#
#
# def test_2_press_drop():
#     assert throttle2.deltaP == 1.8808163265306124
#
#
# def test_t2_output_flow():
#     assert throttle2.flow_out == 28.8
#
#
# def test_t2_press_out():
#     assert throttle2.press_out == 28.119183673469387
#
#
# # Gate Valve 4
# def test_v4_input_press():
#     assert valve4.press_in == 28.119183673469387
#
#
# def test_v4_input_flow():
#     assert valve4.flow_in == 28.8
#
#
# def test_v4_press_drop():
#     assert valve4.deltaP== 0.020736000000000004
#
#
# def test_v4_output_flow():
#     assert valve4.flow_out == 28.800000000000004
#
#
# def test_v4_press_out():
#     assert valve4.press_out == 28.098447673469387
