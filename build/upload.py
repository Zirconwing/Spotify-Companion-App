from kivy.app import App
from kivy.uix.screenmanager import Screen

class UploadScreen(Screen):
    def selected(self, filename):
        self.ids.my_label.text = filename[0]
        


class UploadApp(App):
    def build(self):
        return UploadScreen()

    
if __name__ == '__main__':
    UploadApp().run()

