
import Stoffdaten


class Wärmepumpe():

    self.temp_KW_VL = None
    self.temp_KW_RL = None #Bekannt
    self.temp_KÜ_VL = None #Bekannt
    self.temp_KÜ_RL = None
    self.COP = None
    self.Q_wärme = None
    self.strom = None #Bekannt


    def DefineNewWP():
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

        self





    def __init__(self):
        pass

    def Calc_COP(self):
        pass

    def Calc_Wärmeübergang(self):
        pass

    def Calc_Temperatur(self):
        pass



