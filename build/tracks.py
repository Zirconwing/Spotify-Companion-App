from kivy.app import App
from kivy.uix.screenmanager import Screen

class TracksScreen(Screen):
    pass

class TracksApp(App):
    def build(self):
        return TracksScreen()


if __name__ == "__main__":
    TracksApp().run()