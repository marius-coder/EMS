

import urllib.request, json , urllib.parse
import requests
import urllib.parse
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt

def Get_GeothermalData(str_address, flt_depthprobe):
    #Get Erdw�rmedaten f�r Wien
    with urllib.request.urlopen("https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:ERDWSONDOGD") as url:
        data = json.loads(url.read().decode())
    #Die Potenzialkarten f�r Erdw�rmesonden zeigen kein eigentliches Potenzial in Form einer Energiemenge pro Fl�chen- oder Zeiteinheit,
    #sondern die konduktive W�rmeleitf�higkeit, gemittelt �ber drei Tiefenbereiche (0 bis 30, 0 bis 100 und 0 bis 200 Meter) in der Einheit W/m/K. 
    #Dieser Parameter ist von den geologischen und hydrogeologischen Gegebenheiten abh�ngig und dient als Basis f�r die Berechnung der nutzbaren Energiemenge. 
    #Um diese vollst�ndig berechnen zu k�nnen, ist die mittlere Bodentemperatur und die Betriebsweise der Erdsondenanlage (Heizen/K�hlen, Volllaststunden) notwendig.

    #Die mittlere Bodentemperatur zur Dimensionierung von Erdw�rmesonden kann f�r das Bundesland Wien folgenderma�en abgesch�tzt werden:
    #Tiefenintervall 0 bis 30 Meter: 12 +/- 2 �C
    #Tiefenintervall 0 bis 100 Meter: 12 +/- 1 �C
    #Tiefenintervall 0 bis 200 Meter: 14 +/- 1 �C
    #Quelle: https://www.wien.gv.at/stadtentwicklung/energie/themenstadtplan/erdwaerme/erlaeuterungen.html


    #Die relevanten Daten werden extrahiert und in dic_Polygons abgelegt
    #Relevante Daten:sdfsdf
        #Koordinaten welche das Polygon bestimmen
    dic_Polygons = {}



    li_lengths = []
    li_lengths_feature = []
    for feature in data["features"]:
        li_coordinates = []
    
        #Liest die L�ngen der einzelnen Features aus
        #Manche Features haben vernestete Koordinaten die in einem Loop ausgelesen werden m�ssen
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
    #Dieser Loop berechnet nun die richtige l�nge der einzelnen Features 
    for it,item in enumerate(li_lengths_feature, start = 1):
        it_ceiling = sum(li_lengths_feature[0:it])
        item = sum(li_lengths[it_floor:it_ceiling])
        it_floor = sum(li_lengths_feature[0:it])
        li_lengths_new.append(item)

    #Funktion von Simon um eine Adresse in Koordinaten zu wandeln
    def from_address(address_string="Stephansplatz, Wien, �sterreich"):
        parsed_address = urllib.parse.quote(address_string)
        url = 'https://nominatim.openstreetmap.org/search/' + parsed_address +'?format=json'
        response = requests.get(url).json()
        location = (float(response[0]["lon"]), float(response[0]["lat"]) )
        return location
    
    coordinateAddress = from_address(str_address)

    def IsPointInsidePolygon(var_polygon, point):
        #Diese Funktion kontrolliert in welchem Polygon sich die Adresse befindet
        #R�ckgabewert True wenn sich der Punkt im gegebenen Polygon befindet
        var_polygon = Polygon(var_polygon)
        li_Polygons.append(var_polygon)
        return var_polygon.contains(point)

    #Dieser Loop findet heraus in welchen Polygon sich die Adresse befindet
    #Wenn die Adresse gefunden worden ist, ist found_ID nicht mehr "NONE"
    point = Point(coordinateAddress)
    li_Polygons = [] #Wir erstellen eine Liste an Polygons um diese sp�ter zu plotten
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
           

    #Nun da das bestimmte Polygon bekannt ist werden die relevanten Daten extrahiert
    #Relevante Daten:
        #W/m/K in den Verschiedenen Tiefen (10m, 30m, 100m, 200m)
        #MW_WL_100: Gemittelte W�rmeleitf�higkeit des Bodens von 0-100m Tiefe
        #STABW_WL_3: Vielleicht statistische Abweichung f�r 100m Tiefe?
        #ANZWL_100: Keine Ahnung. Anzahl W�rmemessungen vielleicht?
    for features in data["features"]:
        if features["id"] == str_ID:
            dic_Properties = features["properties"]



    
    if 0 < flt_depthprobe <= 10:
        str_mode = "10M"
    if 10 < flt_depthprobe <= 30:
        str_mode = "30M"
    if 30 < flt_depthprobe <= 100:
        str_mode = "100"
    if 100 < flt_depthprobe <= 200:
        str_mode = "200"

    def DetermineColor(int_class):
        #Diese Funktion erh�lt einen Integer welcher die Klasse der W�rmeleitf�higkeit repres�ntiert
        #und gibt die dementsprechende Farbe in HEX zur�ck
        #Falls keine Klasse angegeben ist wird einfach grau zur�ckgegeben
        if int_class == 0:
            #Keine Messung vorhanden
            hex_color = "#aba9a9"
        elif int_class == 1:
            #M��ig (<1.8 W/m/K)
            hex_color = "#ffb300"
        elif int_class == 2:
            #Durchschnittlich (1.8 � 1.99 W/m/K)
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
    #Id des Erdw�rmepolygons in dem sich unsere Adresse befindet
    li_color = []
    dic_export = {"depthprobe" : flt_depthprobe, #Tiefe der Sonden
                  "adresse" : str_address,  #eingegebene Adresse
                  "Polygone" : li_Polygons, #Liste an Polygonen zum zeichnen
                  "color" : li_color, #Liste der Farben die die Polygone haben sollen
                  "coord_target" : coordinateAddress, #Koordinaten der eingegeben Adresse
                  "dic_target" : dic_Properties, #Eigenschaften der Bohrung von der Adresse (W�rmeleitf�higkeit etc.)
                  }

    if str_ID == "NONE":
        print("No Area found with this address")
    else:
        fig, axs = plt.subplots()
        axs.set_aspect('equal', 'datalim')

        li_class = []
        it_poly = 0
        for int_lenghts in li_lengths_new:
        
            for len in range(int_lenghts):
                li_class.append(data["features"][it_poly]["properties"]["KLASSE_" + str_mode])
            it_poly += 1

        for it,polygon in enumerate(li_Polygons):  
        
            color = DetermineColor(li_class[it])
            dic_export["color"].append(color)


            xs, ys = polygon.exterior.xy    
            axs.fill(xs, ys, alpha=0.5, fc= color , ec='none')

        x = coordinateAddress[0]
        y = coordinateAddress[1]
        axs.plot(x, y, marker="o", markersize=5, markeredgecolor="white", markerfacecolor="green")

        plt.show()

    return dic_export




flt_depthprobe = 35
address = "H�chst�dtplatz 6, 1200 Wien, �sterreich"

Get_GeothermalData(str_address = address, flt_depthprobe = flt_depthprobe)