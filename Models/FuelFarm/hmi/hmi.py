from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


class Background(ScreenManager):
    pass


class HMIApp(App):
    def build(self):
        return Background()


if __name__ == "__main__":
    HMIApp().run()
