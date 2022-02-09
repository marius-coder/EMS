# -*- coding: latin-1 -*-
import numpy as np

class cla_PV_Anlage():
    def __init__(self, var_PV_kWp,var_PV_EK):
        self.PV = var_PV_kWp #kW
        self.PV_EK = self.PV * var_PV_EK #kW



