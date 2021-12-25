
import numpy as np

class cla_PV_Anlage():
    def __init__(self, var_PV_kWp,var_PV_EK):
        self.PV = var_PV_kWp #kW
        self.PV_EK = self.PV * var_PV_EK / 1000 #kW




obj_PV_Anlage = cla_PV_Anlage(8,np.genfromtxt("./EMS-Backend/Data/PV_1kWp.csv"))

print("")