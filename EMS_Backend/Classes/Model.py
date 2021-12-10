
from os import makedirs
from numpy.core.fromnumeric import take
import pandas as pd
import numpy as np
import matplotlib as plt
import numpy as np
from Exercise_3 import Building

class Model():

    def __init__(self, path:str):
        self.building = Building(path)
        self.df_usage = pd.read_csv("./data/usage_profiles.csv", encoding="cp1252")
        self.ta = np.genfromtxt("./data/climate.csv", delimiter=";") #°C
        self.qsolar = np.genfromtxt("./data/Solar_gains.csv") #W/m²

    def init_sim(self):
        self.qi_winter = df_usage["Qi Winter W/m²"].to_numpy()
        self.qi_sommer = df_usage["Qi Sommer W/m²"].to_numpy()
        self.qi = self.qi_winter                                 #Interne Gewinne als Kombination von Sommer und Winter, fürs erste = QI_winter
        self.ach_v = df_usage["Luftwechsel_Anlage_1_h"].to_numpy() #Air change per hour through ventilation
        self.ach_i = df_usage["Luftwechsel_Infiltration_1_h"].to_numpy() #Air change per hour through infiltration
        self.qv = np.zeros(8760)        #Ventilation losses
        self.qt = np.zeros(8760)        #transmission losses
        self.ti = np.ones(8760) * 20        #indoor temperature
        self.q_loss = np.zeros(8760)    #total thermal losses/gains
        self.qh = np.zeros(8760)        #Heating demand
        self.qc = np.zeros(8760)        #cooling demand

    def calc_qt(self, t):       #Berechnung Transmissionsverluste
        dt = self.ta[t] - self.ti[t]
        self.qt[t] = self.building.LT * dt

    def calc_qv(self, t):       #Berechnung Lüftungsverluste
        dt = self.ta[t] - self.ti[t]
        self.qv = self.building.volumen * (self.ach_i + self.ach_v) / 3600 * 1,2 * 1,01 * dt
        


    def handle_losses(self, t):
        if 
        self.q_loss[t] = self.qv[t] + self.qt[t] + self.qi_winter[t] - self.qsolar[t]



    def handle_heating(self, t):




    def handle_cooling(self, t):




    def simulate(self):

        for t in range (0,8759,1):

            #Verluste
            self.calc_qv(t)             
            self.calc_qt(t)
            self.handle_losses(t)

            #Heizung:
            self.handle_heating(t)
            
            #Kühlung:
            self.handle_cooling(t)








