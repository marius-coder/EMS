
  
class cla_Batterie():
    
    def __init__(self, var_EntTiefe, var_Effizienz, var_kapMAX, var_LadeEntladeLeistung = 0, var_SelbstEntladung = 0):
        self.Entladetiefe = var_kapMAX * var_EntTiefe / 100  #%
        self.Effizienz = var_Effizienz # Einheit %/100
        self.Kapazit�t = 0 #kWh
        self.Kapazit�t_MAX = var_kapMAX #kWh
        self.Leistung = var_LadeEntladeLeistung #kW
        self.Leistung_MAX = var_kapMAX * 0.5 #kW
        self.Verlust = 0 #kW
        self.Selbstentladung = var_SelbstEntladung / 8760 #in %/Stunde

    def StehVerluste(self):
        self.Kapazit�t = self.Kapazit�t - self.Kapazit�t * self.Selbstentladung
        self.Verlust += self.Kapazit�t * self.Selbstentladung

    def Entladen(self,arg_Reslast):
        #self.Leistung ist der Teil der anschlie�end von der Reslast abgezogen wird
        

        if arg_Reslast > self.Leistung_MAX:
            #Wenn ja wird gekappt
            self.Verlust = self.Leistung_MAX * (1-self.Effizienz)
            self.Leistung = self.Leistung_MAX * self.Effizienz 
        else:
            #Wenn nein, g2g
            self.Verlust = arg_Reslast * (1-self.Effizienz) 
            self.Leistung = arg_Reslast 

        #Kontrolle der Leistung
        if self.Leistung + self.Verlust > self.Kapazit�t:
            #Wenn nicht gen�gend Kapazit�t vorhanden ist wird die Leistung gekappt
            self.Verlust = self.Kapazit�t * (1-self.Effizienz)
            self.Leistung = self.Kapazit�t - self.Verlust
            
        #Ausf�hren des Entladevorgangs
        self.Kapazit�t -= self.Leistung + self.Verlust
        arg_Reslast -= self.Leistung 

        return arg_Reslast
    
    def Laden(self,arg_Reslast):

        if arg_Reslast > self.Leistung_MAX:
            #Wenn ja wird gekappt
            self.Verlust = self.Leistung_MAX * (1-self.Effizienz)
            self.Leistung = self.Leistung_MAX * self.Effizienz 
            
        else:
            #Wenn nein, g2g
            self.Verlust = arg_Reslast * (1-self.Effizienz)
            self.Leistung = arg_Reslast * self.Effizienz 
            
        #Kontrolle ob die Batterie �ber die Maximale Kapazit�t geladen werden w�rde
        if self.Kapazit�t + self.Leistung > self.Kapazit�t_MAX:
            self.Verlust = (self.Kapazit�t_MAX - self.Kapazit�t) * (1-self.Effizienz)
            self.Leistung = (self.Kapazit�t_MAX - self.Kapazit�t) * self.Effizienz
            
            
        #Ausf�hren des Ladevorgangs
        self.Kapazit�t += self.Leistung
        arg_Reslast -= (self.Leistung + self.Verlust)
        
        return arg_Reslast