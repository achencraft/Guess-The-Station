from kivy.uix.screenmanager import Screen
from kivy.utils import platform
if platform == 'android':
    from jnius import autoclass
    from android import mActivity
if platform in ('linux', 'linux2', 'macos', 'win'):
    from runpy import run_path
    from threading import Thread    

from oscpy.server import OSCThreadServer
import os, json, random

from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton 


class HomeScreen(Screen):

    
   
    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.bestscore = "Meilleur score : "
        self.lastscore = "Dernier score : "
        serveur = OSCThreadServer()

        serveur.listen('localhost', port=3000, default=True)
        serveur.bind(b'/ok', self.afficher_home)
        serveur.bind(b'/error', self.afficher_error)
        serveur.bind(b'/step', self.afficher_load_step)

        if not os.path.exists('data/guess.json'):
            self.init_data_file()
        else:
            self.data = json.loads(open('data/guess.json').read())
        
        self.creer_loading_card()
        self.creer_error_card()
        self.creer_home_page()
        self.afficher_load()

        if not os.path.isdir('include/music') or not os.path.isfile('data/cts_stops.json'):
            self.start_update()
        else:
            self.afficher_home()


    def on_enter(self):
        self.data = json.loads(open('data/guess.json','r').read())



    def start(self, instance):
        self.manager.current = "sound"
        
        stops = json.loads(open('data/cts_stops.json','r').read())
        selection_id = []
        selection = []

        while not len(selection_id) == 5:
            rand_int = random.randint(0,len(stops)-1)
            if not rand_int in selection_id:
                selection_id.append(rand_int)
                selection.append(stops[rand_int])

        self.data['selection'] = selection
        self.data['tour'] = 1
        self.data['score_game'] = 0
        self.data['score_maxi_round'] = 100
        self.data['indice_round'] = 0

        open('data/guess.json','w').write(json.dumps(self.data))  

        print(selection)  



    def creer_loading_card(self):
        self.loading = MDFloatLayout()
        if platform == 'android':
            logo = AsyncImage(source='include/guess_the_station_transparent.png',size_hint_x=0.4,pos_hint={"center_x": .5, "center_y": 0.8})
        else:
            logo = AsyncImage(source='include/guess_the_station_transparent.png',size_hint_x=0.2,pos_hint={"center_x": .5, "center_y": 0.8})
 
        titre = MDLabel(text='Chargement des ressources',halign='center',font_style='H5')
        self.gif = AsyncImage(source='include/loading.gif',size_hint_x=0.1,pos_hint={"center_x": .5, "center_y": 0.3})
        self.step = MDLabel(halign='center',pos_hint={"center_x": .5, "center_y": 0.1})
        
        self.loading.add_widget(logo)
        self.loading.add_widget(titre)
        self.loading.add_widget(self.gif)
        self.loading.add_widget(self.step)


    def creer_error_card(self):
        self.error = MDFloatLayout()
        if platform == 'android':
            logo = AsyncImage(source='include/guess_the_station_transparent.png',size_hint_x=0.4,pos_hint={"center_x": .5, "center_y": 0.8})
        else:
            logo = AsyncImage(source='include/guess_the_station_transparent.png',size_hint_x=0.2,pos_hint={"center_x": .5, "center_y": 0.8})
 
        titre = MDLabel(text='Echec du téléchargement',halign='center',font_style='H5')
        gif = AsyncImage(source='include/error.png',size_hint_x=0.1,pos_hint={"center_x": .5, "center_y": 0.3})

        self.error.add_widget(logo)
        self.error.add_widget(titre)
        self.error.add_widget(gif)


    def creer_home_page(self):
        self.home = MDFloatLayout()
        if platform == 'android':
            logo = AsyncImage(source='include/guess_the_station_transparent.png',size_hint_x=0.4,pos_hint={"center_x": .5, "center_y": 0.8})
        else:
            logo = AsyncImage(source='include/guess_the_station_transparent.png',size_hint_x=0.2,pos_hint={"center_x": .5, "center_y": 0.8})
        titre = MDLabel(text='Guess the station',halign='center',font_style='H2')
        play = MDRoundFlatButton(text='JOUER',pos_hint={"center_x": .5, "center_y": 0.1})
        play.bind(on_release = self.start)

        score = MDBoxLayout(pos_hint= {"center_x": .5, "center_y": 0.25})
        self.bestscore_label = MDLabel(text="Meilleur score\n"+str(self.data['bestscore']),halign='center',font_style='H5')
        self.lastscore_label = MDLabel(text="Dernier score\n"+str(self.data['lastscore']),halign='center',font_style='H5')

        self.home.add_widget(logo)
        self.home.add_widget(titre)
        self.home.add_widget(play)
        score.add_widget(self.bestscore_label)
        score.add_widget(self.lastscore_label)
        self.home.add_widget(score)

    def afficher_home(self):
        Screen.clear_widgets(self)
        Screen.add_widget(self,self.home)

    def afficher_error(self):
        Screen.clear_widgets(self)
        Screen.add_widget(self,self.error)

    def afficher_load(self):
        Screen.clear_widgets(self)
        Screen.add_widget(self,self.loading)

    def afficher_load_step(self, message):
        msg = message.decode('utf8')
        self.step.text = message.decode('utf8')

        if msg == "OK !":
            self.gif.source ='include/ok.png'

        
    def init_data_file(self):
        if not os.path.exists('data'):
                os.mkdir('data')

        data = {
            'bestscore':0,
            'lastscore':0
        }

        self.data = data
        open("data/guess.json", "w").write(json.dumps(data))



    def start_update(self):
        if platform == 'android':            
            context =  mActivity.getApplicationContext()
            SERVICE_NAME = str(context.getPackageName()) + '.Service' + 'Update'
            self.service = autoclass(SERVICE_NAME)
            self.service.start(mActivity,'')


        elif platform in ('linux', 'linux2', 'macos', 'win'):
            self.service = Thread(
                target=run_path,
                args=['service/update.py'],
                kwargs={'run_name': '__main__'},
                daemon=True
            )
            self.service.start()
        else:
            raise NotImplementedError(
                "service start not implemented on this platform"
            )



    def on_enter(self):

        self.data = json.loads(open('data/guess.json','r').read())
        self.bestscore_label.text = "Meilleur score\n"+str(self.data['bestscore'])
        self.lastscore_label.text = "Dernier score\n"+str(self.data['lastscore'])
