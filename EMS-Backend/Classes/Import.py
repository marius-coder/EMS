
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
		self.input_Warmwater = data

	def Import_Strombedarf(self, data):
		self.input_Strombedarf = data

	def Import_PV_Batterie(self, data):
		self.input_PV_Batterie = data
		



importGUI = Import()
#importGUI.Import_Geothermal()