# -*- coding: <utf-8> -*-

import pybind11module
data_Sim = {
	"Punkte X" : 3,
	"Punkte Y" : 3,
	"Länge Punkt [m]" : 0.5,
	"Länge Sonde [m]" : 0.2}

data_Boden = {
	"Temperatur" : 6,
	"cp" : 1000,
	"rho" : 2600}

data_Pixel = {}

da = pybind11module.ErdSim(data_Sim, data_Pixel, data_Boden)

print(da.dichte)