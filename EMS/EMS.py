

import pandas as pd
import numpy as np
np.set_printoptions(threshold=np.inf)
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

        bohrtiefe = data_erd["Bohrtiefe"] #m
        self.anz_Sonden = data_erd["Anzahl_Sonden"]
        self.abs_Sonden = data_erd["Abstand_Sonden"] #m

        fläche = data_sim["Länge Punkt [m]"] * data_sim["Länge Punkt [m]"] #m²
        volumen = fläche * bohrtiefe #m³
        self.masse = volumen * rho #kg
        self.U = data_erd["WM_spez"] /  data_sim["Länge Punkt [m]"] #W/m²K
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
        #self.SimOrder_Ordered = np.linspace(0,self.con_Counter)
        #self.SimOrder = np.linspace(0,self.con_Counter)
        self.li_connections = self.li_connections_ordered
        random.shuffle(self.li_connections)

    def PlaceSonden(self):
        l_Quadrat = math.ceil(math.sqrt(self.anz_Sonden))

        mPoint_base = self.data_sim["Punkte X"] // 2
        abs_sonde = self.data_erd["Abstand_Sonden"] / 2 / self.data_sim["Länge Punkt [m]"] 

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

    def SetSondenTemperatur(self,Q):
        for coords in self.li_Coords:
            pixel = self.pixel_array[int(coords[0])][int(coords[1])]
            pixel.temperatur = (Q / (pixel.masse * pixel.cp)) + pixel.temperatur

    def CalculateConnection(self,con):
        pixel_1 = con.Pixel_1
        pixel_2 = con.Pixel_2

        t_misch = (pixel_1.temperatur * pixel_1.masse + pixel_2.temperatur * pixel_2.masse) / (pixel_1.masse + pixel_2.masse)
        
        pixel_1.temperatur = t_misch
        pixel_2.temperatur = t_misch

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
        
        

    def Simulate(self):

        #1. Initialisiere Simulation
        self.Init_Sim()
        for hour in range(8760):
            print(f"Stunde: {hour}")
            #Temperaturen der SondenPixel setzen
            self.SetSondenTemperatur(1000000)
            for con in self.li_connections:
                self.CalculateConnection(con)
                

data_Erdwärme = {
            "Adresse" : "",
            "Bohrtiefe": 100,
            "Anzahl_Sonden" : 9,
            "Abstand_Sonden" : 10,
            "WM_spez" : 2}

data_Sim = {
    "Punkte X" : 20,
    "Punkte Y" : 20,
    "Länge Punkt [m]" : 0.5,
    "Länge Sonde [m]" : 0.2,
    }

data_Boden = {
    "Temperatur" : 6,
    "Temperatur Einspeisung" : 11,
    "cp" : 1000,
    "rho" : 2600}

#Dimension: 1 = 50cm
Test = BKA(data_Sim, data_Boden, data_Erdwärme)
Test.Simulate()
print(Test.Get_Attr_List("x"))
print(Test.Get_Attr_List("y"))
print(Test.Get_Attr_List("temperatur"))
print("")