

import math
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
debug = True

class Wärmespeicher():

	def __init__(self, dicke_dämmung, lambda_dämmung, VL, RL, schichten, height, ladezone, radius = None, diameter = None):
		#Schichten muss mindesten 1 sein
		#Radius oder Durchmesser müssen definiert sein


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
		dT = abs(self.t_VL - self.t_RL) / self.anz_schichten
		for i in range(self.anz_schichten):
			self.li_schichten.append(Create_Schicht(i,height_schicht))
			self.li_schichten[i]["Temperatur [°C]"] = self.t_RL + dT * i

	def Heat_Transmission_BodenDeckel(self, schicht):
		q_HT_BdDk = (self.lambda_dämmung/self.dicke_dämmung) * schicht["Fläche [m²]"] * (schicht["Temperatur [°C]"] - self.t_umg) #Watt
		q_HT_BdDk = q_HT_BdDk * 3600
		return q_HT_BdDk

	def Heat_Transmission(self, schicht):
		r1 = self.geometry["Radius [m]"] 
		r2 = self.geometry["Radius [m]"] + self.dicke_dämmung	
		q_HT = 2 * (math.pi * schicht["Höhe [m]"] * (schicht["Temperatur [°C]"] - self.t_umg)) / ((1/self.lambda_dämmung)* math.log(r2/r1)) #Watt
		q_HT = q_HT* 3600
		return q_HT
	
	def New_Temperature(self, q_toApply, schicht):
		"""Diese Funktion nimmt eine Schicht und Verlust und berechnet eine neue Temperatur damit"""
		water_data = _Liquid(273 + schicht["Temperatur [°C]"])
		t_new = schicht["Temperatur [°C]"] - q_toApply / (water_data["cp"] * 1000 * water_data["rho"] * schicht["Volumen [m³]"]) 
		return t_new

	def Transmission_total(self):
		"""Diese Funktion berechnet den Transmissionswärmeverlust des Speichers und berechnet anschließend die neue Temperatur"""
		q_bottom = self.Heat_Transmission_BodenDeckel(self.li_schichten[0])
		q_top = self.Heat_Transmission_BodenDeckel(self.li_schichten[-1])

		#Alle schichten durchiterieren
		for i in range(self.anz_schichten):
			

			q_schicht = self.Heat_Transmission(self.li_schichten[i])

			if i == 0:
				q_toApply = q_schicht + q_bottom
				self.li_schichten[i]["Temperatur [°C]"] = self.New_Temperature(q_toApply, self.li_schichten[i])
			elif i == (self.anz_schichten - 1):
				q_toApply = q_schicht + q_top
				self.li_schichten[i]["Temperatur [°C]"] = self.New_Temperature(q_toApply, self.li_schichten[i])
			else:
				q_toApply = q_schicht
				self.li_schichten[i]["Temperatur [°C]"] = self.New_Temperature(q_toApply, self.li_schichten[i])



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
		print("Grashofzahl ist: ", GR)

		#Prandtlzahl berechnen
		PR = (n*cp*1000)/k
		print("Prandtlzahl ist: ", PR)

		#Rayleigh Zahl berechnen
		RA = GR / PR
		print("Rayleighzahl ist: ", RA)

		#Nusselt Zahl berechnen
		#NU = 0.0325 * GR**0.4 #Für Senkrecht ebene Wände Aus TD2 Skriptum
		#print("Nusselt ist: ", NU)
		#Formel von hier: https://studyflix.de/ingenieurwissenschaften/naturliche-konvektion-480
		NU = (0.825 + ((0.387 * RA**(1/6)))/(1 + (0.492 / PR)**(9/16))**(8/27))**2
		print("Nusseltzahl ist: ", NU)

		#Berechnung des Wärmepbergangskoeffizienten alpha
		alpha = (NU * k) / l_char
		return alpha

	def Heat_Convection(self):
		"""Diese Funktion wird nur benötigt wenn es eine untere Schicht gibt, die wärmer ist als eine obere"""

		
		#In Position 0 befindet sich die unterste Schicht. Dieser Loop geht also den Speicher von unten nach oben durch
		#und sucht ob eine untere Schicht wärmer ist als die obere
		for i in range(len(self.li_schichten)-1): #Es gibt ímmer um 1 weniger Anzahl an kontaktflächen als Anzahl schichten

			temp1 = self.li_schichten[i]["Temperatur [°C]"]
			temp2 = self.li_schichten[i+1]["Temperatur [°C]"]

			if temp1 > temp2:

				dT = self.li_schichten[i]["Temperatur [°C]"] - self.li_schichten[i+1]["Temperatur [°C]"]
				alpha = self.Get_Alpha_Convection(self.li_schichten[i],self.li_schichten[i+1])
			
				#Leistung zwischen Schicht berechnen
				Q_schicht = alpha * dT * self.li_schichten[i]["Fläche [m²]"] * 3600

				

				#Massenstrom der sich in einer Stunde durch natürliche Konvektion ergibt
				water_data = _Liquid(273 + self.li_schichten[i]["Temperatur [°C]"])
				m_auftrieb = Q_schicht / (water_data["cp"] * 1000 * (self.li_schichten[i]["Temperatur [°C]"] - self.li_schichten[i+1]["Temperatur [°C]"]))



				if debug == True:
					print(f"Alpha: {alpha} W/m²K")
					print(f"Temperatur Schicht {i} {self.li_schichten[i]['Temperatur [°C]']} °C")
					print(f"Temperatur Schicht {i+1} {self.li_schichten[i+1]['Temperatur [°C]']} °C")
					print(f"Leistung zwischen Schicht {i} und Schicht {i+1} ist {Q_schicht} Watt")
					print("-------------------------------------------------------------------------------")
				#Neue Temperaturen rechnen
				water_data_unten = _Liquid(273 + self.li_schichten[i]["Temperatur [°C]"])
				water_data_oben = _Liquid(273 + self.li_schichten[i+1]["Temperatur [°C]"])

				schicht_unten = self.li_schichten[i]
				schicht_unten["Masse"] = schicht_unten["Volumen [m³]"] * water_data_unten["rho"]
				schicht_oben = self.li_schichten[i+1]
				schicht_oben["Masse"] = schicht_oben["Volumen [m³]"] * water_data_oben["rho"]

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


	def Speicher_Laden(self, Q_laden, VL):

		#Zwischenvariablen
		water_data_laden = _Liquid(273 + self.li_schichten[self.ladezone-1]["Temperatur [°C]"])
		water_data_VL = _Liquid(273 + VL)
		schicht_laden = self.li_schichten[self.ladezone-1]

		#Massenstrom der nach unten gedrückt wird
		m_new = Q_laden / (water_data_VL["cp"] * 1000 * (VL-schicht_laden["Temperatur [°C]"])) * 3600

		#Neue Temperatur für Ladeschicht
		t_neu_schicht_laden = (schicht_laden["Volumen [m³]"] * water_data_laden["rho"] * water_data_laden["cp"] * 1000 * (schicht_laden["Temperatur [°C]"]) + \
					m_new * water_data_VL["cp"] * 1000 * (VL)) /  \
					(schicht_laden["Volumen [m³]"] * water_data_laden["rho"] * water_data_laden["cp"] * 1000 + m_new * water_data_VL["cp"] * 1000)

		self.li_schichten[self.ladezone-1]["Temperatur [°C]"] = t_neu_schicht_laden

		#Nun werden alle Schichten unter der Ladezone iteriert und die Temperatur angepasst da sich nun Wasser mit unterschiedlicher Temperatur mischt
		#Dabei wird von der untersten Schicht nach oben iteriert
		for i in range(self.ladezone - 1, 0, -1 ):

			#Zwischenvariablen definieren zwecks Übersichtlichkeit
			schicht_unten = self.li_schichten[i-1]
			schicht_oben = self.li_schichten[i]

			#Wasserdaten definieren
			water_data_base = _Liquid(273 + schicht_unten["Temperatur [°C]"])
			water_data_new = _Liquid(273 + schicht_oben["Temperatur [°C]"])
			
			#Zwischenvariable
			schicht_unten["Masse"] = schicht_unten["Volumen [m³]"] * water_data_base["rho"]


			t_neu = (schicht_unten["Masse"] * water_data_base["cp"] * 1000 * schicht_unten["Temperatur [°C]"] + \
					m_new * water_data_new["cp"] * 1000 * schicht_oben["Temperatur [°C]"]) /  \
					(schicht_unten["Masse"] * water_data_base["cp"] * 1000 + m_new * water_data_new["cp"] * 1000)
			
			print(f"Temperatur Schicht {i+1} {self.li_schichten[i]['Temperatur [°C]']} °C")
			print(f"Temperatur Schicht {i} {self.li_schichten[i-1]['Temperatur [°C]']} °C")
			print(f"Massenstrom zwischen Schicht {i} und Schicht {i+1} ist {m_new} kg/h")
			print(f"TNEU in Schicht {i} {t_neu} °C")
			self.li_schichten[i-1]["Temperatur [°C]"] = t_neu

	def Speicher_Entladen(self, Q_Entladen, RL):

		#Es wird gerade immer aus der obersten Schicht Wasser entnommen
		water_data = _Liquid(273 + self.li_schichten[0]["Temperatur [°C]"])

		#Massenstrom der entnommen wird
		m_new = (Q_Entladen / (water_data["cp"] * 1000 * (self.li_schichten[-1]["Temperatur [°C]"] - RL))) * 3600

		#Neue Temperatur für unterste schicht
		water_data_zero = _Liquid(273 + self.li_schichten[-1]["Temperatur [°C]"])
		water_data_RL = _Liquid(273 + RL)
		t_neu_schicht_0 = (self.li_schichten[-1]["Volumen [m³]"] * water_data_zero["rho"] * water_data_zero["cp"] * 1000 * (self.li_schichten[-1]["Temperatur [°C]"]) + \
					m_new * water_data_RL["cp"] * 1000 * (RL)) /  \
					(self.li_schichten[-1]["Volumen [m³]"] * water_data_zero["rho"] * water_data_zero["cp"] * 1000 + m_new * water_data_RL["cp"] * 1000)
		#Neue Temperatur zuweisen
		self.li_schichten[-1]["Temperatur [°C]"] = t_neu_schicht_0
		#Nun werden alle Schichten iteriert und die Temperatur angepasst da sich nun Wasser mit unterschiedlicher Temperatur mischt
		#Dabei wird von der untersten Schicht nach oben iteriert
		for i in range(self.anz_schichten - 1, 0, -1 ):

			#Zwischenvariablen definieren zwecks Übersichtlichkeit
			schicht_unten = self.li_schichten[i]
			schicht_oben = self.li_schichten[i-1]

			#Wasserdaten definieren
			water_data_base = _Liquid(273 + schicht_unten["Temperatur [°C]"])
			water_data_new = _Liquid(273 + schicht_oben["Temperatur [°C]"])
			
			#Zwischenvariable
			schicht_oben["Masse"] = schicht_oben["Volumen [m³]"] * water_data_base["rho"]

			#Neue Temperatur für obere Schicht berechnen
			#Formel von hier: https://rechneronline.de/chemie-rechner/temperaturen-mischen.php
			t_neu = (schicht_oben["Masse"] * water_data_new["cp"] * 1000 * schicht_oben["Temperatur [°C]"] + \
					m_new * water_data_base["cp"] * 1000 * schicht_unten["Temperatur [°C]"]) /  \
					(schicht_oben["Masse"] * water_data_new["cp"] * 1000 + m_new * water_data_base["cp"] * 1000)
			
			print(f"Temperatur Schicht {i+1} {schicht_unten['Temperatur [°C]']} °C")
			print(f"Temperatur Schicht {i} {schicht_oben['Temperatur [°C]']} °C")
			print(f"Massenstrom zwischen Schicht {i} und Schicht {i+1} ist {m_new} kg/h")
			print(f"TNEU in Schicht {i+1} {t_neu} °C")
			#Neue Temperatur zuweisen
			self.li_schichten[i-1]["Temperatur [°C]"] = t_neu

	






wärmespeicher = Wärmespeicher(dicke_dämmung = 0.1, lambda_dämmung = 0.04,VL = 35, RL = 30, schichten = 5, height = 2, diameter = 0.5, ladezone = 3)


for i in range(1):
	wärmespeicher.Transmission_total()
	wärmespeicher.Speicher_Laden(1000, VL = 35)
	wärmespeicher.Heat_Convection()
	
	#wärmespeicher.Speicher_Entladen(1000, RL = 5)
















