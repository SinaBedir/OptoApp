from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from database import Database
from kivy.core.window import Window


Window.softinput_mode = "below_target"
class Interface(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.quit)
        Database.connect()
    def quit(self, window, key, *args):
        if(key==27):
            MDApp.get_running_app().stop()

class OptoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Pink"
        self.theme_cls.primary_light_hue="300"
        self.theme_cls.accent_palette="Gray"
        self.theme_cls.accent_hue="700"
        self.theme_cls.accent_light_hue="50"
        self.theme_cls.material_style="M2"
        return super().build()

OptoApp().run()
