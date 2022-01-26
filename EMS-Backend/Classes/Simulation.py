﻿
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
#from Building import Building
#from Erdwärme import Get_GeothermalData
#from Import import importGUI
import importlib

ImportBuilding = importlib.import_module("EMS-Backend.Classes.Building")
ImportSpeicher = importlib.import_module("EMS-Backend.Classes.Wärmespeicher")
ImportWP = importlib.import_module("EMS-Backend.Classes.Wärmepumpe")
ImportStromnetz = importlib.import_module("EMS-Backend.Classes.Stromnetz")
ImportErdwärme = importlib.import_module("EMS-Backend.Classes.Erdwärme")
Import = importlib.import_module("EMS-Backend.Classes.Import")



from bokeh.plotting import figure, show


class Simulation():

	def __init__(self,b_geothermal = False, b_PV = False, b_battery = False, b_districtHeating = False, b_heatPump = False, b_solarPower = False, ):
		 self.b_geothermal = b_geothermal 
		 self.b_PV = b_PV
		 self.b_battery = b_battery
		 self.b_districtHeating = b_districtHeating
		 self.b_heatPump = b_heatPump
		 self.b_solarPower = b_solarPower
		 
		 self.building = ImportBuilding.Building("./EMS-Backend/data/building.xlsx")
		 self.df_usage = pd.read_csv("./EMS-Backend/data/usage_profiles.csv", encoding="cp1252")
		 self.ta = np.genfromtxt("./EMS-Backend/data/climate.csv", delimiter=";", usecols = (1), skip_header = 1) #°C
		 self.qsolar = np.genfromtxt("./EMS-Backend/data/Solar_gains.csv") #W/m² Solar gains
		 self.import_data = Import.importGUI
		 self.warmwater_data = self.import_data.input_Warmwater
		 self.PV_Bat_data = self.import_data.input_PV_Batterie
		 self.WP_Heizen = self.import_data.input_WP_Heizen
		 self.speicher_HZG = self.import_data.input_Speicher_HZG
		 self.WP_WW = self.import_data.input_WP_WW
		 self.speicher_WW = self.import_data.input_Speicher_WW

	def Setup_Simulation(self):
		""" """
		self.qi_winter = self.df_usage["Qi Winter W/m²"].to_numpy()
		self.qi_sommer = self.df_usage["Qi Sommer W/m²"].to_numpy()
		self.qi = self.qi_winter                                 #Interne Gewinne als Kombination von Sommer und Winter, f�rs erste = QI_winter
		self.ach_v = self.df_usage["Luftwechsel_Anlage_1_h"].to_numpy() #Air change per hour through ventilation
		self.ach_i = self.df_usage["Luftwechsel_Infiltration_1_h"].to_numpy() #Air change per hour through infiltration
		self.anz_personen = self.df_usage["Pers/m2"] 
		#self.q_warmwater = self.df_usage["Warmwasserbedarf_W_m2"] 
		self.q_warmwater = np.zeros(8760)
		self.q_maschinen = self.df_usage['Aufzug, Regelung etc._W_m2']
		self.q_beleuchtung = self.df_usage["Beleuchtung_W_m2"]
		self.Pel_gebäude = np.zeros(8760)



		
		self.qv = np.zeros(8760)        #Ventilation losses
		self.qt = np.zeros(8760)        #transmission losses
		self.ti = np.zeros(8760)        #indoor temperature
		self.ti_sim = 20                #Laufvariable für die Innentemperatur
		self.qh = np.zeros(8760)        #Heating demand
		self.qc = np.zeros(8760)        #cooling demand
		self.CONST_Q_PERSONEN_SPEZ = 80 #W/Person
		self.cp_air = 0.34  # spez. Wärme kapazität * rho von Luft (Wh/m3K)

		self.t_Zul = np.ones(8760) #Zulufttemperatur
		self.t_Abl = np.ones(8760) #Ablufttemperatur
		self.t_soll = np.ones(8760) * 20   #Soll Rauminnentemperatur
		self.qs = np.zeros(8760) #Solar gains array in Watt
		self.q_außen = np.zeros(8760)
		self.q_personen = np.zeros(8760)
		self.q_beleuchtung = np.zeros(8760)
		self.q_maschinen = np.zeros(8760)
		self.q_innen = np.zeros(8760)
		self.t_heating = 20
		self.t_cooling = 26
		self.b_heating = True
		
		self.t_hzg_VL = 30
		self.t_hzg_RL = 25
		self.t_klg_VL = 8
		self.t_klg_RL = 12
		self.t_WW_VL = 50

		self.Speicher_HZG = ImportSpeicher.Wärmespeicher(self.speicher_HZG, self.t_hzg_VL, self.t_hzg_RL)
		self.WP_HZG = ImportWP.Wärmepumpe(speicher = self.Speicher_HZG,data_WP = self.WP_Heizen, geb_VL_HZG = self.t_hzg_VL, geb_VL_KLG = self.t_klg_VL)


		self.Speicher_WW = ImportSpeicher.Wärmespeicher(self.speicher_WW, self.t_hzg_VL, self.t_hzg_RL)
		self.WP_WW = ImportWP.Wärmepumpe(speicher = self.Speicher_WW,data_WP = self.WP_WW, geb_VL_HZG = self.t_WW_VL, geb_VL_KLG = 0)
		self.Stromnetz = ImportStromnetz.Stromnetz(self.PV_Bat_data)
		
		
		data_Sim = {
			"Punkte X" : 60,
			"Punkte Y" : 60,
			"Länge Punkt [m]" : 0.5,
			"Länge Sonde [m]" : 0.2,
			}

		data_Boden = {
			"Temperatur" : 6,
			"Temperatur Einspeisung" : 11,
			"cp" : 1000,
			"rho" : 2600}
		self.Erd_Sim = ImportErdwärme.BKA(data_Sim, data_Boden, self.import_data.input_GeoData)
		self.Erd_Sim.Init_Sim()

		stat_HL = self.Static_HL()
		stat_KL = self.Static_KL()

		self.heating_months = [1, 2, 3, 4, 9, 10, 11, 12]
		self.cooling_months = [4, 5, 6, 7, 8, 9]


		
		print(f"Die statische Heizlast beträgt {round(stat_HL['Heizlast [W]'] / 1000,2)} kW")
		print(f"Die statische Kühllast beträgt {round(stat_KL['Kühllast [W]'] / 1000,2)} kW")


	   
	def calc_t_Zul(self, hour):
		WRG = self.building.WRG
		self.t_Abl[hour] = self.ti[hour]
		self.t_Zul[hour] = self.t_Abl[hour] * WRG + self.t_Abl[hour] * (1 - WRG)
		print(f"Zulufttemperatur: {self.t_Zul[hour]} °C")

	def calc_QV(self, ach_v, ach_i, t_Zul, ta, ti ):
		"""Ventilation heat losses [W/m²BGF] at timestep t"""
		#Lüftungswärmeverlust-Koeffizient für mechanische Lüftung
		Hv = self.cp_air * ach_v * self.building.volumen  # W/K
		qv_mech = Hv * (t_Zul - ti) # W
		 
		#Lüftungswärmeverlust-Koeffizient für Infiltration
		Hv = self.cp_air * ach_i * self.building.volumen  # W/K
		qv_inf = Hv * (ta - ti) # W

		#Gesamtlüftungsverluste in Watt
		qv = (qv_mech + qv_inf)
		return qv
	 

	def calc_QT(self, ta, ti):
		"""Transmission heat losses [W/m²BGF] at timestep t"""
		#Transmisisonsverlust von beheizten Raum an die Außenluft eg. Wand und Dach
		dTa = ta - ti
		q_wand = self.building.wand["LT"] * dTa
		q_fenster = self.building.window["LT"] * dTa
		q_dach = self.building.dach["LT"] * dTa
		#Transmissionsverlust von beheizten Raum zu unbeheizten Räumen
		#N.V.

		#Transmissionsverlust von beheizten Räumen an das Erdreich
		dT_boden = 6 - ti #Annahme das der Boden konstant 6°C hat.
		q_fußboden = self.building.fußboden["LT"] * dT_boden

		#Gesamttransmissionswärmeverlust in Watt
		qt = (q_wand + q_fußboden + q_dach + q_fenster) #Watt
		return qt

		
	def handle_losses(self, t, q_toApply):
		# determine indoor temperature after losses
		self.ti_sim = self.TI_after_Q(self.ti_sim, q_toApply, self.building.heat_capacity, self.building.gfa) #°C


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
		t_Zul = min_ta

		qt = self.calc_QT(min_ta, ti)
		qv = self.calc_QV(max_achv, max_achi, t_Zul, min_ta, ti )
		
		stat_HL = {
			"Heizlast [W]" : qt + qv,
			"spez. Heizlast [W/m²]" : (qt + qv) / self.building.gfa
			}
		return stat_HL


	def Q_Personen(self, hour) -> float:
		return self.anz_personen[hour] * self.building.gfa * self.CONST_Q_PERSONEN_SPEZ #W

	def Q_Beleuchtung(self, hour) -> float:
		return self.building.gfa * self.q_beleuchtung[hour]
	
	def Q_Maschinen(self, hour) -> float:
		return self.building.gfa * self.q_maschinen[hour]

	def Q_Solar(self, hour) -> float:
		return self.qsolar[hour] * self.building.window["Fläche"]

	def Q_InnerGains(self, hour) -> float:
		return self.qi[hour] * self.building.gfa

	def Static_KL(self):
		max_value = max(self.ta)
		hour = list(self.ta).index(max_value)

		#Kühllast von Außen
		qt = self.calc_QT(self.ta[hour], 26) #W
		qv = self.calc_QV(self.ach_v[hour], self.ach_i[hour], self.t_soll[hour], self.ta[hour], 26 ) #W
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
			
			#Zulufttemperatur rechnen
			self.calc_t_Zul(hour-1)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------    
			#Heiz / Kühllast berechnen
			#Äußere Wärmeströme
			self.qt[hour] = self.calc_QT( self.ta[hour], self.ti_sim) #Transmission
			self.qv[hour] = self.calc_QV( self.ach_v[hour], self.ach_i[hour], self.t_Zul[hour], self.ta[hour], self.ti_sim) #Ventilation
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
			print("Stunde: ",hour)
			print("Verluste: ",self.q_gesamt)
			print("Temp vor Heizen: ",self.ti_sim)
			self.ti[hour] = self.ti_sim

			self.WP_HZG.COP_betrieb[hour] = self.WP_HZG.GetCOP(self.ta[hour])
			print(f"COP Heizen bei {self.ta[hour]} °C Außentemperatur: {self.WP_HZG.COP_betrieb[hour]}")
			print(f"Object Heizen: {self.WP_HZG.speicher}")
			print(f"Object WW: {self.WP_WW.speicher}")

			#Heizen
			if DetermineMonth(hour) in self.heating_months:

				#Check_SpeicherHeizen kontrolliert die Speichertemperatur und führt die Verlustvorgänge für den Speicher durch
				#Wenn notwendig schaltet diese Funktion auch die WP ein
				self.WP_HZG.Check_SpeicherHeizen(hour)

				if self.WP_HZG.is_on[hour] == True:
					self.WP_HZG.Pel_Betrieb[hour] = self.WP_HZG.Pel
				else:
					self.WP_HZG.Pel_Betrieb[hour] = 0
				#Benötigte Wärmeenergie um auf Solltemperatur zu kommen
				self.q_soll = self.heating_power(self.t_soll[hour], self.ti_sim, self.building.heat_capacity, self.building.gfa)
				self.qh[hour] = self.q_soll

				#Energie aus dem Speicher entnehmen
				self.WP_HZG.speicher.Speicher_Entladen(Q_Entladen = self.q_soll, RL = self.t_hzg_RL)
				#Neue Innentemperatur berechnen
				self.handle_losses(hour, q_toApply = self.q_soll)



			elif DetermineMonth(hour) in self.cooling_months:

				#Check_SpeicherKühlen kontrolliert die Speichertemperatur und führt die Verlustvorgänge für den Speicher durch
				#Wenn notwendig schaltet diese Funktion auch die WP ein
				self.WP_HZG.Check_SpeicherKühlen(hour)

				if self.WP_HZG.is_on[hour] == True:
					self.WP_HZG.Pel_Betrieb[hour] = self.WP_HZG.Pel
				else:
					self.WP_HZG.Pel_Betrieb[hour] = 0
				#Benötigte Wärmeenergie um auf Solltemperatur zu kommen
				self.q_soll = self.heating_power(self.t_soll[hour], self.ti_sim, self.building.heat_capacity, self.building.gfa)
				self.qc[hour] = self.q_soll

				#Energie aus dem Speicher entnehmen
				self.WP_HZG.speicher.Speicher_Entladen(Q_Entladen = self.q_soll, RL = self.t_hzg_RL)
				#Neue Innentemperatur berechnen
				self.handle_losses(hour, q_toApply = self.q_soll)
			print("Temp nach Heizen: ",self.ti_sim)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------		
			#Warmwasser
			month = DetermineMonth(hour)
			hourofDay = DetermineHourofDay(hour)

			self.WP_WW.COP_betrieb[hour] = self.WP_WW.GetCOP(self.ta[hour])
			print(f"COP Warmwasser bei {self.ta[hour]} °C Außentemperatur: {self.WP_WW.COP_betrieb[hour]}")
			Q_warmwater = self.CalcWarmwaterEnergy(month, hourofDay)
			self.q_warmwater[hour] = Q_warmwater
			print(f"Benötigte Warmwasserleistung: {Q_warmwater/1000} kW")
			#Check_SpeicherHeizen kontrolliert die Speichertemperatur und führt die Verlustvorgänge für den Speicher durch
			#Wenn notwendig schaltet diese Funktion auch die WP ein
			self.WP_WW.Check_SpeicherHeizen(hour)

			if self.WP_WW.is_on[hour] == True:
				self.WP_WW.Pel_Betrieb[hour] = self.WP_WW.Pel
			else:
				self.WP_WW.Pel_Betrieb[hour] = 0
			#Energie aus dem Speicher entnehmen
			self.WP_WW.speicher.Speicher_Entladen(Q_Entladen = self.q_warmwater[hour], RL = 15)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
			#Strom			
			self.Pel_gebäude[hour] = self.CalcStrombedarf(hour, month, hourofDay)
			print(f"Benötigte Stromleistung: {self.Pel_gebäude[hour]/1000} kW")
			reslast = self.Stromnetz.CalcResLast(hour,self.Pel_gebäude[hour])
			self.Stromnetz.CheckResLast(hour,reslast)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
			#Simulation-Bodenerwärmung
			Q_toDump = self.WP_WW.Pel_Betrieb[hour] + self.WP_HZG.Pel_Betrieb[hour] +\
						self.q_warmwater[hour] + self.q_soll
			self.Erd_Sim.Simulate(Q_toDump)
			

			print("---------------------------------------------------------------")
		print(f"MAXIMALE TEMPERATUR: {max(self.ti)}")
		print(f"MINIMALE TEMPERATUR: {min(self.ti)}")

		sns.heatmap(self.Erd_Sim.Get_Attr_List("temperatur"), square=True, cmap='viridis')
		plt.show()


			
	def CalcWarmwaterEnergy(self, month, hourofDay):
		m_water = self.import_data.input_Warmwater["hour [l/h]"][month-1][hourofDay]  #liter
		print(f"Warmwasserverbauch in liter: {m_water}")
		Q_waterheating = m_water * 4180 * (60-15) /3600
		return Q_waterheating

	def CalcStrombedarf(self, hour, month, hourofDay):
		"""Diese Funktion nimmt das importierte Stromprofil, extrahiert den Strombedarf und addiert extra Verbraucher dazu 
		(Die beiden Wärmepumpen)"""

		#Profilentnahme
		P_profile = self.import_data.input_Strombedarf["hour [kWh/h]"][month-1][hourofDay] * 1000  #Watt
		#Hinzufügen der Wärmepumpen
		P_profile += self.WP_HZG.Pel_Betrieb[hour] + self.WP_WW.Pel_Betrieb[hour]
		return P_profile

def DetermineHourofDay(hour):
	return (hour+1) % 24


def DetermineMonth(hour):
	if 0 <= hour <= 744:
		return 1
	elif 744 < hour <= 1416:
		return 2
	elif 1416 < hour <= 2160:
		return 3
	elif 2160 < hour <= 2880:
		return 4
	elif 2880 < hour <= 3624:
		return 5
	elif 3624 < hour <= 4344:
		return 6
	elif 4344 < hour <= 5088:
		return 7
	elif 5088 < hour <= 5832:
		return 8
	elif 5832 < hour <= 6552:
		return 9
	elif 6552 < hour <= 7296:
		return 10
	elif 7296 < hour <= 8016:
		return 11
	elif 8016 < hour <= 8760:
		return 12



#model = Simulation(b_geothermal = False)
#model.Setup_Simulation()
#model.Simulate()

