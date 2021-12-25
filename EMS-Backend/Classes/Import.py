
class Import():
	"""Diese Klasse importiert die verschiedenen Eingaben aus dem GUI
	Jetzt gerade werden die Input Parameter noch im Code selbst eingegeben
	"""

	def __init__(self):
		pass
		#self.Import_Geothermal()


	def Import_Geothermal(self):
		self.input_GeoData = {"Adresse" : "Höchstädtplatz 6, 1200 Wien, Österreich",
								"Bohrtiefe" : 150,
								"Anzahl_Sonden" : 5}



	def Import_WarmWater(self, data):

		profileName = data[0]
		values = data[1:25]
		ww_values = data[25:]    
		
   

		self.input_Warmwater = {
			"Profilname" : profileName,
			"WW-Verbrauch [%]" : values,
			"Verbrauchsart" : ww_values
			}





importGUI = Import()