from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.utils import platform

if platform in ('linux', 'linux2', 'macos', 'win'):
    from playsound import playsound

import json, os, random

from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundFlatButton, MDIconButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu



class SoundScreen(Screen):





    def __init__(self,**kwargs):
        super(SoundScreen, self).__init__(**kwargs)

        self.create_page()
        Screen.clear_widgets(self)
        Screen.add_widget(self,self.page)



    def create_page(self):

        self.page = MDFloatLayout(width="50")
        titre = MDLabel(text='Guess the station !',halign='center',font_style='H4',pos_hint={"center_x": .5, "center_y": 0.9})
        self.tour = MDLabel(text='',halign='center',font_style='H5',pos_hint={"center_x": .5, "center_y": 0.8})
        self.desc = MDLabel(text="écoutez l'annonce sonore",halign='center',pos_hint={"center_x": .5, "center_y": 0.65})

        
        

        self.page.add_widget(titre)
        self.page.add_widget(self.tour)
        self.page.add_widget(self.desc)
        

    def play_sound(self, instance):
        if(instance.icon == "play"):

            instance.icon = 'stop'
            if platform == 'android':
                if self.sound:
                    self.sound.on_stop = self.reset_sound
                    self.sound.play()
            else:
                playsound("include/music/"+self.soundname,False)
        else:
            instance.icon = "play"
            if platform == 'android':
                self.sound.stop()

    def reset_sound(self):
        self.icon.icon = "play"



    def next_indice_callback(self, instance):

        open('data/guess.json','w').write(json.dumps(self.data))

        if os.path.exists("include/music/"+self.soundname):
            if platform == 'android':
                self.sound.stop()

        self.manager.current = "indice1"


    def validation_callback(self, instance):

        saisie = self.answer.current_item
        tour = self.data['tour']
        self.data = json.loads(open('data/guess.json','r').read())
        if saisie == "Sélectionnez une réponse":
            self.desc.text = "Veuillez sélectionner une réponse"
            return
        if saisie == self.data['selection'][tour-1]['StopName']:
            open('data/guess.json','w').write(json.dumps(self.data))
            if os.path.exists("include/music/"+self.soundname):
                if platform == 'android':
                    self.sound.stop()
            self.manager.current = "revelation"
        else:
            self.data['score_maxi_round'] = self.data['score_maxi_round'] - 5
            open('data/guess.json','w').write(json.dumps(self.data))
            self.desc.text = "Mauvaise réponse !\nRetente ta chance ou débloque un indice"

            if(self.data['score_maxi_round'] <= 0):
                open('data/guess.json','w').write(json.dumps(self.data))
                if os.path.exists("include/music/"+self.soundname):
                    if platform == 'android':
                        self.sound.stop()
                self.manager.current = "revelation"

    def on_enter(self):

        self.create_page()
        Screen.clear_widgets(self)
        Screen.add_widget(self,self.page)


        self.data = json.loads(open('data/guess.json','r').read())
        self.stops = json.loads(open('data/cts_stops.json','r').read())

        tour = self.data['tour']
        station = self.data['selection'][tour-1]
        self.soundname = station['StopPointRef']+".ogg"


        self.tour.text = "Tour "+str(tour)+"/5"


        lst_all = [i for i in sorted(self.stops, key=lambda d: d['StopName'])]
        lst_tmp = [station]
        while (len(lst_tmp) < 10):
            tmp = random.choice(lst_all)
            if tmp not in lst_tmp:
                lst_tmp.append(tmp)
        lst_tmp = sorted(lst_tmp, key = lambda x: x['StopName'])
        self.data['propositions'] = lst_tmp
        open('data/guess.json','w').write(json.dumps(self.data))
        print(self.data['propositions'])

        if os.path.exists("include/music/"+self.soundname):
            if platform == 'android':
                self.sound = SoundLoader.load("include/music/"+self.soundname)

            self.icon = MDIconButton(icon='play',user_font_size="72sp",pos_hint={"center_x": .5, "center_y": 0.5})        
            self.icon.bind(on_release = self.play_sound)   

            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": f"{i['StopName']}",
                    "on_release": lambda x=f"{i['StopName']}": self.set_item(x),
                } for i in self.data['propositions']
            ]

            menu_items.append({"viewclass":"OneLineListItem","text":"Sélectionnez une réponse"})

            self.answer = MDDropDownItem(pos_hint={"center_x": .5, "center_y": 0.3}, size_hint=(0.8,1),on_release = self.open_menu)
            self.menu = MDDropdownMenu(caller=self.answer,items=menu_items,position="center",width_mult=4, size_hint=(0.8,1))             

            self.page.add_widget(self.answer)
            self.answer.set_item("Sélectionnez une réponse")

            valider = MDRoundFlatButton(text='Valider',pos_hint={"center_x": .65, "center_y": 0.15})
            indice = MDRoundFlatButton(text='Indice',pos_hint={"center_x": .35, "center_y": 0.15})
            valider.bind(on_release = self.validation_callback)
            self.page.add_widget(valider)
        else:
            print('no audio')
            self.icon = MDIconButton(icon='volume-off',user_font_size="96sp",pos_hint={"center_x": .5, "center_y": 0.4})
            indice = MDRoundFlatButton(text='Indice',pos_hint={"center_x": .5, "center_y": 0.2}) 
            self.desc.text = "Aucune annonce sonore pour cette station.\nUtilisez l'indice gratuitement.\nScore x2"
            self.data['indice_round'] = 1


        self.page.add_widget(self.icon)
        indice.bind(on_release = self.next_indice_callback)
        self.page.add_widget(indice)
        




    def open_menu(self, instance):
        self.menu.open()

    def set_item(self, text_item):
        self.answer.set_item(text_item)
        self.menu.dismiss()
