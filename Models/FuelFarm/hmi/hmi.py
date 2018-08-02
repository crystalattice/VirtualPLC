import Models.FuelFarm.components as components
import Models.FuelFarm.functionality as functionality

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

import kivy
kivy.require("1.10.0")

Config.set("graphics", "width", "1062")
Config.set("graphics", "height", "849")
Config.set("graphics", "resizable", False)

# print(components.tank1.level)
# print(components.tank1.static_tank_press)


class HMI(FloatLayout):

    @staticmethod
    def on_state(valve):  # Get the status of the valve
        # if valve.group == "valve1":
        if valve.state == "down":
            # print(valve.group, "Opened")
            exec("functionality.{}_open()".format(valve.group))  # Dynamically call valve function
            # functionality.gate1_open()
        else:
            # print(valve.group, "Closed")
            exec("functionality.{}_close()".format(valve.group))




class HMIApp(App):
    def build(self):
        return HMI()


if __name__ == "__main__":
    HMIApp().run()