




dic_geoData_in = {
    "Adresse" : "Geifieng",
    "Sondentiefe" : 100,
    "Abstand der Sonden" :10
    }

class Simulation():

    def __init__(self,bool_geothermal = False, bool_WP = False):
         self.bool_geothermal = bool_geothermal
         self.bool_PV = bool_PV
         self.bool_battery = bool_battery
         self.bool_districtHeating = bool_districtHeating
         self.bool_heatPump = bool_heatPump
         self.bool_solarPower = bool_solarPower
         
         self.building = Building("./data/building.xlsx")
         self.df_usage = pd.read_csv("./data/usage_profiles.csv", encoding="cp1252")
         self.ta = np.genfromtxt("./data/climate.csv", delimiter=";") #°C
         self.qsolar = np.genfromtxt("./data/Solar_gains.csv") #W/m²
         

    def Setup_Simulation(self, dic_geoData_in = {}):
        if self.bool_geothermal == True:
            self.dic_geoData_out = Get_geoData(dic_geoData_in)


        self.qi_winter = df_usage["Qi Winter W/m²"].to_numpy()
        self.qi_sommer = df_usage["Qi Sommer W/m²"].to_numpy()
        self.qi = self.qi_winter                                 #Interne Gewinne als Kombination von Sommer und Winter, f�rs erste = QI_winter
        self.ach_v = df_usage["Luftwechsel_Anlage_1_h"].to_numpy() #Air change per hour through ventilation
        self.ach_i = df_usage["Luftwechsel_Infiltration_1_h"].to_numpy() #Air change per hour through infiltration
        self.qv = np.zeros(8760)        #Ventilation losses
        self.qt = np.zeros(8760)        #transmission losses
        self.ti = np.ones(8760) * 20        #indoor temperature
        self.q_loss = np.zeros(8760)    #total thermal losses/gains
        self.qh = np.zeros(8760)        #Heating demand
        self.qc = np.zeros(8760)        #cooling demand

            

    def Simulate(self):
        for hour in range(8760):





            pass
        pass





model = Simulation()
model.Setup_Simulation()






