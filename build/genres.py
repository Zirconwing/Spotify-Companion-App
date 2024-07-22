from kivy.app import App
from kivy.uix.screenmanager import Screen

class GenresScreen(Screen):
    pass

class GenresApp(App):
    def build(self):
        return GenresScreen()


if __name__ == "__main__":
    GenresApp().run()