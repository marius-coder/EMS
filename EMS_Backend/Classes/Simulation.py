
import pandas as pd
import numpy as np
from Building import Building


dic_geoData_in = {
    "Adresse" : "Geifieng",
    "Sondentiefe" : 100,
    "Abstand der Sonden" :10
    }

class Simulation():

    def __init__(self,bool_geothermal = False, bool_WP = False, bool_PV = False, bool_battery = False, bool_districtHeating = False, bool_heatPump = False, bool_solarPower = False, ):
         self.bool_geothermal = bool_geothermal 
         self.bool_PV = bool_PV
         self.bool_battery = bool_battery
         self.bool_districtHeating = bool_districtHeating
         self.bool_heatPump = bool_heatPump
         self.bool_solarPower = bool_solarPower
         
         self.building = Building("./data/building.xlsx")
         self.df_usage = pd.read_csv("./data/usage_profiles.csv", encoding="cp1252")
         self.ta = np.genfromtxt("./data/climate.csv", delimiter=";", usecols = (1), skip_header = 1) #°C
         self.qsolar = np.genfromtxt("./data/Solar_gains.csv") #W/m² Solar gains
         

    def Setup_Simulation(self, dic_geoData_in = {}):
        if self.bool_geothermal == True:
            self.dic_geoData_out = Get_geoData(dic_geoData_in)


        self.qi_winter = self.df_usage["Qi Winter W/m²"].to_numpy()
        self.qi_sommer = self.df_usage["Qi Sommer W/m²"].to_numpy()
        self.qi = self.qi_winter                                 #Interne Gewinne als Kombination von Sommer und Winter, f�rs erste = QI_winter
        self.ach_v = self.df_usage["Luftwechsel_Anlage_1_h"].to_numpy() #Air change per hour through ventilation
        self.ach_i = self.df_usage["Luftwechsel_Infiltration_1_h"].to_numpy() #Air change per hour through infiltration
        self.qv = np.zeros(8760)        #Ventilation losses
        self.qt = np.zeros(8760)        #transmission losses
        self.ti = np.ones(8760) * 20    #indoor temperature
        self.q_loss = np.zeros(8760)    #total thermal losses/gains
        self.qh = np.zeros(8760)        #Heating demand
        self.qc = np.zeros(8760)        #cooling demand
        self.cp_air = 0.34  # spez. Wärme kapazität * rho von Luft (Wh/m3K)

        self.t_Zul = np.ones(8760) * 20 #Zulufttemperatur TODO:Wärmerückfuhr einbauen. 
        self.t_Abl = np.ones(8760) * 20 #Ablufttemperatur
            
    def calc_QV(self, t):
        """Ventilation heat losses [W/m²BGF] at timestep t"""
        #Lüftungswärmeverlust-Koeffizient für mechanische Lüftung
        Hv = self.cp_air * self.ach_v * self.building.volumen  # W/K
        qv_mech = Hv * abs(self.t_Zul[t] - self.ti[t]) # W

        #Lüftungswärmeverlust-Koeffizient für Infiltration
        Hv = self.cp_air * self.ach_i * self.building.volumen  # W/K
        qv_inf = Hv * abs(self.ta[t] - self.ti[t]) # W

        self.qv[t] = qv_mech + qv_inf

        print(self.qv[t])

    def calc_QT(self, t):
        """Transmission heat losses [W/m²BGF] at timestep t"""
        #Transmisisonsverlust von beheizten Raum an die Außenluft eg. Wand und Dach

        #Transmissionsverlust von beheizten Raum zu unbeheizten Räumen

        #Transmissionsverlust von Bheizten Räumen an das Erdreich





        dT = self.ta[t] - self.ti[t]
        dT_boden = 6 - self.ti[t] #TODO: Annahme das der Boden konstant 6°C hat. Später durch genaueres ersetzen.
        q_wand = abs(self.building.wand["LT"] * dT)
        q_fußboden = abs(self.building.fußboden["LT"] * dT)
        q_dach = abs(self.building.dach["LT"] * dT )
        self.qt[t] = q_wand + q_fußboden + q_dach
        print(self.qt[t])
        
    def handle_losses(self, t):
        # determine losses
        self.q_loss[t] = (self.qt[t] + self.qv[t]) + self.qsolar[t] + self.qi[t]
        print(self.q_loss[t])
        # determine indoor temperature after losses
        self.ti[t] = self.TI_after_Q(self.TI[t - 1], self.q_loss[t], self.building.heat_capacity)
        print(self.ti[t])

    def Simulate(self):
        for hour in range(8760):

            self.calc_QT(hour)
            self.calc_QV(hour)
            self.handle_losses(hour)








            pass
        pass





model = Simulation()
model.Setup_Simulation()
model.Simulate()






