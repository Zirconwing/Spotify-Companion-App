from kivy.app import App
from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    pass

class HomeApp(App):
    def build(self):
        self.icon = "applogo.png"
        return HomeScreen()

if __name__ == "__main__":
    app = HomeApp()
    app.run()