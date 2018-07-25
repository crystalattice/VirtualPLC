import kivy
kivy.require("1.10.0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.config import Config

Config.set("graphics", "width", "1062")
Config.set("graphics", "height", "849")


class Background(Widget):
    pass


class HMIApp(App):
    def build(self):
        return Background()


if __name__ == "__main__":
    HMIApp().run()
