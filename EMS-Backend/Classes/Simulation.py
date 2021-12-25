
import pandas as pd
import numpy as np
import math
from Building import Building
from Erdwärme import Get_GeothermalData
from Import import importGUI

#TODO: Alle Konstanten zusammenlegen

class Simulation():

	def __init__(self,b_geothermal = False, b_PV = False, b_battery = False, b_districtHeating = False, b_heatPump = False, b_solarPower = False, ):
		 self.b_geothermal = b_geothermal 
		 self.b_PV = b_PV
		 self.b_battery = b_battery
		 self.b_districtHeating = b_districtHeating
		 self.b_heatPump = b_heatPump
		 self.b_solarPower = b_solarPower
		 
		 self.building = Building("./EMS-Backend/data/building.xlsx")
		 self.df_usage = pd.read_csv("./EMS-Backend/data/usage_profiles.csv", encoding="cp1252")
		 self.ta = np.genfromtxt("./EMS-Backend/data/climate.csv", delimiter=";", usecols = (1), skip_header = 1) #°C
		 self.qsolar = np.genfromtxt("./EMS-Backend/data/Solar_gains.csv") #W/m² Solar gains
		 self.import_data = importGUI
		 

	def Setup_Simulation(self):
		""" """
		#TODO: Die Erdwärme in eine eigene Klasse schieben
		if self.b_geothermal == True:
			self.geo_temp = 13 #°C Bodentemperatur Quelle: https://www.wien.gv.at/stadtentwicklung/energie/themenstadtplan/erdwaerme/erlaeuterungen.html
			self.dt_geo = 5 #Temperaturdiff Quellenseite WP
			self.anz_Sonden = self.import_data.input_GeoData["Anzahl_Sonden"] #Anzahl an Sonden
			self.dic_geoData_out = Get_GeothermalData(self.import_data.input_GeoData)
			self.Q_quelleBoden = self.dic_geoData_out["Bohrtiefe"] * self.dic_geoData_out["MW_WL"] * self.anz_Sonden * self.dt_geo # W

	  


		self.qi_winter = self.df_usage["Qi Winter W/m²"].to_numpy()
		self.qi_sommer = self.df_usage["Qi Sommer W/m²"].to_numpy()
		self.qi = self.qi_winter                                 #Interne Gewinne als Kombination von Sommer und Winter, f�rs erste = QI_winter
		self.ach_v = self.df_usage["Luftwechsel_Anlage_1_h"].to_numpy() #Air change per hour through ventilation
		self.ach_i = self.df_usage["Luftwechsel_Infiltration_1_h"].to_numpy() #Air change per hour through infiltration
		self.anz_personen = self.df_usage["Pers/m2"] 
		self.q_warmwater = self.df_usage["Warmwasserbedarf_W_m2"] 
		self.q_maschinen = self.df_usage['Aufzug, Regelung etc._W_m2']
		self.q_beleuchtung = self.df_usage["Beleuchtung_W_m2"]



		
		self.qv = np.zeros(8760)        #Ventilation losses
		self.qt = np.zeros(8760)        #transmission losses
		self.ti = np.ones(8760) * 20    #indoor temperature
		self.qh = np.zeros(8760)        #Heating demand
		self.qc = np.zeros(8760)        #cooling demand
		self.CONST_Q_PERSONEN_SPEZ = 80 #W/Person
		self.cp_air = 0.34  # spez. Wärme kapazität * rho von Luft (Wh/m3K)

		self.t_Zul = np.ones(8760) * 20 #Zulufttemperatur TODO:Wärmerückgewinnung hinzufügen
		self.t_Abl = np.ones(8760) * 20 #Ablufttemperatur
		self.t_soll = np.ones(8760) * 20   #Soll Rauminnentemperatur
		self.qs = np.zeros(8760) #Solar gains array in Watt
		self.q_außen = np.zeros(8760)
		self.q_personen = np.zeros(8760)
		self.q_beleuchtung = np.zeros(8760)
		self.q_maschinen = np.zeros(8760)
		self.q_innen = np.zeros(8760)
		self.t_heating = 20
		self.t_cooling = 26
		
		self.building.insert_windows(1.2, 25)
		stat_HL = self.Static_HL()
		stat_KL = self.Static_KL()

		
		print(f"Die statische Heizlast beträgt {round(stat_HL['Heizlast [W]'] / 1000,2)} kW")
		print(f"Die statische Kühllast beträgt {round(stat_KL['Kühllast [W]'] / 1000,2)} kW")
	   
		#Annahmen TODO: In eine QT Form wandeln für user input
		#WP_COP = float(input("Bitte COP für Wärmepumpe eingeben: "))
		#WP_kW_Q = float(input("Bitte Wärmeleistung für eine Wärmepumpe in kW eingeben: "))
		#WP_Anz = float(input("Bitte Anzahl der Wärmepumpen eingeben: "))
		#WP_kW_P = WP_kW_Q / WP_COP
		#WP_kW_P = input("Bitte elektrische Leistung für Wärmepumpe in kW eingeben: ")

		#B0/W35

		









	def calc_QV(self, ach_v, ach_i, t_Zul, ta, ti ):
		"""Ventilation heat losses [W/m²BGF] at timestep t"""
		#Lüftungswärmeverlust-Koeffizient für mechanische Lüftung
		Hv = self.cp_air * ach_v * self.building.volumen  # W/K
		qv_mech = Hv * (t_Zul - ti) # W
		 
		#Lüftungswärmeverlust-Koeffizient für Infiltration
		Hv = self.cp_air * ach_i * self.building.volumen  # W/K
		qv_inf = Hv * (ta - ti) # W

		#Gesamtlüftungsverluste in Watt
		qv = qv_mech + qv_inf
		return qv
	 

	def calc_QT(self, ta, ti):
		"""Transmission heat losses [W/m²BGF] at timestep t"""
		#Transmisisonsverlust von beheizten Raum an die Außenluft eg. Wand und Dach
		dTa = ta - ti
		q_wand = self.building.wand["LT"] * dTa
		q_fenster = self.building.window["LT"] * dTa
		q_dach = self.building.dach["LT"] * dTa
		#Transmissionsverlust von beheizten Raum zu unbeheizten Räumen
		#TODO: Transmission zu unbeheizten Räumen einführen

		#Transmissionsverlust von beheizten Räumen an das Erdreich
		dT_boden = 6 - ti #TODO: Annahme das der Boden konstant 6°C hat. Später durch genaueres ersetzen.
		q_fußboden = self.building.fußboden["LT"] * dT_boden

		#Gesamttransmissionswärmeverlust in Watt
		qt = q_wand + q_fußboden + q_dach + q_fenster #Watt
		return qt

		
	def handle_losses(self, t, q_toApply):
		# determine indoor temperature after losses
		self.ti[t] = self.TI_after_Q(self.ti[t], q_toApply, self.building.heat_capacity, self.building.gfa) #°C


	def TI_after_Q(self, Ti_before, Q, cp, A):
		"""cp = spec. building heat_capacity"""
		return Ti_before + Q / A / cp

	def heating_power(self, ti_s, ti, cp, A):
		return cp * A * (ti_s - ti)

	def handle_heating(self, t, ):
		pass


	def Static_HL(self):
		min_ta = min(self.ta)
		ti = max(self.t_soll)
		max_achi = max(self.ach_i)
		max_achv = max(self.ach_v)
		t_Zul = ti #TODO: Genauer machen mit WRG

		qt = self.calc_QT(min_ta, ti)
		qv = self.calc_QV(max_achv, max_achi, t_Zul, min_ta, ti )
		
		stat_HL = {
			"Heizlast [W]" : qt + qv,
			"spez. Heizlast [W/m²]" : (qt + qv) / self.building.gfa
			}
		return stat_HL


	def Q_Personen(self, hour) -> float:
		#TODO: Variable Personenanzahl je nach Stunde
		return self.anz_personen[hour] * self.building.gfa * self.CONST_Q_PERSONEN_SPEZ #W

	def Q_Beleuchtung(self, hour) -> float:
		#TODO: Variable Beleuchtung je nach Stunde
		return self.building.gfa * self.q_beleuchtung[hour]
	
	def Q_Maschinen(self, hour) -> float:
		#TODO: Variable Maschinenlast je nach Stunde
		return self.building.gfa * self.q_maschinen[hour]

	def Q_Solar(self, hour) -> float:
		return self.qsolar[hour] * self.building.window["Fläche"]

	def Q_InnerGains(self, hour) -> float:
		return self.qi[hour] * self.building.gfa

	def Static_KL(self):
		max_value = max(self.ta)
		hour = list(self.ta).index(max_value)

		#Kühllast von Außen
		qt = self.calc_QT(self.ta[hour], self.ti[hour]) #W
		qv = self.calc_QV(self.ach_v[hour], self.ach_i[hour], self.t_soll[hour], self.ta[hour], self.ti[hour] ) #W
		qs = self.Q_Solar(hour)
		q_außen = qt + qv + qs #W

		#Innere Kühllast
		q_personen = self.Q_Personen(hour)
		q_beleuchtung = self.Q_Beleuchtung(hour)
		q_maschinen = self.Q_Maschinen(hour)
		q_innen = q_personen + q_beleuchtung + q_maschinen

		#gesamte Kühllast
		stat_KL = {
			"Kühllast [W]" : q_außen + q_innen,
			"spez. Kühllast [W/m²]" : (q_außen + q_innen) / self.building.gfa
			}
		return stat_KL

	def Simulate(self):
		for hour in range(8760):		
			
			day_1 = math.ceil((hour + 1) / 24)

			mean_temp = sum(self.ta[day_1 * 24 : day_1 * 24 + 24]) / 24

