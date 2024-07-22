from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class RecScreen(Screen):
    pass

class RecApp(App):
    def build(self):
        return RecScreen()

if __name__ == "__main__":
    RecApp().run()