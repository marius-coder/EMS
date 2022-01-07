# -*- coding: latin-1 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import importlib
Sim = importlib.import_module("EMS-Backend.Classes.Simulation")

from Geb�ude.Geb�ude import Ui_Geb�ude
from Strom.Strom import Ui_Strombedarf
from Warmwasser.Warmwasser import Ui_Warmwasser
from PV_Batterie.PV_Batterie import Ui_PV_Batterie
from Erdw�rme.Erdw�rme import Ui_Erdw�rme


class Ui_Main(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(278, 324)
        self.pushButton_Simulate = QtWidgets.QPushButton(Form)
        self.pushButton_Simulate.setGeometry(QtCore.QRect(150, 240, 75, 23))
        self.pushButton_Simulate.setObjectName("pushButton_Simulate")
        self.pushButton_Simulate.setText("Simulate!")        
        self.pushButton_Simulate.clicked.connect(self.Simulate)


        self.pushButton_openSpeicher = QtWidgets.QPushButton(Form)
        self.pushButton_openSpeicher.setGeometry(QtCore.QRect(40, 200, 75, 23))
        self.pushButton_openSpeicher.setObjectName("pushButton_openSpeicher")
        self.pushButton_openSpeicher.setText("Speicher")

        self.pushButton_openStrombedarf = QtWidgets.QPushButton(Form)
        self.pushButton_openStrombedarf.setGeometry(QtCore.QRect(160, 40, 75, 23))
        self.pushButton_openStrombedarf.setObjectName("pushButton_openStrombedarf")
        self.pushButton_openStrombedarf.setText("Strombedarf")
        self.pushButton_openStrombedarf.clicked.connect(self.OpenStrombedarf)

        self.pushButton_openPVBatterie = QtWidgets.QPushButton(Form)
        self.pushButton_openPVBatterie.setGeometry(QtCore.QRect(160, 80, 75, 23))
        self.pushButton_openPVBatterie.setObjectName("pushButton_openPVBatterie")
        self.pushButton_openPVBatterie.setText("PV/Batterie")
        self.pushButton_openPVBatterie.clicked.connect(self.OpenPV_Batterie)

        self.pushButton_openW�rmepumpe = QtWidgets.QPushButton(Form)
        self.pushButton_openW�rmepumpe.setGeometry(QtCore.QRect(40, 160, 75, 23))
        self.pushButton_openW�rmepumpe.setObjectName("pushButton_openW�rmepumpe")
        self.pushButton_openW�rmepumpe.setText("W�rmepumpe")

        self.pushButton_openErdw�rme = QtWidgets.QPushButton(Form)
        self.pushButton_openErdw�rme.setGeometry(QtCore.QRect(40, 120, 75, 23))
        self.pushButton_openErdw�rme.setObjectName("pushButton_openErdw�rme")
        self.pushButton_openErdw�rme.setText("Erdw�rme")
        self.pushButton_openErdw�rme.clicked.connect(self.OpenErdwarme)

        self.pushButton_openWarmwasser = QtWidgets.QPushButton(Form)
        self.pushButton_openWarmwasser.setGeometry(QtCore.QRect(40, 80, 75, 23))
        self.pushButton_openWarmwasser.setObjectName("pushButton_openWarmwasser")
        self.pushButton_openWarmwasser.setText("Warmwasser")
        self.pushButton_openWarmwasser.clicked.connect(self.OpenWarmwasser)

        self.pushButton_openKosten = QtWidgets.QPushButton(Form)
        self.pushButton_openKosten.setGeometry(QtCore.QRect(40, 240, 75, 23))
        self.pushButton_openKosten.setObjectName("pushButton_openKosten")
        self.pushButton_openKosten.setText("Kosten")

        self.pushButton_Geb�ude = QtWidgets.QPushButton(Form)
        self.pushButton_Geb�ude.setGeometry(QtCore.QRect(40, 40, 75, 23))
        self.pushButton_Geb�ude.setObjectName("pushButton_Geb�ude")
        self.pushButton_Geb�ude.setText("Geb�ude")
        self.pushButton_Geb�ude.clicked.connect(self.OpenGebaude)


    def OpenErdwarme(self):
        self.Erd�rme = Ui_Erdw�rme()
        self.Erd�rme.show()

    def OpenGebaude(self):
        self.Geb�ude = Ui_Geb�ude()
        self.Geb�ude.show()

    def OpenStrombedarf(self):
        self.Strombedarf = Ui_Strombedarf()
        self.Strombedarf.show()

    def OpenWarmwasser(self):
        self.Warmwasser = Ui_Warmwasser()
        self.Warmwasser.show()

    def OpenPV_Batterie(self):
        self.PV_Batterie = Ui_PV_Batterie()
        self.PV_Batterie.show()

    def Simulate(self):
        model = Sim.Simulation(b_geothermal = False)
        model.Setup_Simulation()
        model.Simulate()
            
       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
main = MainWindow()
w = Ui_Main()
w.setupUi(main)
main.show()
app.exec()