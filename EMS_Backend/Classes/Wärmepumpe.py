
import Stoffdaten


class Wärmepumpe():

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
                   trinkwassererwärmung = False, #WP mit Trinkwassererwärmung?
                   heizstableistung = 0, #Wenn ja, wie viel kW hat die Nachheizung dafür
                   triwasserspeicher = 0, #Wenn ja, wie groß ist der Trinkwasserspeicher (ohne Schichtung)
                   COP_m15 = -1, COP_m7 = -1, COP_2 = -1, COP_7 = -1, COP_12 = -1, #Werte für COP bei verschiedenen Außentemperaturen
                   ):
        #Diese Fkt soll nachdem der User eine neue WP eingegeben hat, die WP als csv abspeichern
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

        self.str_energiequelle = energiequelle
        self.str_energiesenke = energiesenke
        self.dic_maße = { "Länge" : länge,
                       "Breite" : breite,
                       "Höhe"   : höhe}
        self.b_trinkwassererwärmung = trinkwassererwärmung
        self.flt_heizstableistung = heizstableistung
        self.flt_triwasserspeicher = triwasserspeicher
        self.dic_COP = { "-15°C" : COP_m15,
                        "-7°C" : COP_m7,
                        "2°C" : COP_2,
                        "7°C" : COP_7,
                        "12°C" : COP_12,}

    def __init__(self):
        pass

    def Calc_COP(self):
        pass

    def Calc_Wärmeübergang(self):
        pass

    def Calc_Temperatur(self):
        pass



