
import pandas as pd
import os
import csv
import numpy as np
import importlib
ImportSpeicher = importlib.import_module("EMS-Backend.Classes.Wärmespeicher")



class Wärmepumpe():

    def __init__(self, speicher, data_WP, geb_VL_HZG, geb_VL_KLG):
        self.Pel = data_WP["Stromverbrauch"]
        self.COP_betrieb = np.ones(8760) 
        self.speicher = speicher
        self.WP_VL_HZG = data_WP["VL_HZG"]
        self.geb_VL_HZG = geb_VL_HZG
        self.WP_VL_KLG = data_WP["VL_KLG"]
        self.geb_VL_KLG = geb_VL_KLG
        self.Pel_Betrieb = np.zeros(8760)
        self.is_on = np.zeros(8760, dtype = bool)
        self.SetupCOP(data_WP["Table"])

    def SetupCOP(self,dataString):
        dataString = dataString.split("----")[:-1]

        data_x = []
        data_y = []

        dataString = [dataString[i:i + 2] for i in range(0, len(dataString), 2)] 
        for i in range(0,len(dataString)//2+2,2):
            data_x.append(dataString[i])
            data_y.append(dataString[i+1])

        self.li_range_X = []
        self.li_k = []
        self.li_d = []

        for i in range(len(data_x)):
            k = (float(data_y[i][1])- float(data_y[i][0])) / (float(data_x[i][1])- float(data_x[i][0]))
            d = float(data_y[i][0]) - float(data_x[i][0]) * k

            self.li_k.append(k)
            self.li_d.append(d)
            self.li_range_X.append([float(data_x[i][0]),float(data_x[i][1])])

    def GetCOP(self,t_a):
        COP = 0
        for i in range(len(self.li_range_X)):
            if self.li_range_X[i][0] <= t_a <= self.li_range_X[i][1]:
                COP = t_a * self.li_k[i] + self.li_d[i]
                break

        #Falls die Außentemperatur vom Bereich abweicht wird der nächstbeste Wert genommen
        if COP == 0 and t_a>0:
            COP = t_a * self.li_k[-1] + self.li_d[-1]
        elif COP == 0 and t_a<0:
            COP = t_a * self.li_k[0] + self.li_d[0]
        return COP

    #--------------------------------------------------------------------------------------------------------------------------------------

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
            self.WP_TurnOn(self.WP_VL_HZG, self.COP_betrieb[hour])
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
            self.WP_TurnOn(self.WP_VL_KLG, self.COP_betrieb[hour]-1)
        else:
            print("TurnOff2")
            self.is_on[hour] = False
            self.WP_TurnOff()
        
    def WP_TurnOn(self, t_VL, COP):
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