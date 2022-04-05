from kivy.uix.screenmanager import Screen
import json, random

from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu

from kivy_garden.mapview import MapMarker


class Indice3Screen(Screen):



    def __init__(self,**kwargs):
        super(Indice3Screen, self).__init__(**kwargs)

        self.create_page()
        Screen.clear_widgets(self)
        Screen.add_widget(self,self.page)

        self.loaded = False


    def create_page(self):

        self.page = MDFloatLayout(width="50")
        titre = MDLabel(text='Guess the station !',halign='center',font_style='H4',pos_hint={"center_x": .5, "center_y": 0.9})
        self.tour = MDLabel(text='',halign='center',font_style='H5',pos_hint={"center_x": .5, "center_y": 0.8})
        self.desc = MDLabel(text="",halign='center',pos_hint={"center_x": .5, "center_y": 0.75})


        
        abandon = MDRoundFlatButton(text='Je ne sais pas',pos_hint={"center_x": .35, "center_y": 0.15})
        abandon.bind(on_release = self.reveal_callback)




        self.page.add_widget(titre)
        self.page.add_widget(self.tour)
        self.page.add_widget(self.desc)
        self.page.add_widget(abandon)

    def reveal_callback(self,instance):
        self.data['score_maxi_round'] = 0
        open('data/guess.json','w').write(json.dumps(self.data))
        self.ids.map.remove_marker(self.marker)

        self.manager.current = "revelation"

    def validation_callback(self,instance):
        saisie = self.answer.current_item
        tour = self.data['tour']
        self.data = json.loads(open('data/guess.json','r').read())
        if saisie == "Sélectionnez une réponse":
            self.desc.text = "Veuillez sélectionner une réponse"
            return
        if saisie == self.data['selection'][tour-1]['StopName']:
            open('data/guess.json','w').write(json.dumps(self.data))
            self.ids.map.remove_marker(self.marker)
            self.manager.current = "revelation"
        else:
            self.data['score_maxi_round'] = self.data['score_maxi_round'] - 5
            open('data/guess.json','w').write(json.dumps(self.data))
            self.desc.text = "Mauvaise réponse !\nRetente ta chance ou abandonne"

            if(self.data['score_maxi_round'] <= 0):
                open('data/guess.json','w').write(json.dumps(self.data))
                self.ids.map.remove_marker(self.marker)
                self.manager.current = "revelation"


    def on_enter(self):

        self.desc.text = "Localisation précise"

        self.data = json.loads(open('data/guess.json','r').read())
        self.stops = json.loads(open('data/cts_stops.json','r').read())

        if(self.data['indice_round'] < 3):
            self.data['score_maxi_round'] = self.data['score_maxi_round'] - 15
            self.data['indice_round'] = 3
            open('data/guess.json','w').write(json.dumps(self.data))


        tour = self.data['tour']
        self.tour.text = "Tour "+str(tour)+"/5"
        station = self.data['selection'][tour-1]


        self.marker = MapMarker(lat=station['Latitude'], lon=station['Longitude'],source='include/map.png')
        self.ids.map.lat = station['Latitude']
        self.ids.map.lon = station['Longitude']
        self.ids.map.add_marker(self.marker)
        self.ids.map.zoom = 15


        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i['StopName']}",
                "on_release": lambda x=f"{i['StopName']}": self.set_item(x),
            } for i in self.data['propositions']
        ]
        menu_items.append({"viewclass":"OneLineListItem","text":"Sélectionnez une réponse"})

        if not self.loaded:

            self.answer = MDDropDownItem(pos_hint={"center_x": .5, "center_y": 0.3}, size_hint=(0.8,1),on_release = self.open_menu)
            self.menu = MDDropdownMenu(caller=self.answer,items=menu_items,position="center",width_mult=4, size_hint=(0.8,1))             
        
            

            valider = MDRoundFlatButton(text='Valider',pos_hint={"center_x": .65, "center_y": 0.15})
            valider.bind(on_release = self.validation_callback)

            self.page.add_widget(self.answer)
            self.page.add_widget(valider)

            self.loaded = True

        else:
            self.menu.items = menu_items

        self.answer.set_item("Sélectionnez une réponse")

    def open_menu(self, instance):
        self.menu.open()

    def set_item(self, text_item):
        self.answer.set_item(text_item)
        self.menu.dismiss()
