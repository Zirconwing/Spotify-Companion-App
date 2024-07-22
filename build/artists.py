from kivy.app import App
from kivy.uix.screenmanager import Screen

class ArtistsScreen(Screen):
    pass

class ArtistsApp(App):
    def build(self):
        return ArtistsScreen()


if __name__ == "__main__":
    ArtistsApp().run()