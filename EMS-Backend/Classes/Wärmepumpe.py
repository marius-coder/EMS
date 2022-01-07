
import pandas as pd
import os
import csv
import numpy as np
import importlib
ImportSpeicher = importlib.import_module("EMS-Backend.Classes.Wärmespeicher")



class Wärmepumpe():

    def __init__(self, Pel, COP, speicher, WP_VL_HZG, geb_VL_HZG, WP_VL_KLG, geb_VL_KLG):
        self.Pel = Pel
        self.COP = COP
        self.speicher = speicher
        self.WP_VL_HZG = WP_VL_HZG
        self.geb_VL_HZG = geb_VL_HZG
        self.WP_VL_KLG = WP_VL_KLG
        self.geb_VL_KLG = geb_VL_KLG
        self.Pel_Betrieb = np.zeros(8760)



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
        self.flt_strombedarf = strombedarf
        self.COP = COP
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
           Wenn alles passt wird eine neue Zeile zur csv hinzugefügt"""

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
            with open("./data/Wärmepumpen.csv",'a',newline= "") as fd:
                fd.write(str_newRow)
            return True
        else:
            #Spaltenanzahl stimmt nicht überein
            print("Spaltenanzahl stimmt nicht überein")
    
    #--------------------------------------------------------------------------------------------------------------------------------------

    def calc_COP_csv(self, path:str, t_Q: int, t_VL:int):
        df = pd.read_csv(path, delimiter=";")
            
        a = np.zeros(len(df))                                                  #erstellt ein array mit allen Quelltemperaturen
        for i in range(0, len(df), 1):
            a[i] = df.iloc[i,1]
        
        boolian = t_Q in a
        if boolian == True:
            df_1 = df.loc[df["t_VL"] == t_VL]                                  #erstellt df nur mit gewünschtem VL
            df_2 = df_1.loc[df_1["t_Q"] == t_Q]                                #erstellt df nur mit gewünschtem VL und Quelltemperatur
            self.COP_t = df_2.iloc[0,10]
            
        else:
            x2 = a[(np.abs(a-t_Q)).argmin()]                                   #Wenn t_Q nicht in array a, dann x2 = nächster Wert

            df_1 = df.loc[df["t_VL"] == t_VL]                                  #erstellt df nur mit gewünschtem VL
            df_2 = df_1.loc[df_1["t_Q"] == x2]                                 #erstellt df nur mit gewünschtem VL und Quelltemperatur
            y2 = df_2.iloc[0,10]

            b = df_2.iloc[:,10].index                                          #b = Index von y2  
            y1 = float(df_1.iloc[b-1,10])           
            x1 = float(df_1.iloc[b-1,1])
            x = t_Q
            k = (y2-y1)/(x2-x1)
    
            self.COP_t = y1 + k*(x-x1)                                         #berechnet COP bei Quelltemperatur (linear interpoliert)
        return self.COP_t
    
    #--------------------------------------------------------------------------------------------------------------------------------------

    def calc_COP_GUI(self, path:str, t_Q: int, t_VL:int):
        pass

    def Check_SpeicherHeizen(self):
        """Diese Funktion kontrolliert zu jeder Stunde den dazugehörigen Speicher auf Temperatur
           Wenn die Temperatur außerhalb des Sollwertes liegt wird WP_TurnOn aufgerufen"""

        #Verlust und Ausgleichsvorgänge
        self.speicher.UpdateSpeicher()

        schichttoCheck = int(self.speicher.anz_schichten / 2) #Wenn der Speicher halb durchgeladen ist wird abgedreht
        print("Kontrollschicht Vorletzte: ", self.speicher.li_schichten[-2]["Temperatur [°C]"])
        print("Kontrollschicht 5: ", self.speicher.li_schichten[schichttoCheck]["Temperatur [°C]"])
                
        if self.speicher.li_schichten[schichttoCheck]["Temperatur [°C]"] > self.geb_VL_HZG:
            print("TurnOff1")
            self.WP_TurnOff()
        elif self.speicher.li_schichten[-2]["Temperatur [°C]"] < self.geb_VL_HZG:
            print("TurnOn")
            self.WP_TurnOn(self.WP_VL_HZG, self.COP)
        else:
            print("TurnOff2")
            self.WP_TurnOff()

    def Check_SpeicherKühlen(self):
        """Diese Funktion kontrolliert zu jeder Stunde den dazugehörigen Speicher auf Temperatur
           Wenn die Temperatur außerhalb des Sollwertes liegt wird WP_TurnOn aufgerufen"""

        #Verlust und Ausgleichsvorgänge
        self.speicher.UpdateSpeicher()

        schichttoCheck = int(self.speicher.anz_schichten / 2) #Wenn der Speicher halb durchgeladen ist wird abgedreht
        #print("Kontrollschicht Vorletzte: ", self.speicher.li_schichten[-2]["Temperatur [°C]"])
        #print("Kontrollschicht 5: ", self.speicher.li_schichten[schichttoCheck]["Temperatur [°C]"])
                
        if self.speicher.li_schichten[schichttoCheck]["Temperatur [°C]"] < self.geb_VL_KLG:
            #print("TurnOff1")
            self.WP_TurnOff()
        elif self.speicher.li_schichten[-2]["Temperatur [°C]"] > self.geb_VL_KLG:
            #print("TurnOn")
            self.WP_TurnOn(self.WP_VL_KLG, self.COP-1)
        else:
            #print("TurnOff2")
            self.WP_TurnOff()
        
    def WP_TurnOn(self, t_VL, COP):
        #TODO: Logik um COP und Pel dynamisch zu berechnen
        QtoLoad = self.Pel * COP * 1000
        self.speicher.Speicher_Laden(QtoLoad, VL = t_VL)
        
    def WP_TurnOff(self):
        pass
#Speicher = ImportSpeicher.Wärmespeicher(dicke_dämmung = 0.1, lambda_dämmung = 0.04,VL = 6, RL = 14, schichten = 10, ladezone = 5, height = 2, diameter = 0.5)
#WP = Wärmepumpe(0.5,3,Speicher,WP_VL_HZG = 35, geb_VL_HZG = 30, WP_VL_KLG = 6, geb_VL_KLG = 8)
