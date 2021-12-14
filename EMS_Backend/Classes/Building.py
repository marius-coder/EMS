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

        self.wand = {"Fläche" : self.df_thermal_hull.iloc[0,1],
                     "U-Wert" : self.df_thermal_hull["U-Wert"][0],
                     "f_T" : self.df_thermal_hull["Temperatur-Korrekturfaktor"][0],}
        self.wand["LT"] = self.calc_LT("wand")

        self.dach = {"Fläche" : self.df_thermal_hull.iloc[1,1],
                     "U-Wert": self.df_thermal_hull["U-Wert"][1],
                     "f_T": self.df_thermal_hull["Temperatur-Korrekturfaktor"][1]}
        self.dach["LT"] = self.calc_LT("dach")

        self.fußboden = {"Fläche" : self.df_thermal_hull.iloc[2,1],
                     "U-Wert": self.df_thermal_hull["U-Wert"][2],
                     "f_T": self.df_thermal_hull["Temperatur-Korrekturfaktor"][2]}
        self.fußboden["LT"] = self.calc_LT("fußboden")

        self.volumen = self.gfa * self.net_storey_height
        self.LT_WandGesamt = 0
        

    def calc_LT(self, Bauteil:str):
        try:
            return getattr(self, Bauteil)["Fläche"] * getattr(self, Bauteil)["U-Wert"] * getattr(self, Bauteil)["f_T"]

        except:
            return getattr(self, Bauteil)["Fläche"] * getattr(self, Bauteil)["U-Wert"]

    def insert_windows(self, u_f:float, ff_anteil:float):
        self.window = {"Fläche" : self.wand["Fläche"] * ff_anteil,
                       "U-Wert" : u_f,
                       "ff_anteil" : ff_anteil}

        self.wand = {"Fläche" : self.wand["Fläche"] - self.window["Fläche"],
                     "U-Wert" : self.df_thermal_hull["U-Wert"][0],
                     "f_T" : self.df_thermal_hull["Temperatur-Korrekturfaktor"][0]}

        self.wand_gesamt = {"Fläche" : self.wand["Fläche"] + self.window["Fläche"],
                       "U-Wert" : (u_f * self.window["Fläche"] + self.wand["U-Wert"] * self.wand["Fläche"]) /\
                           (self.window["Fläche"] + self.wand["Fläche"])}
        