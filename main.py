
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission


from pages.End import EndScreen
from pages.Home import HomeScreen
from pages.Indice1 import Indice1Screen
from pages.Indice2 import Indice2Screen
from pages.Indice3 import Indice3Screen
from pages.Revelation import RevealScreen
from pages.Sound import SoundScreen



class MyApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        if platform == 'android':      
            request_permissions([Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION])



    def build(self):
        return Builder.load_file("main.kv")


MyApp().run()
