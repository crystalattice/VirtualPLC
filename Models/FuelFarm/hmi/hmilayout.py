import Models.FuelFarm.components as components
import Models.FuelFarm.functionality as functionality
from random import sample
from string import ascii_lowercase

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.lang import Builder

import kivy
kivy.require("1.10.0")

Config.set("graphics", "width", "1112")
Config.set("graphics", "height", "849")
Config.set("graphics", "resizable", False)


class HMILayout(PageLayout):
    # Methods are associated with their class; each class would have its own .kv file
    @staticmethod
    def on_state(valve):  # Get the status of the valve
        if valve.state == "down":
            # print(valve.group, "Opened")
            exec("functionality.{}_open()".format(valve.group))  # Dynamically call valve open()
        else:
            # print(valve.group, "Closed")
            exec("functionality.{}_close()".format(valve.group))  # Dynamically call valve close()

    def populate(self):
        tank_properties1 = {}
        tank_properties2 = {}
        valve_properties1 = {}
        valve_properties2 = {}
        valve_properties3 = {}
        valve_properties4 = {}
        valve_properties5 = {}
        valve_properties6 = {}
        valve_properties7 = {}

        # Convert instances to dictionaries
        for key, value in vars(components.tank1).items():
            tank_properties1[key] = value
        for key, value in vars(components.tank2).items():
            tank_properties2[key] = value

        for key, value in vars(components.gate1).items():
            valve_properties1[key] = value
        for key, value in vars(components.gate2).items():
            valve_properties2[key] = value
        for key, value in vars(components.gate3).items():
            valve_properties3[key] = value
        for key, value in vars(components.gate4).items():
            valve_properties4[key] = value
        for key, value in vars(components.gate5).items():
            valve_properties5[key] = value
        for key, value in vars(components.gate6).items():
            valve_properties6[key] = value
        for key, value in vars(components.gate7).items():
            valve_properties7[key] = value

        # Populate table
        self.table.data = [{"value": "Tank"}, {"value": "Level"}, {"value": "Pressure Out"}, {"value": "Flow Out"},
                           {"value": ""}, {"value": ""},
                           # Tank 1
                           {"value": tank_properties1["name"]},
                           {"value": str(tank_properties1["_Tank__level"])},
                           {"value": "{:.2f}".format((tank_properties1["_Tank__tank_press"]))},
                           {"value": "{:.2f}".format((tank_properties1["flow_out"]))},
                           {"value": ""},
                           {"value": ""},
                           # Tank 2
                           {"value": tank_properties2["name"]},
                           {"value": str(tank_properties2["_Tank__level"])},
                           {"value": "{:.2f}".format((tank_properties2["_Tank__tank_press"]))},
                           {"value": "{:.2f}".format((tank_properties2["flow_out"]))},
                           {"value": ""},
                           {"value": ""},

                           {"value": "Valve"}, {"value": "Position"}, {"value": "Pressure In"}, {"value": "Flow In"},
                           {"value": "Pressure Out"}, {"value": "Flow Out"},
                           # Valve 1
                           {"value": valve_properties1["name"]},
                           {"value": str(valve_properties1["_Valve__position"])},
                           {"value": "{:.2f}".format((valve_properties1["press_in"]))},
                           {"value": "{:.2f}".format((valve_properties1["flow_in"]))},
                           {"value": "{:.2f}".format((valve_properties1["press_out"]))},
                           {"value": "{:.2f}".format((valve_properties1["flow_out"]))},
                           # Valve 2
                           {"value": valve_properties2["name"]},
                           {"value": str(valve_properties2["_Valve__position"])},
                           {"value": "{:.2f}".format((valve_properties2["press_in"]))},
                           {"value": "{:.2f}".format((valve_properties2["flow_in"]))},
                           {"value": "{:.2f}".format((valve_properties2["press_out"]))},
                           {"value": "{:.2f}".format((valve_properties2["flow_out"]))},
                           # Valve 3
                           {"value": valve_properties3["name"]},
                           {"value": str(valve_properties3["_Valve__position"])},
                           {"value": "{:.2f}".format((valve_properties3["press_in"]))},
                           {"value": "{:.2f}".format((valve_properties3["flow_in"]))},
                           {"value": "{:.2f}".format((valve_properties3["press_out"]))},
                           {"value": "{:.2f}".format((valve_properties3["flow_out"]))},
                           # Valve 4
                           {"value": valve_properties4["name"]},
                           {"value": str(valve_properties4["_Valve__position"])},
                           {"value": "{:.2f}".format((valve_properties4["press_in"]))},
                           {"value": "{:.2f}".format((valve_properties4["flow_in"]))},
                           {"value": "{:.2f}".format((valve_properties4["press_out"]))},
                           {"value": "{:.2f}".format((valve_properties4["flow_out"]))},
                           # Valve 5
                           {"value": valve_properties5["name"]},
                           {"value": str(valve_properties5["_Valve__position"])},
                           {"value": "{:.2f}".format((valve_properties5["press_in"]))},
                           {"value": "{:.2f}".format((valve_properties5["flow_in"]))},
                           {"value": "{:.2f}".format((valve_properties5["press_out"]))},
                           {"value": "{:.2f}".format((valve_properties5["flow_out"]))},
                           # Valve 6
                           {"value": valve_properties6["name"]},
                           {"value": str(valve_properties6["_Valve__position"])},
                           {"value": "{:.2f}".format((valve_properties6["press_in"]))},
                           {"value": "{:.2f}".format((valve_properties6["flow_in"]))},
                           {"value": "{:.2f}".format((valve_properties6["press_out"]))},
                           {"value": "{:.2f}".format((valve_properties6["flow_out"]))},
                           # Valve 7
                           {"value": valve_properties7["name"]},
                           {"value": str(valve_properties7["_Valve__position"])},
                           {"value": "{:.2f}".format((valve_properties7["press_in"]))},
                           {"value": "{:.2f}".format((valve_properties7["flow_in"]))},
                           {"value": "{:.2f}".format((valve_properties7["press_out"]))},
                           {"value": "{:.2f}".format((valve_properties7["flow_out"]))},
                           ]

    def sort(self):
        self.table.data = sorted(self.table.data, key=lambda x: x['value'])

    def clear(self):
        self.table.data = []

    def insert(self, value):
        self.table.data.insert(0, {'value': value or 'default value'})

    def update(self, value):
        if self.table.data:
            self.table.data[0]['value'] = value or 'default new value'
            self.table.refresh_from_data()

    def remove(self):
        if self.table.data:
            self.table.data.pop(0)


class HMIApp(App):
    def build(self):
        return HMILayout()


if __name__ == "__main__":
    HMIApp().run()
