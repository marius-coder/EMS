# -*- coding: latin-1 -*-

import pybind11module
import numpy as np
from timeit import default_timer as timer
data_Sim = {
	"Punkte X" : 50,
	"Punkte Y" : 50,
	"Laenge Punkt [m]" : 0.5,
	}
data_Pixel = {
	"Bohrtiefe" : 100,
	"Anzahl_Sonden" : 49,
	"Abstand_Sonden" : 10,
	"WM_spez" : 2
	}
data_Boden = {
	"Temperatur" : 6,
	"cp" : 1000,
	"rho" : 2600,
	}

start = timer()
da = pybind11module.ErdSim(data_Sim, data_Pixel, data_Boden)
da.Simulate(1000000)
end = timer()
print(end - start)
#test = np.zeros([52,52], dtype=float)
test = da.GetTemperatures()
#print(da.pixelArrayTemperatures)
print(test)
