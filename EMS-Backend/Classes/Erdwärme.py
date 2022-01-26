import urllib.request, json , urllib.parse
import requests
import urllib.parse
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import unary_union
import matplotlib.pyplot as plt 

def Get_GeothermalData(input_GeoData : dict)-> dict: 

    #Inputdictionary entpacken
    str_address = input_GeoData["Adresse"]
    flt_depthprobe = input_GeoData["Bohrtiefe"]

  

    #Get Erdwärmedaten für Wien
    with urllib.request.urlopen("https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:ERDWSONDOGD") as url:
        data = json.loads(url.read().decode())
    #Die Potenzialkarten für Erdwärmesonden zeigen kein eigentliches Potenzial in Form einer Energiemenge pro Flächen- oder Zeiteinheit,
    #sondern die konduktive Wärmeleitfähigkeit, gemittelt über drei Tiefenbereiche (0 bis 30, 0 bis 100 und 0 bis 200 Meter) in der Einheit W/m/K. 
    #Dieser Parameter ist von den geologischen und hydrogeologischen Gegebenheiten abhängig und dient als Basis für die Berechnung der nutzbaren Energiemenge. 
    #Um diese vollständig berechnen zu können, ist die mittlere Bodentemperatur und die Betriebsweise der Erdsondenanlage (Heizen/Kühlen, Volllaststunden) notwendig.

    #Die mittlere Bodentemperatur zur Dimensionierung von Erdwärmesonden kann für das Bundesland Wien folgendermaßen abgeschätzt werden:
    #Tiefenintervall 0 bis 30 Meter: 12 +/- 2 °C
    #Tiefenintervall 0 bis 100 Meter: 12 +/- 1 °C
    #Tiefenintervall 0 bis 200 Meter: 14 +/- 1 °C
    #Quelle: https://www.wien.gv.at/stadtentwicklung/energie/themenstadtplan/erdwaerme/erlaeuterungen.html


    #Die relevanten Daten werden extrahiert und in dic_Polygons abgelegt
    #Relevante Daten:
        #Koordinaten welche das Polygon bestimmen
    dic_Polygons = {}


  
    li_lengths = []
    li_lengths_feature = []
    for feature in data["features"]:
        li_coordinates = []
    
        #Liest die Längen der einzelnen Features aus
        #Manche Features haben vernestete Koordinaten die in einem Loop ausgelesen werden müssen
        li_lengths_feature.append(len(feature["geometry"]["coordinates"]))
        if len(feature["geometry"]["coordinates"]) == 1:
            li_lengths.append(len(feature["geometry"]["coordinates"]))
        elif len(feature["geometry"]["coordinates"]) > 1:
            for coords in feature["geometry"]["coordinates"]:
                li_lengths.append(len(coords))

        for coords in feature["geometry"]["coordinates"]:
            li_coordinates.append(coords)
    
        dic_Polygons[feature["id"]] = li_coordinates


    it_floor = 0
    it_ceiling = 0
    li_lengths_new = []
    #Dieser Loop berechnet nun die richtige länge der einzelnen Features 
    for it,item in enumerate(li_lengths_feature, start = 1):
        it_ceiling = sum(li_lengths_feature[0:it])
        item = sum(li_lengths[it_floor:it_ceiling])
        it_floor = sum(li_lengths_feature[0:it])
        li_lengths_new.append(item)

    #Funktion von Simon um eine Adresse in Koordinaten zu wandeln
    def from_address(address_string="Stephansplatz, Wien, Österreich"):
        parsed_address = urllib.parse.quote(address_string)
        url = 'https://nominatim.openstreetmap.org/search/' + parsed_address +'?format=json'
        response = requests.get(url).json()
        location = (float(response[0]["lon"]), float(response[0]["lat"]) )
        return location
    
    coordinateAddress = from_address(str_address)

    def IsPointInsidePolygon(var_polygon, point):
        #Diese Funktion kontrolliert in welchem Polygon sich die Adresse befindet
        #Rückgabewert True wenn sich der Punkt im gegebenen Polygon befindet
        var_polygon = Polygon(var_polygon)
        li_Polygons.append(var_polygon)
        return var_polygon.contains(point)

    #Dieser Loop findet heraus in welchen Polygon sich die Adresse befindet
    #Wenn die Adresse gefunden worden ist, ist found_ID nicht mehr "NONE"
    point = Point(coordinateAddress)
    li_Polygons = [] #Wir erstellen eine Liste an Polygons um diese später zu plotten
    str_ID = "NONE"
    for key, value in dic_Polygons.items():
        for coords in value:
        
            if len(value) > 1:
                for extra_coords in coords:
                    result = IsPointInsidePolygon(extra_coords, point)
                    if result == True:
             
                        str_ID = key
                        break
   
            else:
                result = IsPointInsidePolygon(coords, point)
            if result == True:
                str_ID = key
           
    if str_ID == "NONE":
        print("Adresse: ", str_address, " nicht gefunden")
    #Nun da das bestimmte Polygon bekannt ist werden die relevanten Daten extrahiert
    #Relevante Daten:
        #W/m/K in den Verschiedenen Tiefen (10m, 30m, 100m, 200m)
        #MW_WL_100: Gemittelte Wärmeleitfähigkeit des Bodens von 0-100m Tiefe
        #STABW_WL_3: Vielleicht statistische Abweichung für 100m Tiefe?
        #ANZWL_100: Keine Ahnung. Anzahl Wärmemessungen vielleicht?
    for features in data["features"]:
        if features["id"] == str_ID:
            dic_Properties = features["properties"]



    
    if 0 < flt_depthprobe <= 10:
        str_mode = "10M"
        str_mode_export = "10"
    if 10 < flt_depthprobe <= 30:
        str_mode = "30M"
        str_mode_export = "30"
    if 30 < flt_depthprobe <= 100:
        str_mode = "100"
        str_mode_export = "100"
    if 100 < flt_depthprobe <= 200:
        str_mode = "200"
        str_mode_export = "200"

    def DetermineColor(int_class):
        #Diese Funktion erhält einen Integer welcher die Klasse der Wärmeleitfähigkeit represäntiert
        #und gibt die dementsprechende Farbe in HEX zurück
        #Falls keine Klasse angegeben ist wird einfach grau zurückgegeben
        if int_class == 0:
            #Keine Messung vorhanden
            hex_color = "#aba9a9"
        elif int_class == 1:
            #Mäßig (<1.8 W/m/K)
            hex_color = "#ffb300"
        elif int_class == 2:
            #Durchschnittlich (1.8 – 1.99 W/m/K)
            hex_color = "#ff0000"
        elif int_class == 3:
            #Gut (>= 2 W/m/K)
            hex_color = "#590000"
        else:
            hex_color = "#aba9a9"
        return hex_color
    

    #Schnittstelle:
    #Export: Liste an Farben + Polygonen
    #Koordinaten der eingegebenen Adresse
    #Id des Erdwärmepolygons in dem sich unsere Adresse befindet
    li_color = []
    dic_export = {"Bohrtiefe" : flt_depthprobe, #Tiefe der Sonden
                  "adresse" : str_address,  #eingegebene Adresse                 
                  "color" : li_color, #Liste der Farben die die Polygone haben sollen
                  "coord_target" : coordinateAddress, #Koordinaten der eingegeben Adresse
                  "dic_target" : dic_Properties, #Eigenschaften der Bohrung von der Adresse (Wärmeleitfähigkeit etc.)
                  "MW_WL" : dic_Properties["MW_WL_" + str_mode_export],
                  "Layer" : "MW_WL_" + str_mode_export
                  }

    return dic_export


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import math

