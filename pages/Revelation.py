from kivy.uix.screenmanager import Screen

import json, os

from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton 




class RevealScreen(Screen):

   

    def __init__(self,**kwargs):
        super(RevealScreen, self).__init__(**kwargs)
        self.create_page()
        Screen.clear_widgets(self)
        Screen.add_widget(self,self.page)


    def create_page(self):

        self.page = MDFloatLayout(width="50")
        titre = MDLabel(text='Guess the station !',halign='center',font_style='H3',pos_hint={"center_x": .5, "center_y": 0.9})
        self.desc = MDLabel(text="",halign='center',pos_hint={"center_x": .5, "center_y": 0.70},font_style='H3')

        self.responce = MDLabel(text="",halign='center',pos_hint={"center_x": .5, "center_y": 0.55},font_style='H4')

        score = MDBoxLayout(pos_hint= {"center_x": .5, "center_y": 0.35})
        self.point = MDLabel(text="",halign='center',font_style='H5')
        self.point_partie = MDLabel(text="",halign='center',font_style='H5')

        self.multi = MDLabel(text="",halign='center',font_style='H5',pos_hint={"center_x": .5, "center_y": 0.2})
        
        self.next = MDRoundFlatButton(text='',pos_hint={"center_x": .5, "center_y": 0.1})
        self.next.bind(on_release = self.next_callback)



      
        self.page.add_widget(titre)
        self.page.add_widget(self.desc)
        self.page.add_widget(self.responce)
        score.add_widget(self.point)
        score.add_widget(self.point_partie)
        self.page.add_widget(score)
        self.page.add_widget(self.multi)
        self.page.add_widget(self.next)

    def next_callback(self,instance):
        self.data['score_maxi_round'] = 100
        self.data['tour'] = self.data['tour'] + 1
        self.data['indice_round'] = 0
        open('data/guess.json','w').write(json.dumps(self.data))
        
        if self.tour == 5:
            self.manager.current = "recapitulatif"  
        else:
            self.manager.current = "sound"

    def on_enter(self):

        self.data = json.loads(open('data/guess.json','r').read())
        self.multi.text = ""
        
        open('data/guess.json','w').write(json.dumps(self.data))

        self.tour = self.data['tour']
        station = self.data['selection'][self.tour-1]

        self.desc.text = "Tour "+str(self.tour)
        self.responce.text = station['StopName']



        self.point.text = "Points obtenus\n"+str(self.data['score_maxi_round'])
        

        self.data['selection'][self.tour-1]['Points'] = self.data['score_maxi_round']


        self.soundname = station['StopPointRef']+".ogg"        
        if not os.path.exists("include/music/"+self.soundname):
            self.point.text = self.point.text
            self.multi.text = "Points x2"
            self.data['selection'][self.tour-1]['Points'] = self.data['score_maxi_round'] * 2
            self.data['score_maxi_round'] = self.data['score_maxi_round'] * 2
            open('data/guess.json','w').write(json.dumps(self.data))


        self.data['score_game'] = self.data['score_game'] + self.data['score_maxi_round']
        self.point_partie.text = "Points totaux\n"+str(self.data['score_game'])

        if self.tour == 5:
            self.next.text = "Récapitulatif"
        else:
            self.next.text = "Station suivante"
