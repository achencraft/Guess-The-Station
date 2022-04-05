from kivy.uix.screenmanager import Screen


import json

from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundFlatButton 



class EndScreen(Screen):

   

    def __init__(self,**kwargs):
        super(EndScreen, self).__init__(**kwargs)

        self.create_page()
        Screen.clear_widgets(self)
        Screen.add_widget(self,self.page)


    def create_page(self):

        self.page = MDFloatLayout(width="50")
        titre = MDLabel(text='Guess the station !',halign='center',font_style='H3',pos_hint={"center_x": .5, "center_y": 0.9})
        desc = MDLabel(text="Récapitulatif",halign='center',pos_hint={"center_x": .5, "center_y": 0.70},font_style='H3')

        self.point = MDLabel(text="",halign='center',pos_hint={"center_x": .5, "center_y": 0.55},font_style='H5')
        self.recap = MDLabel(text="",halign='center',pos_hint={"center_x": .5, "center_y": 0.40})
                
        next = MDRoundFlatButton(text='Menu principal',pos_hint={"center_x": .5, "center_y": 0.1})
        next.bind(on_release = self.home_callback)



      
        self.page.add_widget(titre)
        self.page.add_widget(desc)
        self.page.add_widget(self.point)
        self.page.add_widget(self.recap)
        self.page.add_widget(next)

    def home_callback(self,instance):
        self.data['score_maxi_round'] = 100
        self.data['tour'] = self.data['tour'] + 1
        open('data/guess.json','w').write(json.dumps(self.data))
        
        self.manager.current = "home"  

    def on_enter(self):

        self.data = json.loads(open('data/guess.json','r').read())

        self.data['lastscore'] = self.data['score_game']

        self.point.text = "Points de cette partie: "+str(self.data['score_game'])

        if(self.data['score_game'] > self.data['bestscore']):

            print(self.data['bestscore'])
            self.data['bestscore'] = self.data['score_game']
            self.point.text = self.point.text + "\nNouveau record !"


        compteur = 1
        self.recap.text = ""
        for stop in self.data['selection']:
            self.recap.text = self.recap.text + '#'+str(compteur) + " - " + stop['StopName'] + " : " + str(stop['Points']) + "\n"
            compteur = compteur + 1

        
        

        open('data/guess.json','w').write(json.dumps(self.data))