global id_counter
id_counter = 0
global connection_Counter
connection_Counter = 0

class Pixel():
    def __init__(self, cp, rho, t, m, U, fläche_Seite):
        global id_counter
        self.id = id_counter #Unique Number für jeden Pixel
        id_counter +=1
        self.cp = cp  #spez Wärmekapazität in kJ/kgK
        self.dichte = rho #Dichte des pixels in kg/m³
        self.masse = m #masse des Pixels in kg
        self.temperatur = t  #Anfangstemperatur in °C
        self.U = U
        self.fläche_Seite = fläche_Seite
        self.isErdsonde = False #Bool der anzeigt ob mein Pixel geupdated wurde
        self.x = -1 #Position mit -1 initialisiert für Errorchecking
        self.y = -1 #Position mit -1 initialisiert für Errorchecking
        self.li_connections = []

    def __lt__(self, other):
        return self.temperatur > other.temperatur

class Connection():
    def __init__(self,pxl_1, pxl_2) -> None:
        global connection_Counter
        self.id = connection_Counter
        connection_Counter += 1
        self.isCalculated = False
        self.Pixel_1 = pxl_1
        self.Pixel_2 = pxl_2



class BKA():
    def __init__(self, data_sim, data_pixel, data_erd):
        self.data_sim = data_sim
        self.data_pixel = data_pixel
        self.data_erd = data_erd

        self.pixel_x = data_sim["Punkte X"]
        self.pixel_y = data_sim["Punkte Y"]
        self.pixel_array = np.zeros([self.pixel_x+2,self.pixel_y+2], dtype=object)
        self.li_connections_ordered = []

        t_Boden = data_pixel["Temperatur"] #°C
        cp = data_pixel["cp"] #kJ/kgK
        rho = data_pixel["rho"] #kg/m³

        bohrtiefe = float(data_erd["Bohrtiefe"]) #m
        self.anz_Sonden = float(data_erd["Anzahl_Sonden"])
        self.abs_Sonden = float(data_erd["Abstand_Sonden"]) #m

        fläche = data_sim["Länge Punkt [m]"] * data_sim["Länge Punkt [m]"] #m²
        volumen = fläche * bohrtiefe #m³
        self.masse = volumen * rho #kg
        self.U = float(data_erd["WM_spez"]) /  data_sim["Länge Punkt [m]"] #W/m²K
        self.fläche_Seite = bohrtiefe * data_sim["Länge Punkt [m]"]
 
        #Außenrand hinzufügen
        for y in range(self.pixel_y+2):
            self.pixel_array[y][0] = (Pixel(cp,rho,t_Boden,self.masse,self.U,self.fläche_Seite)) 
            self.pixel_array[y][-1] = (Pixel(cp,rho,t_Boden,self.masse,self.U,self.fläche_Seite)) 
            
        for x in range(self.pixel_x+2):
            self.pixel_array[0][x] = (Pixel(cp,rho,t_Boden,self.masse,self.U,self.fläche_Seite)) 
            self.pixel_array[-1][x] = (Pixel(cp,rho,t_Boden,self.masse,self.U,self.fläche_Seite)) 

        #Erstellt Pixelobjekte
        for y in range(1,self.pixel_y+1):
            for x in range(1,self.pixel_x+1):
                self.pixel_array[y][x] = (Pixel(cp,rho,t_Boden,self.masse,self.U,self.fläche_Seite)) 



        #Erstellt Connections
        for y in range(1,self.pixel_y+1):
            for x in range(1,self.pixel_x+1):
                while len(self.pixel_array[y][x].li_connections) != 4:
                    pixel_1 = self.pixel_array[y][x]
                    pixel_North = self.pixel_array[y+1][x]
                    pixel_East = self.pixel_array[y][x+1]
                    pixel_South = self.pixel_array[y-1][x]
                    pixel_West = self.pixel_array[y][x-1]
                    li_pixels = [pixel_North,pixel_East,pixel_South,pixel_West]

                    for pixel in li_pixels:
                        if len(pixel_1.li_connections) == 0:
                            con = Connection(pixel_1,pixel)
                            self.li_connections_ordered.append(con)
                            pixel_1.li_connections.append(con)
                            pixel.li_connections.append(con)
                        else:
                            li_test = []
                            for cons in pixel_1.li_connections:
                                li_test.append(cons.Pixel_1)
                                li_test.append(cons.Pixel_2)
                            if not pixel in li_test:
                                con = Connection(pixel_1,pixel)
                                self.li_connections_ordered.append(con)
                                pixel_1.li_connections.append(con)
                                pixel.li_connections.append(con)
                                
        self.con_Counter = connection_Counter
        print(f"Anzahl an zu berechnenden Verbindungen: {self.con_Counter}")
        print(f"Anzahl an zu berechnenden Verbindungen: {len(self.li_connections_ordered)}")
                    
    def CreateSimulationOrder(self):
        self.li_connections = self.li_connections_ordered
        random.shuffle(self.li_connections)

    def PlaceSonden(self):
        l_Quadrat = math.ceil(math.sqrt(self.anz_Sonden))

        mPoint_base = self.data_sim["Punkte X"] // 2
        abs_sonde = float(self.data_erd["Abstand_Sonden"]) / 2 / self.data_sim["Länge Punkt [m]"] 

        sonden = self.anz_Sonden
        self.li_Coords = []
        x_beg = mPoint_base - l_Quadrat/2 * abs_sonde - abs_sonde/2
        x = x_beg
        y = mPoint_base - l_Quadrat/2 * abs_sonde - abs_sonde/2
        for row in range(l_Quadrat):
            y += abs_sonde
            x = x_beg
            if sonden == 0:
                    break
            for column in range(l_Quadrat):
                x += abs_sonde
                self.li_Coords.append([x,y])
                self.pixel_array[int(x)][int(y)].isErdsonde = True
                sonden -= 1
                if sonden == 0:
                    break

    def DumpEnergy(self,Q):
        Q = Q / self.anz_Sonden
        for coords in self.li_Coords:
            pixel = self.pixel_array[int(coords[0])][int(coords[1])]
            pixel.temperatur = (Q * 3600 / (pixel.masse * pixel.cp)) + pixel.temperatur


    def CalculateConnection(self,con):
        pixel_1 = con.Pixel_1
        pixel_2 = con.Pixel_2

        t1 = pixel_1.temperatur
        t2 = pixel_2.temperatur

        #Leistung zwischen Pixel
        Q = float(self.data_erd["WM_spez"]) * self.fläche_Seite * ((t1-t2)/self.data_sim["Länge Punkt [m]"])

        #Temperaturänderung
        dt = ((Q * 3600)/(self.masse * self.data_pixel["cp"]))

        t1_neu = t1 - dt
        t2_neu = dt + t2
        pixel_1.temperatur = t1_neu
        pixel_2.temperatur = t2_neu


    def Get_Attr_List(self, str_attr):
        #Get_Attr_List nimmt ein beliebiges Attribut von Pixel und gibt dieses für alle Pixel instanzen in Form eines arrays zurück
        li_first = []
        for first in self.pixel_array:
            li_second = []
            for second in first:
                li_second.append(getattr(second,str_attr))
            li_first.append(li_second)
        return np.array(li_first)

    def Flatten_2D_List(self, _2D_list):
        #Nimmt eine einfach genestete Liste und flacht diese aus
        return [item for sublist in _2D_list for item in sublist]

    def Create_2D_Array(self,flat_list):
        #Nimmt eine geflächte Liste und nestet diese wieder in ein 2D Array
        nested_list = []

        for i in range(0,self.pixel_y):
            nested_list.append(flat_list[i * self.pixel_x:i * self.pixel_x + self.pixel_x]) 
        array = np.array(nested_list, dtype = object)
        return array

    def Init_Sim(self):     
        #Initialize all pixels with coordinates
        for x, first in enumerate(self.pixel_array, start = 0):
            for y,second in enumerate(first, start = 0):
                second.x = x
                second.y = y

        #Shuffle Simulation Order of connections
        self.CreateSimulationOrder()
        #Sonden im Array platzieren
        self.PlaceSonden()
        print("Init_Sim DONE")
        
        

    def Simulate(self, Q_toDump):
        #Temperaturen der SondenPixel setzen
        self.DumpEnergy(Q_toDump) #Watt
        for con in self.li_connections:
            self.CalculateConnection(con)
                

#data_Erdwärme = {
#            "Adresse" : "",
#            "Bohrtiefe": 100,
#            "Anzahl_Sonden" : 9,
#            "Abstand_Sonden" : 10,
#            "WM_spez" : 2}

#data_Sim = {
#    "Punkte X" : 40,
#    "Punkte Y" : 30,
#    "Länge Punkt [m]" : 0.5,
#    "Länge Sonde [m]" : 0.2,
#    }

#data_Boden = {
#    "Temperatur" : 6,
 #   "Temperatur Einspeisung" : 11,
 #   "cp" : 1000,
#    "rho" : 2600}

#Dimension: 1 Punkt = 50cm
#Test = BKA(data_Sim, data_Boden, data_Erdwärme)
#Test.Simulate()

#sns.heatmap(Test.Get_Attr_List("temperatur"), square=True, cmap='viridis')
#plt.show()
