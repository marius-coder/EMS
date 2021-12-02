
import Classes.Stoffdaten
import pandas as pd
import os
import csv
from Classes.Helper import Helper
obj_helper = Helper()

cwd = os.getcwd()  # Get the current working directory (cwd)
print("Working DIR: ", cwd)


class Wärmepumpe():

    def __init__(self):
    
        self.temp_KW_VL = None
        self.temp_KW_RL = None #Bekannt
        self.temp_KÜ_VL = None #Bekannt
        self.temp_KÜ_RL = None
        self.COP = None
        self.Q_wärme = None
        self.strom = None #Bekannt


    def DefineNewWP(self,
                    hersteller, #Name des Herstellers
                    ModellNr,      #Modellnummer der Wärmepumpe
                    energiequelle, #Außenenergiequelle
                    energiesenke,   #Abgabemedium
                   länge,breite,höhe, #Maße der WP in cm
                   strombedarf, #Welchen maximalen Strombedarf hat die WP
                   bivalenztemp, #Welche Bivalenztemperatur hat die WP
                   schallpegel, #Welchen genormten Schallpegel hat die WP
                   trinkwassererwärmung = False, #WP mit Trinkwassererwärmung?
                   heizstableistung = 0, #Wenn ja, wie viel kW hat die Nachheizung dafür
                   triwasserspeicher = 0, #Wenn ja, wie groß ist der Trinkwasserspeicher (ohne Schichtung)
                   COP_m15 = -1, COP_m7 = -1, COP_2 = -1, COP_7 = -1, COP_12 = -1, #Werte für COP bei verschiedenen Außentemperaturen
                   ):
        #Diese Fkt soll nachdem der User eine neue Wärmepumpe eingegeben hat, die WP als csv abspeichern
        #Diese Fkt prüft auch alle Eingabewerte auf Plausibilität (eg Ob die Eingabe eine positive Zahl ist)
        #Verschiedene Eingabeoptionen sind
        #Energiequelle: Luft, Wasser, Sohle
        #Rückkühlmedium: Luft, Wasser, Sohle
        #Maße: L,B,H in cm
        #Inhalt in Liter
        #Mit Trinkwassererwärmung?: Ja oder Nein
        #Wenn ja, Zusatzheizung hat wie viel kW?
        #Leistung: in kW
        #Schallleistungspegel
        #Nennstromverbauch
        #COP
        #Je nach Energiequelle die Verschiedenen Normzustände eingeben
        #zB B = Brine(Sohle) , W = Water, E = Erdreich, A = Air

        #Spätere Funktion die die Buttons ausliest rückgabe: Dictionary
        #
        self.str_hersteller = hersteller
        self.str_modellNr = ModellNr
        self.str_energiequelle = energiequelle
        self.str_energiesenke = energiesenke
        self.flt_länge = länge
        self.flt_breite = breite
        self.flt_höhe = höhe
        self.flt_strombedarf = strombedarf
        self.flt_bivalenztemp = bivalenztemp
        self.flt_schallpegel = schallpegel
        self.b_trinkwassererwärmung = trinkwassererwärmung
        self.flt_heizstableistung = heizstableistung
        self.flt_triwasserspeicher = triwasserspeicher
        self.dic_COP_m15 = COP_m15
        self.dic_COP_m7 = COP_m7
        self.dic_COP_2 = COP_2
        self.dic_COP_7 = COP_7
        self.dic_COP_12 = COP_12
        
        

        str_newRow = ""
        for attr,val in self.__dict__.items():
            str_newRow = str_newRow + str(getattr(self, attr)) + ";"
        str_newRow = str_newRow[:-1]    #Delete last ";"
        str_newRow = str_newRow + "\r\n" #Add newline and reset
        self.checksum = obj_helper.Create_Checksum(str_newRow) #Create Checksum for current object
        str_newRow = self.checksum + ";" + str_newRow #Insert Checksum into our new row
        self.AppendCSV(str_newRow) #Call Function that handles appending the new row
        

    def AppendCSV(self,str_newRow):
        """Diese Funktion kontrolliert ob die neue Zeile alle Spalten ausfüllt
           Sie kontrolliert ob die Spaltenanzahl der newRow zu der Spaltenanzahl im csv passt
           Wenn alles passt wir eine neue Zeile zur csv hinzugefügt"""

        #Zuerst wird kontrolliert wie viele Spalten die csv hat
        with open('./data/Wärmepumpen.csv', newline='') as f:
            csv_reader = csv.reader(f)
            csv_headings = str(next(csv_reader))

        #Check if String is empty
        if str_newRow == "":
            print("str_newRow is empty")
            return False

        #Kontrolle ob diese Wärmepumpe schon existiert
        if obj_helper.Check_Checksums(self.checksum,'./data/Wärmepumpen.csv') == True:
            print("Objekt existiert bereits")
            return False

        #Kontrolle ob die Spaltenanzahl übereinstimmt
        if len(csv_headings.split(";")) == len(str_newRow.split(";")):
            print("Writing CSV")
            with open("./data/Wärmepumpen.csv",'a') as fd:
                fd.write(str_newRow)
            return True
        else:
            #Spaltenanzahl stimmt nicht überein
            print("Spaltenanzahl stimmt nicht überein")


WP = Wärmepumpe()

WP.DefineNewWP("Stiebel","01-6959_25A","Luft","Wasser",10,20,30,1,-7,50,True,22,78,1,2,3,4,5)