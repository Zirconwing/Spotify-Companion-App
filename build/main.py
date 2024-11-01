from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ListProperty
from kivy import platform
from home import HomeScreen
from Recommendations import RecScreen
from genres import GenresScreen
from artists import ArtistsScreen
from menu import MenuScreen
from tracks import TracksScreen
from upload import UploadScreen
import string
import webbrowser as web
import json
class LoginManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        self.icon = "applogo.png"
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE])
        return LoginManager()
    def web_open(self):
        web.open_new_tab('http://spotify-companion-app-production.up.railway.app/')
    rec = ListProperty(['']*5)
    art = ListProperty(['']*5)
    gen = ListProperty(['']*5)
    track = ListProperty(['']*5) 
    filename = ''
    def pressed(self, filename):
        try:
            self.filename = filename[0]
            if self.filename.endswith(".json"):
                self.root.current = "HomeScreen"
        except:
            pass
    def contents(self):
        try:
            f = open(self.filename, 'r')
            file = json.loads(f.read())
            f.close()
            self.vals = file
        except (json.decoder.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
            self.root.current = "LoginScreen"
    def recommendations(self):
        x = 0
        for i in self.vals["recommendations"]:
            self.rec[x] = i
            x += 1
    def artists(self):
        x = 0
        for i in self.vals["artists"]:
            self.art[x] = i
            x += 1
    def genres(self):
        x = 0
        for i in self.vals["genres"]:
            self.gen[x] = string.capwords(i)
            x += 1
    def tracks(self):
        x = 0
        for i in self.vals["tracks"]:
            self.track[x] = i
            x += 1

MainApp().run()