#-----------------------------------------------------------------------------------------------------------------------------------------------------------    
			#Heiz / Kühllast berechnen
			#Äußere Wärmeströme
			self.qt[hour] = self.calc_QT( self.ta[hour], self.ti[hour]) #Transmission
			self.qv[hour] = self.calc_QV( self.ach_v[hour], self.ach_i[hour], self.t_Zul[hour], self.ta[hour], self.ti[hour]) #Ventilation
			self.qs[hour] = self.Q_Solar(hour) #Solare Gewinne
			self.q_außen[hour] = self.qt[hour] + self.qv[hour] + self.qs[hour] #W Gesamt

			#Innere Wärmeströme
			self.q_personen[hour] = self.Q_Personen(hour)
			self.q_beleuchtung[hour] = self.Q_Beleuchtung(hour)
			self.q_maschinen[hour] = self.Q_Maschinen(hour)
			self.q_innen[hour] = self.q_personen[hour] + self.q_beleuchtung[hour] + self.q_maschinen[hour]

			#Gesamtwärmeströme
			self.q_gesamt = self.q_außen[hour] + self.q_innen[hour]
			self.handle_losses(hour, q_toApply = self.q_gesamt) #Neue Innentemperatur rechnen
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
			#Nun wird mithilfe der neuen Innentemperatur die benötigte Leistung berechnet um auf die gewünschte Innentemp zu kommen
			#TODO: Variable Sollinnentemperatur, zB Nachtabsenkung, Temperaturhysterese
			self.q_soll = self.heating_power(self.t_soll[hour], self.ti[hour], self.building.heat_capacity, self.building.gfa)
			self.handle_losses(hour, q_toApply = self.q_soll)





model = Simulation(b_geothermal = True)
model.Setup_Simulation()
model.Simulate()