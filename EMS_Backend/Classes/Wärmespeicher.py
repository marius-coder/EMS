

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

class Wärmespeicher():

	def __init__(self, dicke_dämmung, lambda_dämmung, VL, RL, schichten, height, radius = None, diameter = None):
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
		self.anz_schichten = schichten
		height_schicht = height / self.anz_schichten
		def Create_Schicht(id):
			schicht = {
			"ID" : id,
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
			self.li_schichten.append(Create_Schicht(i))
			self.li_schichten[i]["Temperatur [°C]"] = self.t_VL - dT * i

	def Heat_Transmission_BodenDeckel(self, schicht):
		q_HT_BdDk = (self.lambda_dämmung/self.dicke_dämmung) * schicht["Fläche"] * (schicht["Temperatur [°C]"] - t_umg) #Watt
		return q_HT_BdDk

	def Heat_Transmission(self, schicht):
		t_umg = 20 #Annahme dass der Technikraum immer 20°C hat.
		r1 = self.geometry["Radius [m]"] 
		r2 = self.geometry["Radius [m]"] + self.dicke_dämmung	
		q_HT = 2 * (math.pi * self.schicht["Höhe [m]"] * (schicht["Temperatur [°C]"] - t_umg)) / ((1/self.lambda_dämmung)* math.log(r2/r1)) #Watt
		return q_HT


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

		#Reynoldszahl berechnen
		RE = (w * l_char) / v
		print("Reynoldszahl ist: ", RE)
		
	
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
		NU = (0.825 + ((0.387 * RA**(1/6)))/(1 + (0.492 / PR)**(9/16))**(8/27))**2
		print("Nusseltzahl ist: ", NU)

		#Berechnung des Wärmepbergangskoeffizienten alpha
		alpha = (NU * k) / l_char
		return alpha

	def Heat_Convection(self):



		for i in range(len(self.li_schichten)-1): #Es gibt ímmer um 1 weniger Anzahl an kontaktflächen als Anzahl schichten
			dT = self.li_schichten[i]["Temperatur [°C]"] - self.li_schichten[i+1]["Temperatur [°C]"]
			alpha = self.Get_Alpha_Convection(self.li_schichten[i],self.li_schichten[i+1])

			print(f"Alpha: {alpha} W/m²K")
			print(f"Temperatur Schicht {i} {self.li_schichten[i]['Temperatur [°C]']} °C")
			print(f"Temperatur Schicht {i+1} {self.li_schichten[i+1]['Temperatur [°C]']} °C")

			Q_schicht = alpha * dT * self.li_schichten[i]["Fläche [m²]"]

			print(f"Leistung zwischen Schicht {i} und Schicht {i+1} ist {Q_schicht} Watt")
			print("-------------------------------------------------------------------------------")

wärmespeicher = Wärmespeicher(dicke_dämmung = 0.1, lambda_dämmung = 0.04,VL = 60, RL = 40, schichten = 5, height = 10, diameter = 3)
wärmespeicher.Heat_Convection()




















