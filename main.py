import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen


class StartScreen(Screen):
    pass



class RootScreen(ScreenManager):
    pass


class FlappyApp(App):
    def build(self):
        return RootScreen()


if __name__ == "__main__":
    FlappyApp().run()