

import pandas as pd
import numpy as np

global id_counter
id_counter = 0
global connection_Counter
connection_Counter = 0

class Pixel():
    def __init__(self, c, rho, m, t = 20,):
        global id_counter
        self.id = id_counter #Unique Number für jeden Pixel
        id_counter +=1
        self.spez_Wärmekap = c  #spez Wärmekapazität in kJ/kgK
        self.dichte = rho #Dichte des pixels in kg/m³
        self.masse = m #masse des Pixels in kg
        self.temperatur = t  #Anfangstemperatur in °C
        self.Update = 0 #Bool der anzeigt ob mein Pixel geupdated wurde
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
        #self.Pixel_2 = pxl_2



class BKA():
    def __init__(self, pixel_x, pixel_y):
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        self.pixel_array = np.zeros([pixel_y,pixel_x], dtype=object)

        #Erstellt Pixelobjekte
        for y in range(pixel_y):
            for x in range(pixel_x):
                self.pixel_array[y][x] = (Pixel(4.18,1000,1,20)) 

        #Außenrand hinzufügen


        #Erstellt Connections
        for y in range(pixel_y):
            for x in range(pixel_x):
                while len(self.pixel_array[y][x].li_connections) != 4:



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




    def Init_Sim(self, init_temp):
        self.array[int(self.pixel_y/2)][int(self.pixel_x/2)].temperatur = init_temp

        #Initialize all pixels with coordinates
        for x, first in enumerate(self.array, start = 0):
            for y,second in enumerate(first, start = 0):
                second.x = x
                second.y = y


        

    def Simulate(self,init_temp):

        #1. Initialisiere Simulation
        self.Init_Sim(init_temp)
        





Test = BKA(5,3)
Test.Simulate(500)
print(Test.Get_Attr_List("x"))
print(Test.Get_Attr_List("y"))
print(Test.Get_Attr_List("temperatur"))
print("")