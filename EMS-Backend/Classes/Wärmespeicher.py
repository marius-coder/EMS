

import math
import matplotlib.pyplot as plt
#Library die die physikalischen Werte von Wasser berechen kann
from iapws._iapws import _Liquid
#Dict with calculated properties of water. The available properties are:
#h: Specific enthalpy, [kJ/kg]
#u: Specific internal energy, [kJ/kg]
#a: Specific Helmholtz energy, [kJ/kg]
#g: Specific Gibbs energy, [kJ/kg]
#s: Specific entropy, [kJ/kgK]
#cp: Specific isobaric heat capacity, [kJ/kgK]
#cv: Specific isochoric heat capacity, [kJ/kgK]
#w: Speed of sound, [m/s²]
#rho: Density, [kg/m³]
#v: Specific volume, [m³/kg]
#vt: [∂v/∂T]P, [m³/kgK]
#vtt: [∂²v/∂T²]P, [m³/kgK²]
#vp: [∂v/∂P]T, [m³/kg/MPa]
#vtp: [∂²v/∂T∂P], [m³/kg/MPa]
#alfav: Cubic expansion coefficient, [1/K]
#xkappa : Isothermal compressibility, [1/MPa]
#ks: Isentropic compressibility, [1/MPa]
#mu: Viscosity, [mPas]
#k: Thermal conductivity, [W/mK]
#epsilon: Dielectric constant, [-]

global debug
debug = False
global li_test

