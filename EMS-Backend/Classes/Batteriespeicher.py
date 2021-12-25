
  
class cla_Batterie():
    
    def __init__(self, var_EntTiefe, var_Effizienz, var_kapMAX, var_LadeEntladeLeistung = 0, var_SelbstEntladung = 0):
        self.Entladetiefe = var_kapMAX * var_EntTiefe / 100  #%
        self.Effizienz = var_Effizienz # Einheit %/100
        self.Kapazität = 0 #kWh
        self.Kapazität_MAX = var_kapMAX #kWh
        self.Leistung = var_LadeEntladeLeistung #kW
        self.Leistung_MAX = var_kapMAX * 0.5 #kW
        self.Verlust = 0 #kW
        self.Selbstentladung = var_SelbstEntladung / 8760 #in %/Stunde

    def StehVerluste(self):
        self.Kapazität = self.Kapazität - self.Kapazität * self.Selbstentladung
        self.Verlust += self.Kapazität * self.Selbstentladung

    def Entladen(self,arg_Reslast):
        #self.Leistung ist der Teil der anschließend von der Reslast abgezogen wird
        

        if arg_Reslast > self.Leistung_MAX:
            #Wenn ja wird gekappt
            self.Verlust = self.Leistung_MAX * (1-self.Effizienz)
            self.Leistung = self.Leistung_MAX * self.Effizienz 
        else:
            #Wenn nein, g2g
            self.Verlust = arg_Reslast * (1-self.Effizienz) 
            self.Leistung = arg_Reslast 

        #Kontrolle der Leistung
        if self.Leistung + self.Verlust > self.Kapazität:
            #Wenn nicht genügend Kapazität vorhanden ist wird die Leistung gekappt
            self.Verlust = self.Kapazität * (1-self.Effizienz)
            self.Leistung = self.Kapazität - self.Verlust
            
        #Ausführen des Entladevorgangs
        self.Kapazität -= self.Leistung + self.Verlust
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
            
        #Kontrolle ob die Batterie über die Maximale Kapazität geladen werden würde
        if self.Kapazität + self.Leistung > self.Kapazität_MAX:
            self.Verlust = (self.Kapazität_MAX - self.Kapazität) * (1-self.Effizienz)
            self.Leistung = (self.Kapazität_MAX - self.Kapazität) * self.Effizienz
            
            
        #Ausführen des Ladevorgangs
        self.Kapazität += self.Leistung
        arg_Reslast -= (self.Leistung + self.Verlust)
        
        return arg_Reslast