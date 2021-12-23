
import pandas as pd
import numpy as np

############################################################################################################################################

class Wärmepumpe:
        
    def __init__(self,
                 # WP_Anzahl,
                 path_COP = r"C:\Users\Chris\Desktop\Inplan\Wärmepumpe\COP.csv",
                 path_climate = r"C:\Users\Chris\Desktop\Inplan\Wärmepumpe\climate.csv",
                 t_VL = 45,           #°C
                 # t_Q = False,       #°C
                 L_T = 758.27,        #W/K
                 L_V = 713.24,        #W/K
                 t_i = 22,            #°C
                 ):

        
        self.path_COP = path_COP
        self.path_climate = path_climate
        self.t_VL = t_VL
        self.t_Q = np.genfromtxt(self.path_climate, delimiter = ";")
        self.L_T = L_T
        self.L_V = L_V
        self.L = self.L_T + self.L_V
        self.t_i = t_i
        # self.WP_Anzahl = WP_Anzahl
        
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
        
#------------------------------------------------------------------------------

    def simulate(self):
        Q = np.zeros(len(self.t_Q)-1)
        P = np.zeros(len(self.t_Q)-1)
        for i in range(0,len(self.t_Q)-1,1):
            dt = (self.t_i - self.t_Q[i+1,1])
            Q[i] = self.L * dt / 1000                                          #kWh
            self.calc_COP(self.path_COP, self.t_Q[i+1,1], self.t_VL)
            P[i] = Q[i] / self.COP_t                                           #kWh
            print(i)
        
        self.f_JAZ = sum(Q) / sum(P)
        self.Energiekennzahlen = {"JAZ" : self.f_JAZ,
                    "Q" : Q,
                    "P" :P}
        return self.Energiekennzahlen
       
    
############################################################################################################################################    
    
WP = Wärmepumpe()

# WP.calc_COP(WP.path_COP,10,35)
WP.simulate()

# JAZ = WP.dic["JAZ"]
# Q = WP.Energiekennzahlen["Q"]
# P = WP.Energiekennzahlen["P"]

print(WP.COP_t)




