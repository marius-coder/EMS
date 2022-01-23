
import pandas as pd
import os
import csv
import numpy as np
import importlib
ImportSpeicher = importlib.import_module("EMS-Backend.Classes.Wärmespeicher")



class Wärmepumpe():

    def __init__(self, speicher, data_WP, geb_VL_HZG, geb_VL_KLG):
        self.Pel = data_WP["Stromverbrauch"]
        self.COP = data_WP["COP"]
        self.COP_betrieb = np.ones(8760) * data_WP["COP"]
        self.speicher = speicher
        self.WP_VL_HZG = data_WP["VL_HZG"]
        self.geb_VL_HZG = geb_VL_HZG
        self.WP_VL_KLG = data_WP["VL_KLG"]
        self.geb_VL_KLG = geb_VL_KLG
        self.Pel_Betrieb = np.zeros(8760)
        self.is_on = np.zeros(8760, dtype = bool)

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

    def Check_SpeicherHeizen(self, hour):
        """Diese Funktion kontrolliert zu jeder Stunde den dazugehörigen Speicher auf Temperatur
           Wenn die Temperatur außerhalb des Sollwertes liegt wird WP_TurnOn aufgerufen"""

        #Verlust und Ausgleichsvorgänge
        self.speicher.UpdateSpeicher(hour, self.WP_VL_HZG)

        schichttoCheck = int(self.speicher.anz_schichten / 2) #Wenn der Speicher halb durchgeladen ist wird abgedreht
        schichtEinschalten = int(self.speicher.anz_schichten * 4/5)
        print("Entnahmeschicht: ", self.speicher.li_schichten[-1]["Temperatur [°C]"], " °C")
        print("Kontrollschicht Einschalten: ", self.speicher.li_schichten[schichtEinschalten]["Temperatur [°C]"], " °C")
        print("Kontrollschicht Aussschalten: ", self.speicher.li_schichten[schichttoCheck]["Temperatur [°C]"], " °C")
                
        if self.speicher.li_schichten[schichttoCheck]["Temperatur [°C]"] > self.geb_VL_HZG:
            print("TurnOff1")
            self.is_on[hour] = False
            self.WP_TurnOff()
        elif self.speicher.li_schichten[schichtEinschalten]["Temperatur [°C]"] < self.geb_VL_HZG + 2: #+2°C damit die WP schon ein bisschen früher anfängt als dass Sie eigentlich gebraucht wird
            print("TurnOn")
            self.is_on[hour] = True
            self.WP_TurnOn(self.WP_VL_HZG, self.COP)
        else:
            print("TurnOff2")
            self.is_on[hour] = False
            self.WP_TurnOff()

    def Check_SpeicherKühlen(self, hour):
        """Diese Funktion kontrolliert zu jeder Stunde den dazugehörigen Speicher auf Temperatur
           Wenn die Temperatur außerhalb des Sollwertes liegt wird WP_TurnOn aufgerufen"""

        #Verlust und Ausgleichsvorgänge
        self.speicher.UpdateSpeicher(hour, self.WP_VL_KLG)

        schichttoCheck = int(self.speicher.anz_schichten / 2) #Wenn der Speicher halb durchgeladen ist wird abgedreht
        schichtEinschalten = int(self.speicher.anz_schichten * 4/5)
        print("Entnahmeschicht: ", self.speicher.li_schichten[-1]["Temperatur [°C]"], " °C")
        print("Kontrollschicht Einschalten: ", self.speicher.li_schichten[schichtEinschalten]["Temperatur [°C]"], " °C")
        print("Kontrollschicht Aussschalten: ", self.speicher.li_schichten[schichttoCheck]["Temperatur [°C]"], " °C")
                
        if self.speicher.li_schichten[schichttoCheck]["Temperatur [°C]"] < self.geb_VL_KLG:
            print("TurnOff1")
            self.is_on[hour] = False
            self.WP_TurnOff()
        elif self.speicher.li_schichten[schichtEinschalten]["Temperatur [°C]"] > self.geb_VL_KLG-1:
            print("TurnOn")
            self.is_on[hour] = True
            self.WP_TurnOn(self.WP_VL_KLG, self.COP-1)
        else:
            print("TurnOff2")
            self.is_on[hour] = False
            self.WP_TurnOff()
        
    def WP_TurnOn(self, t_VL, COP):
        #TODO: Logik um COP und Pel dynamisch zu berechnen
        #Get Tl temp
        temp_RL = self.speicher.li_schichten[0]["Temperatur [°C]"]
        Q_toLoad = self.Pel * COP * 1000
        m_toLoad = Q_toLoad / (4180 * abs(t_VL - temp_RL)) * 3600               
        self.speicher.Speicher_Laden(m_toLoad, VL = t_VL)
        
    def WP_TurnOff(self):
        pass


#Speicher = ImportSpeicher.Wärmespeicher(dicke_dämmung = 0.1, lambda_dämmung = 0.04,VL = 6, RL = 10, schichten = 10, ladezone = 5, height = 2, diameter = 0.5)
#WP = Wärmepumpe(0.5,3,Speicher,WP_VL_HZG = 35, geb_VL_HZG = 30, WP_VL_KLG = 6, geb_VL_KLG = 8)


#for i in range(20):
#    WP.Check_SpeicherKühlen()
#    WP.speicher.Speicher_Entladen(500,12)