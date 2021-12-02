
import Stoffdaten
import pandas as pd
import os 

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


    def DefineNewWP(energiequelle, #Außenenergiequelle
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

        self.str_energiequelle = energiequelle
        self.str_energiesenke = energiesenke
        self.länge
        self.breite
        self.höhe
        self.b_trinkwassererwärmung = trinkwassererwärmung
        self.flt_heizstableistung = heizstableistung
        self.flt_triwasserspeicher = triwasserspeicher
        self.dic_COP_m15 = COP_m15
        self.dic_COP_m7 = COP_m7
        self.dic_COP_2 = COP_2
        self.dic_COP_7 = COP_7
        self.dic_COP_12 = COP_12
        

        for attr,val in self.__dict__.items():
            print(attr)
            #Test this function
        #df_WP = pd.read_csv("./data/Wärmepumpen.csv", sep = ";")

  

        #with open('document.csv','a') as fd:
         #   fd.write(myCsvRow)

    def __init__(self):
        pass

    def Calc_COP(self):
        pass

    def Calc_Wärmeübergang(self):
        pass

    def Calc_Temperatur(self):
        pass



