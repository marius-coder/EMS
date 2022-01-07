# -*- coding: utf-8 -*-

import importlib
ImportPV = importlib.import_module("EMS-Backend.Classes.PV-Anlage")
ImportBat = importlib.import_module("EMS-Backend.Classes.Batteriespeicher")
import numpy as np


class Stromnetz():
    def __init__(self, inputdata):

        if inputdata["Leistung [kW]"] == "None":
            inputdata["Leistung [kW]"] = float(inputdata["Leistung [%]"]) / 100 * float(inputdata["Bat_kWh"])

        self.Batterie = ImportBat.cla_Batterie(var_EntTiefe = inputdata["PV_kWp"],
                                               var_Effizienz = inputdata["Effizienz"], 
                                               var_kapMAX = inputdata["Bat_kWh"], 
                                               var_LadeEntladeLeistung = inputdata["Leistung [kW]"], 
                                               var_SelbstEntladung = inputdata["Selbstentladung"])
        self.PV_Anlage = ImportPV.cla_PV_Anlage(var_PV_kWp = inputdata["PV_kWp"],
                                                var_PV_EK = np.genfromtxt("./EMS-Backend/Data/PV_1kWp.csv"))
        self.Batterieladung = np.zeros(8760)
        self.Batterieeinspeisung = np.zeros(8760)
        self.Batterieentladung = np.zeros(8760)
        self.Netzeinspeisung = np.zeros(8760)
        self.Netzbezug = np.zeros(8760)



        

    def CheckResLast(self, hour, var_ResLast):
        var_ResLast = var_ResLast / 1000 #Reslast in kW Umwandeln
        if var_ResLast > 0: 
            #Einspeisefall
            var_ResLast = self.Batterie.Laden(var_ResLast)
            self.Batterieeinspeisung[hour] = self.Batterie.Leistung
            #Restverwertung via Netz + Tracking
            self.Netzeinspeisung[hour] = var_ResLast

        elif var_ResLast < 0:
            #Entladefall
            var_ResLast = abs(var_ResLast) #Die späteren Funktionen gehen immer von einer Positiven Zahl aus.
            var_ResLast = self.Batterie.Entladen(var_ResLast)
            self.Batterieentladung[hour] = self.Batterie.Leistung + self.Batterie.Verlust
            #Restverwertung via Netz + Tracking
            self.Netzbezug[hour] = var_ResLast

        self.Batterie.StehVerluste()
        self.Batterieladung[hour] = self.Batterie.Kapazität


    def CalcResLast(self, hour, Strombedarf):
        return (self.PV_Anlage.PV_EK[hour] * 1000) - Strombedarf

#Netz = Stromnetz()


#for hour in range(8760):
#    reslast = Netz.CalcResLast(hour,1)
#    Netz.CheckResLast(hour,reslast)

#    if hour == 100:
#        print("")