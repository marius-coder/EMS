
import pandas as pd
import numpy as np

class Wärmepumpe:
        
    def calc_COP(self, path:str, t_Quelle: int, t_VL:int):
        self.t_Quelle = t_Quelle
        self.t_VL = t_VL
        self.df = pd.read_csv(path, delimiter=";")
        
        self.a = np.zeros(len(self.df))                                     #erstellt ein array mit allen Quelltemperaturen
        for i in range(0, len(self.df), 1):
            self.a[i] = self.df.iloc[i,1]
        
        boolian = self.t_Quelle in self.a
        if boolian == True:
            self.df_1 = self.df.loc[self.df["t_VL"] == self.t_VL]           #erstellt df nur mit gewünschtem VL
            self.df_2 = self.df_1.loc[self.df_1["t_Q"] == self.t_Quelle]    #erstellt df nur mit gewünschtem VL und Quelltemperatur
            self.COP_t = self.df_2.iloc[0,10]
            
        else:
            self.x2 = self.a[(np.abs(self.a-t_Quelle)).argmin()]            #Wenn t_Quelle nicht in array a, dann x2 = nächster Wert

            self.df_1 = self.df.loc[self.df["t_VL"] == self.t_VL]           #erstellt df nur mit gewünschtem VL
            self.df_2 = self.df_1.loc[self.df_1["t_Q"] == self.x2]          #erstellt df nur mit gewünschtem VL und Quelltemperatur
            self.y2 = self.df_2.iloc[0,10]   
    
            self.b = self.df_2.iloc[:,10].index                             #b = Index von y2  
            self.y1 = float(self.df_1.iloc[self.b-1,10])           
            self.x1 = float(self.df_1.iloc[self.b-1,1])
            self.x = self.t_Quelle
            self.k = (self.y2-self.y1)/(self.x2-self.x1)
    
            self.COP_t = self.y1 + self.k*(self.x-self.x1)                  #berechnet COP bei Quelltemperatur (linear interpoliert)
            return self.COP_t
    
path = "./data/COP.csv"
WP = Wärmepumpe()
WP.calc_COP(path, 20, 35)

print(WP.COP_t)