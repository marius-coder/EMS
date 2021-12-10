#!/usr/local/bin/python
# -*- coding: <utf-8> -*-

import pandas as pd
import matplotlib as plt
import numpy as np

class Building():


    def __init__(self, path:str):
        self.df_params = pd.read_excel(path,sheet_name="params")
        self.df_thermal_hull = pd.read_excel(path,sheet_name="thermal_hull")
        self.gfa = self.df_params.iloc[0,1]
        self.heat_capacity = self.df_params["Value"][2]
        self.net_storey_height = self.df_params["Value"][3]

        self.wand = {"Fl�che" : self.df_thermal_hull.iloc[0,1],
                     "U-Wert" : self.df_thermal_hull["U-Wert"][0],
                     "f_T" : self.df_thermal_hull["Temperatur-Korrekturfaktor"][0],}
        self.wand["LT"] = self.LT("wand")

        self.dach = {"Fl�che" : self.df_thermal_hull.iloc[1,1],
                     "U-Wert": self.df_thermal_hull["U-Wert"][1],
                     "f_T": self.df_thermal_hull["Temperatur-Korrekturfaktor"][1]}
        self.dach["LT"] = self.LT("dach")

        self.fussboden = {"Fl�che" : self.df_thermal_hull.iloc[2,1],
                     "U-Wert": self.df_thermal_hull["U-Wert"][2],
                     "f_T": self.df_thermal_hull["Temperatur-Korrekturfaktor"][2]}
        self.fussboden["LT"] = self.LT("fussboden")

        self.volumen = self.gfa * self.net_storey_height

    def LT(self, Bauteil:str):
        try:
            return getattr(self, Bauteil)["Fl�che"] * getattr(self, Bauteil)["U-Wert"] * getattr(self, Bauteil)["f_T"]

        except:
            return getattr(self, Bauteil)["Fl�che"] * getattr(self, Bauteil)["U-Wert"]

    def insert_windows(self, u_f:float, ff_anteil:float):
        self.window = {"Fl�che" : self.wand["Fl�che"] * ff_anteil,
                       "U-Wert" : u_f,
                       "ff_anteil" : ff_anteil}

        self.wand = {"Fl�che" : self.wand["Fl�che"] - self.window["Fl�che"],
                     "U-Wert" : self.df_thermal_hull["U-Wert"][0],
                     "f_T" : self.df_thermal_hull["Temperatur-Korrekturfaktor"][0]}

        self.wand_gesamt = {"Fl�che" : self.wand["Fl�che"] + self.window["Fl�che"],
                       "U-Wert" : (u_f * self.window["Fl�che"] + self.wand["U-Wert"] * self.wand["Fl�che"]) /\
                           (self.window["Fl�che"] + self.wand["Fl�che"])}
        
building = Building("./data/building.xlsx")
building_oib = Building("./data/building_oib_16linie.xlsx")
building_ph = Building("./data/building_ph.xlsx")

building.insert_windows(1.7, 0.3)

print(building.LT("wand_gesamt"))

print(building.gfa)
print(building_ph.df_params)

