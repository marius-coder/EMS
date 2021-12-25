
import pandas as pd
import numpy as np

############################################################################################################################################

class Wärmepumpe:
        
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

############################################################################################################################################    
    
WP = Wärmepumpe()

WP.calc_COP_csv(WP.path_COP,14,35)

print(WP.COP_t)