class Wärmespeicher():

	def __init__(self, data_Speicher, VL, RL):
		dicke_dämmung = data_Speicher["Dämmdicke"]
		lambda_dämmung = data_Speicher["Lambda_Dämmung"]
		schichten = data_Speicher["anz_Schichten"]
		height = data_Speicher["Höhe"]
		ladezone = data_Speicher["Ladeschicht"]
		radius = data_Speicher["Radius"]
		diameter = data_Speicher["Radius"] * 2

		if radius == None and diameter == None:
			raise ValueError("Bitte einen Radius bzw. einen Durchmesser angeben")
		elif radius == None:
			radius = diameter / 2
		elif diameter == None:
			diameter = radius * 2
		

		#Geometrie des Gesamten speichers
		self.geometry = {
			"Radius [m]" : diameter / 2,
			"Durchmesser [m]" : radius * 2,
			"Höhe [m]" : height,
			"Volumen [m³]" : math.pi * radius**2 * height,
			"Fläche_Boden [m²]" : math.pi * radius**2,
			"Mantelfläche [m²]" : 2 * math.pi * radius * height,
			"Oberfläche [m²]" : 2 * math.pi * radius * (radius + height)
			}
		self.lambda_dämmung = lambda_dämmung
		self.dicke_dämmung = dicke_dämmung
		self.t_VL = VL
		self.t_RL = RL
		self.t_umg = 20 #Annahme dass der Technikraum immer 20°C hat.
		self.anz_schichten = schichten
		self.ladezone = ladezone
		height_schicht = height / self.anz_schichten
		def Create_Schicht(id,height_schicht):
			schicht = {
			"ID" : id+1,
			"Höhe [m]" : height_schicht,
			"Volumen [m³]" : math.pi * radius**2 * height_schicht,
			"Fläche [m²]" : math.pi * radius**2,
			"Mantelfläche [m²]" : 2 * math.pi * radius * height_schicht,
			"Temperatur [°C]" : None,
			"Energie [kJ]" : None
			}
			return schicht

		#Liste an Schichten erstellen
		self.li_schichten = []
		dT = (self.t_VL - self.t_RL) / self.anz_schichten
		for i in range(self.anz_schichten):
			self.li_schichten.append(Create_Schicht(i,height_schicht))
			self.li_schichten[i]["Temperatur [°C]"] = self.t_RL + dT * i

	def Heat_Transmission_BodenDeckel(self, schicht):
		q_HT_BdDk = (self.lambda_dämmung/self.dicke_dämmung) * schicht["Fläche [m²]"] * (schicht["Temperatur [°C]"] - self.t_umg) #Watt
		return q_HT_BdDk

	def Heat_Transmission(self, schicht):
		r1 = self.geometry["Radius [m]"] 
		r2 = self.geometry["Radius [m]"] + self.dicke_dämmung	
		oben = 2 * (math.pi * schicht["Höhe [m]"] * (schicht["Temperatur [°C]"] - self.t_umg))
		unten = ((1/self.lambda_dämmung)* math.log(r2/r1))
		q_HT = 2 * (math.pi * schicht["Höhe [m]"] * (schicht["Temperatur [°C]"] - self.t_umg)) / ((1/self.lambda_dämmung)* math.log(r2/r1)) #Watt
		return q_HT
	
	def New_Temperature(self, q_toApply, schicht):
		"""Diese Funktion nimmt eine Schicht und Verlust und berechnet eine neue Temperatur damit"""
		try:
			water_data = _Liquid(273 + schicht["Temperatur [°C]"])
		except:
			pass
		t_new = schicht["Temperatur [°C]"] - q_toApply / (water_data["cp"] * 1000 * water_data["rho"] * schicht["Volumen [m³]"]) 
		return t_new

	def Transmission_total(self):
		"""Diese Funktion berechnet den Transmissionswärmeverlust des Speichers und berechnet anschließend die neue Temperatur"""
		#Alle schichten durchiterieren
		q_trans_Sum = 0
		for i in range(self.anz_schichten):

			q_schicht = self.Heat_Transmission(self.li_schichten[i])

			if i == 0:
				q_bottom = self.Heat_Transmission_BodenDeckel(self.li_schichten[0])
				q_toApply = q_schicht + q_bottom
				self.li_schichten[i]["Temperatur [°C]"] = self.New_Temperature(q_toApply, self.li_schichten[i])
			elif i == (self.anz_schichten - 1):
				q_top = self.Heat_Transmission_BodenDeckel(self.li_schichten[-1])
				q_toApply = q_schicht + q_top
				self.li_schichten[i]["Temperatur [°C]"] = self.New_Temperature(q_toApply, self.li_schichten[i])
				
				
				#print("Temp: ", self.li_schichten[i]["Temperatur [°C]"])
			else:
				q_toApply = q_schicht
				self.li_schichten[i]["Temperatur [°C]"] = self.New_Temperature(q_toApply, self.li_schichten[i])
			q_trans_Sum += q_toApply
		print("Speicher Verlust durch Transmission: ", q_trans_Sum, " Watt")


	def Get_Alpha_Convection(self, schicht_hoch, schicht_niedrig):
		"""Diese Gleichung berechnet den Energieaustausch zwischen Schichten aufgurnd von Temperaturunterschieden
		Dabei wird immer von einer natürlichen Konvektion ausgegangen
		Ergebnis ist der Wärmeübergangskoeffizient alpha der in W/m²K angegeben ist"""

		water_data = _Liquid(schicht_hoch["Temperatur [°C]"] + 273)
		
		l_char = self.geometry["Durchmesser [m]"] #meter
		rho = water_data["rho"]
		w = 0.05 #m/s Eintrittsgeschwindigkeit in Speicher
		n = water_data["mu"]  #dynamische Viskosität Pas
		v =  n / rho #kinematische viskosität 1/K
		k = water_data["k"] # W/mK lambda
		cp = water_data["cp"] #kJ/kgK
		g = 9.81 #m/s²
	
		#Grashofzahl berechnen
		Raumausdehnungskoeffizient = 1 / ((schicht_niedrig["Temperatur [°C]"] + schicht_hoch["Temperatur [°C]"])/2) #1/K
	
		dT = schicht_hoch["Temperatur [°C]"] - schicht_niedrig["Temperatur [°C]"]
		GR = (g * l_char**3 * Raumausdehnungskoeffizient * rho**2 * dT)/ n**2 
		#print("Grashofzahl ist: ", GR)

		#Prandtlzahl berechnen
		PR = (n*cp*1000)/k
		#print("Prandtlzahl ist: ", PR)

		#Rayleigh Zahl berechnen
		RA = GR / PR
		#print("Rayleighzahl ist: ", RA)

		#Nusselt Zahl berechnen
		#Formel von hier: https://studyflix.de/ingenieurwissenschaften/naturliche-konvektion-480
		NU = (0.825 + ((0.387 * RA**(1/6)))/(1 + (0.492 / PR)**(9/16))**(8/27))**2
		#print("Nusseltzahl ist: ", NU)

		#Berechnung des Wärmepbergangskoeffizienten alpha
		alpha = (NU * k) / l_char
		return alpha

	def Heat_Convection(self):
		"""Diese Funktion wird nur benötigt wenn es eine untere Schicht gibt, die wärmer ist als eine obere"""

		
		#In Position 0 befindet sich die unterste Schicht. Dieser Loop geht also den Speicher von unten nach oben durch
		#und sucht ob eine untere Schicht wärmer ist als die obere
		for i in range(len(self.li_schichten)-1): #Es gibt immer um 1 weniger Anzahl an kontaktflächen als Anzahl schichten

			temp1 = self.li_schichten[i]["Temperatur [°C]"]
			temp2 = self.li_schichten[i+1]["Temperatur [°C]"]

			if temp1 > temp2:

				dT = self.li_schichten[i]["Temperatur [°C]"] - self.li_schichten[i+1]["Temperatur [°C]"]
				alpha = self.Get_Alpha_Convection(self.li_schichten[i],self.li_schichten[i+1])
				
				#Leistung zwischen Schicht berechnen
				Q_schicht = alpha * dT * self.li_schichten[i]["Fläche [m²]"] 				

				#Massenstrom der sich in einer Stunde durch natürliche Konvektion ergibt
				water_data = _Liquid(273 + self.li_schichten[i]["Temperatur [°C]"])
				m_auftrieb = (Q_schicht) / (water_data["cp"] * 1000 * (self.li_schichten[i]["Temperatur [°C]"] - self.li_schichten[i+1]["Temperatur [°C]"])) * 3600

				if debug == True:
					print(f"Alpha: {alpha} W/m²K")
					print(f"Temperatur Schicht {i} {self.li_schichten[i]['Temperatur [°C]']} °C")
					print(f"Temperatur Schicht {i+1} {self.li_schichten[i+1]['Temperatur [°C]']} °C")
					print(f"Leistung zwischen Schicht {i} und Schicht {i+1} ist {Q_schicht} Watt")
					print("-------------------------------------------------------------------------------")
				#Neue Temperaturen rechnen
				schicht_unten = self.li_schichten[i]
				schicht_unten["Masse"] = schicht_unten["Volumen [m³]"] * water_data["rho"]
				schicht_oben = self.li_schichten[i+1]
				schicht_oben["Masse"] = schicht_oben["Volumen [m³]"] * water_data["rho"]

				t_neu_oben = ((m_auftrieb * schicht_unten["Temperatur [°C]"]) + (schicht_oben["Masse"] * schicht_oben["Temperatur [°C]"])) / \
						(m_auftrieb + schicht_oben["Masse"])

				t_neu_unten = ((m_auftrieb * schicht_oben["Temperatur [°C]"]) + (schicht_unten["Masse"] * schicht_unten["Temperatur [°C]"])) / \
						(m_auftrieb + schicht_unten["Masse"])

				
				self.li_schichten[i]["Temperatur [°C]"] = t_neu_unten
				self.li_schichten[i+1]["Temperatur [°C]"] = t_neu_oben


				if debug == True:
					print(f"Neue Temperatur Schicht {i}: {t_neu_unten} °C")
					print(f"Neue Temperatur Schicht {i+1}: {t_neu_oben} °C")
					print("-------------------------------------------------------------------------------")	


	def Speicher_Laden(self, massenstrom, VL):
		"""
		Parameters:
		massenstrom: Massenstrom der geladen wird in kg/h
		VL: Temperatur des Massenstromes in °C kommend von der WP
		"""
		#Zwischenvariablen
		water_data = _Liquid(273 + VL)
		schicht_laden = self.li_schichten[self.ladezone-1]
		schicht_laden["Masse"] = schicht_laden["Volumen [m³]"] * water_data["rho"]
		m_new = massenstrom / 10 #pro timestep werden nur 10% der Masse verwendet

		for timestep in range(10):
		#Diese Iterierung wird 10 mal gemacht um einerseits die Durchmischung als auch die Verdrängung der einzelnen Schichten zu simulieren.
		#Neue Temperatur für Ladeschicht
			t_neu_schicht_laden = ((m_new * VL) + (schicht_laden["Masse"] * schicht_laden["Temperatur [°C]"])) / \
							(m_new + schicht_laden["Masse"])	

			self.li_schichten[self.ladezone-1]["Temperatur [°C]"] = t_neu_schicht_laden

		#Nun werden alle Schichten unter der Ladezone iteriert und die Temperatur angepasst da sich nun Wasser mit unterschiedlicher Temperatur mischt
		#Dabei wird von der Ladeschicht nach unten iteriert				
			for i in range(self.ladezone - 1, 0, -1 ):

				#Zwischenvariablen definieren zwecks Übersichtlichkeit
				schicht_unten = self.li_schichten[i-1]
				schicht_oben = self.li_schichten[i]
			
				#Zwischenvariable
				schicht_unten["Masse"] = schicht_unten["Volumen [m³]"] * water_data["rho"]

				t_neu = ((m_new * schicht_oben["Temperatur [°C]"]) + (schicht_unten["Masse"] * schicht_unten["Temperatur [°C]"])) / \
							(m_new + schicht_unten["Masse"])
				self.li_schichten[i-1]["Temperatur [°C]"] = t_neu

		if debug == True:
			for i in range(self.ladezone - 1, 0, -1 ):		
				print(f"Funktion: Speicher_Laden")
				print(f"Ort: Iterierung nach Speicherladung")
				print(f"Temperatur Schicht {i+1} {self.li_schichten[i]['Temperatur [°C]']} °C")
				print(f"Temperatur Schicht {i} {self.li_schichten[i-1]['Temperatur [°C]']} °C")
				print(f"Massenstrom zwischen Schicht {i} und Schicht {i+1} ist {m_new*10} kg/h")
				print(f"TNEU in Schicht {i} {t_neu} °C")
			

	def Speicher_Entladen(self, Q_Entladen, RL):
		"""
		Parameters:
		Q_Entladen: Leistung die entladen wird in W
		RL: Temperatur des Massenstromes in °C kommend vom Heiz-/Kühlkreis
		"""

		#Zwischenvariablen
		water_data = _Liquid(273 + RL)
		schicht_entladen = self.li_schichten[0]
		schicht_entladen["Masse"] = schicht_entladen["Volumen [m³]"] * water_data["rho"]
		Q_Entladen_step = abs(Q_Entladen) / 10 #pro timestep werden nur 10% der Masse verwendet

		#Neue Temperatur für unterste schicht
		for timestep in range(10):
		#Diese Iterierung wird 10 mal gemacht um einerseits die Durchmischung als auch die Verdrängung der einzelnen Schichten zu simulieren.
		#Neue Temperatur für Ladeschicht
			try:
				m_new = Q_Entladen_step / (water_data["cp"] * 1000 * abs(self.li_schichten[-1]["Temperatur [°C]"]-RL)) * 3600
			except:
				pass
			t_neu_schicht_entladen = ((m_new * RL) + (schicht_entladen["Masse"] * schicht_entladen["Temperatur [°C]"])) / \
							(m_new + schicht_entladen["Masse"])	

			self.li_schichten[0]["Temperatur [°C]"] = t_neu_schicht_entladen

		#Nun werden alle Schichten unter der Ladezone iteriert und die Temperatur angepasst da sich nun Wasser mit unterschiedlicher Temperatur mischt
		#Dabei wird von der Ladeschicht nach unten iteriert				
			for i in range(0, self.anz_schichten-1):

				#Zwischenvariablen definieren zwecks Übersichtlichkeit
				schicht_unten = self.li_schichten[i]
				schicht_oben = self.li_schichten[i+1]
			
				#Zwischenvariable
				schicht_oben["Masse"] = schicht_oben["Volumen [m³]"] * water_data["rho"]

				t_oben_neu = ((m_new * schicht_unten["Temperatur [°C]"]) + (schicht_oben["Masse"] * schicht_oben["Temperatur [°C]"])) / \
							(m_new + schicht_oben["Masse"])
				self.li_schichten[i+1]["Temperatur [°C]"] = t_oben_neu

		if debug == True:
			for i in range(0, self.anz_schichten-1):		
				print(f"Funktion: Speicher_Entladen")
				print(f"Ort: Iterierung nach Speicherentladung")
				print(f"Temperatur Schicht {i} {self.li_schichten[i]['Temperatur [°C]']} °C")
				print(f"Temperatur Schicht {i+1} {self.li_schichten[i+1]['Temperatur [°C]']} °C")
				print(f"Massenstrom zwischen Schicht {i} und Schicht {i+1} ist {m_new*10} kg/h")
				print(f"TNEU in Schicht {i+1} {t_oben_neu} °C")
			
		#Nun werden alle Schichten iteriert und die Temperatur angepasst da sich nun Wasser mit unterschiedlicher Temperatur mischt
		#Dabei wird von der untersten Schicht nach oben iteriert



	def MixSchichten(self):
		"""Diese Funktion mischt die Schichten zu jeder Stunde durch.
		   Dabei wird von einer Durchmischung von 5% des Volumens zwischen den Schichten ausgegangen"""

		for i in range(len(self.li_schichten)-1): #Es gibt immer um 1 weniger Anzahl an kontaktflächen als Anzahl schichten

			water_data = _Liquid(273 + self.li_schichten[i]["Temperatur [°C]"])


			schicht_unten = self.li_schichten[i]
			schicht_unten["Masse"] = schicht_unten["Volumen [m³]"] * water_data["rho"]
			schicht_oben = self.li_schichten[i+1]
			schicht_oben["Masse"] = schicht_oben["Volumen [m³]"] * water_data["rho"]
			m_Mischung = schicht_unten["Masse"] * 0.05

			t_neu_oben = ((m_Mischung * schicht_unten["Temperatur [°C]"]) + (schicht_oben["Masse"] * schicht_oben["Temperatur [°C]"])) / \
					(m_Mischung + schicht_oben["Masse"])

			t_neu_unten = ((m_Mischung * schicht_oben["Temperatur [°C]"]) + (schicht_unten["Masse"] * schicht_unten["Temperatur [°C]"])) / \
					(m_Mischung + schicht_unten["Masse"])
			self.li_schichten[i]["Temperatur [°C]"] = t_neu_unten
			self.li_schichten[i+1]["Temperatur [°C]"] = t_neu_oben


	def ChangeOver(self,m):

		for i in range(-1,len(self.li_schichten)-1): #Es gibt immer um 1 weniger Anzahl an kontaktflächen als Anzahl schichten
			m_Mischung = m
			if i == -1:
				water_data_unten = _Liquid(273 + self.li_schichten[i]["Temperatur [°C]"])
				water_data_oben = _Liquid(273 + self.li_schichten[i+1]["Temperatur [°C]"])

				schicht_unten = self.li_schichten[0]
				schicht_unten["Masse"] = schicht_unten["Volumen [m³]"] * water_data_unten["rho"]
				schicht_oben = self.li_schichten[-1]
				schicht_oben["Masse"] = schicht_oben["Volumen [m³]"] * water_data_oben["rho"]
				
				t_neu_oben = ((m_Mischung * schicht_unten["Temperatur [°C]"]) + (schicht_oben["Masse"] * schicht_oben["Temperatur [°C]"])) / \
						(m_Mischung + schicht_oben["Masse"])

				t_neu_unten = ((m_Mischung * schicht_oben["Temperatur [°C]"]) + (schicht_unten["Masse"] * schicht_unten["Temperatur [°C]"])) / \
						(m_Mischung + schicht_unten["Masse"])
				self.li_schichten[0]["Temperatur [°C]"] = t_neu_unten
			else:
				water_data_unten = _Liquid(273 + self.li_schichten[i]["Temperatur [°C]"])
				water_data_oben = _Liquid(273 + self.li_schichten[i+1]["Temperatur [°C]"])

				schicht_unten = self.li_schichten[i]
				schicht_unten["Masse"] = schicht_unten["Volumen [m³]"] * water_data_unten["rho"]
				schicht_oben = self.li_schichten[i+1]
				schicht_oben["Masse"] = schicht_oben["Volumen [m³]"] * water_data_oben["rho"]

				t_neu_oben = ((m_Mischung * schicht_unten["Temperatur [°C]"]) + (schicht_oben["Masse"] * schicht_oben["Temperatur [°C]"])) / \
						(m_Mischung + schicht_oben["Masse"])

				t_neu_unten = ((m_Mischung * schicht_oben["Temperatur [°C]"]) + (schicht_unten["Masse"] * schicht_unten["Temperatur [°C]"])) / \
						(m_Mischung + schicht_unten["Masse"])
				self.li_schichten[i]["Temperatur [°C]"] = t_neu_unten
				self.li_schichten[i+1]["Temperatur [°C]"] = t_neu_oben




	def UpdateSpeicher(self):
		"""Diese Funktion führt zu jeder Stunde die Verlustrechnung sowie die natürliche Konvektion durch"""
		self.Transmission_total()
		#self.Speicher_Laden(47,50)
		self.Heat_Convection()
		self.MixSchichten()
		#self.Speicher_Entladen(1000,27)


#wärmespeicher = Wärmespeicher(dicke_dämmung = 0.1, lambda_dämmung = 0.04,VL = 35, RL = 30, schichten = 5, ladezone = 3, height = 1, diameter = 0.714)
#print("s")










