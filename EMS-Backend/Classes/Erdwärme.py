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

class Sondenfeld():
    def __init__(self, data) -> None:
        self.bohrtiefe = data["Bohrtiefe"]
        self.anz_Sonden = data["Anzahl_Sonden"]
        self.abs_Sonden = data["Abstand_Sonden"]
        self.WM_spez = data["WM_spez"]


        

    def DumpEnergy(self, q_toDump):
        pass
