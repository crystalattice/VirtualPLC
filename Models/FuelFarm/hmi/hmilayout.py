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
        self.table.data = [{'value': ''.join(sample(ascii_lowercase, 6))}
                           for x in range(50)]

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
