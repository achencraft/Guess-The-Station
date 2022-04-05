import requests, os, json, time, zipfile
from oscpy.client import OSCClient

class UpdateService():

    Client = OSCClient('localhost', 3000)
    TOKEN = '<TOKEN API CTS>'
    
    def run(self):

        
        self.stationInfoFile = "data/data_brute.json"
        self.stationInfoFileProc = "data/cts_stops.json"
        
        

        if not os.path.isdir('include/music'):

            #### ETAPE 1 - Téléchargement des musiques
            time.sleep(0.5)
            self.Client.send_message(b'/step',["Téléchargement des musiques (1/4)".encode('utf8'),],)
            r = requests.Response()
            url = '<LIEN VERS LES MUSIQUES>/cts-musiques.zip'
            try:
                r = requests.get(url, allow_redirects=True)
            except:
                self.Client.send_message(b'/error',[],)
            open('include/cts-musiques.zip', 'wb').write(r.content)

            #### ETAPE 2 - Extraction des musiques
            time.sleep(0.5)
            self.Client.send_message(b'/step',["Extraction des musiques (2/4)".encode('utf8'),],)
            with zipfile.ZipFile('include/cts-musiques.zip', 'r') as zip_ref:
                zip_ref.extractall('include/music')
            os.remove("include/cts-musiques.zip") 

        if not os.path.isfile('data/cts_stops.json'):

            if not os.path.isdir('data'):
                os.mkdir('data')

            #### ETAPE 3 - Téléchargement des stations
            time.sleep(0.5)
            self.Client.send_message(b'/step',["Téléchargement des stations (3/4)".encode('utf8'),],)
            r = requests.Response()
            url = 'https://api.cts-strasbourg.eu/v1/siri/2.0/stoppoints-discovery?includeLinesDestinations=true'
            try:
                r = requests.get(url,auth=(self.TOKEN,''))
            except:
                self.Client.send_message(b'/error',[],)
            open("data/data_brute.json", "w").write(r.text)
            

            #### ETAPE 4 - Conversion des stations
            time.sleep(0.5)
            self.Client.send_message(b'/step',["Conversion des stations (4/4)".encode('utf8'),],)
            self.convert_stopList()
            os.remove("data/data_brute.json") 


            self.Client.send_message(b'/step',["OK !".encode('utf8')],)
            time.sleep(3)

        self.Client.send_message(b'/ok',[],)





    def convert_stopList(self):
        
        f = open(self.stationInfoFile)
        data = json.load(f)
        res = []
        stopNames = []
        for d in data["StopPointsDelivery"]["AnnotatedStopPointRef"]:
            istram = False
            if "Lines" not in d:
                continue
            for l in d["Lines"]:
                if l["Extension"]["RouteType"] == "tram":
                    istram = True
                    break
            if istram:
                if d["StopName"] not in stopNames:
                    newadd = {}
                    newadd["StopPointRef"] = d["StopPointRef"].split("_")[0]
                    newadd["StopName"] = d["StopName"]
                    newadd["Longitude"] = d["Location"]["Longitude"]
                    newadd["Latitude"] = d["Location"]["Latitude"]
                    newadd["LogicalStopCode"] = d["Extension"]["LogicalStopCode"]
                    newadd["Lines"] = []
                    for l in d["Lines"]:
                        if l["LineRef"] not in newadd["Lines"]:
                            newadd["Lines"].append(l["LineRef"])

                    if d["StopPointRef"].split("_")[0] in ["ARBRI","CITAD","PRRHI"]:
                        newadd["Lines"] = ['D']

                    stopNames.append(d["StopName"])
                    res.append(newadd)
                else:
                    index = -1
                    for i in range(len(res)):
                        if res[i]["StopName"] == d["StopName"]:
                            index = i
                            break
                    if index == -1:
                        print("how ???")
                        print(d["StopPointRef"])
                    for l in d["Lines"]:
                        if l["LineRef"] not in res[index]["Lines"]:
                            res[index]["Lines"].append(l["LineRef"])
        for r in res:
            response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={r['Latitude']}&lon={r['Longitude']}")
            if response.status_code == requests.codes.ok:
                jsn = response.json()
                if "city" in jsn["address"]:
                    r["Ville"] = jsn["address"]["city"]
                elif "town" in jsn["address"]:
                    r["Ville"] = jsn["address"]["town"]
                elif "postcode" in jsn["address"] and jsn["address"]["postcode"] == "67300":
                    r["Ville"] = "Schiltigheim"
                else:
                    r["Ville"] = "Strasbourg"
            else:
                print("Failed to get data")
                print(r)
        with open(self.stationInfoFileProc, "w") as outfile:
            json.dump(res, outfile)
    

if __name__ == '__main__':
    UpdateService().run()
    
    
