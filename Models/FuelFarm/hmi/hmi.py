import Models.FuelFarm.components as components
import Models.FuelFarm.functionality as functionality

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

import kivy
kivy.require("1.10.0")

Config.set("graphics", "width", "1062")
Config.set("graphics", "height", "849")

# print(components.tank1.level)
# print(components.tank1.static_tank_press)


class HMI(FloatLayout):

    @staticmethod
    def on_state(valve):  # Get the status of the valve
        # if valve.group == "valve2":
        if valve.state == "down":
            print(valve.group, "Opened")
        else:
            print(valve.group, "Closed")


class HMIApp(App):
    def build(self):
        return HMI()


if __name__ == "__main__":
    HMIApp().run()