# -*- coding: latin-1 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Gebäude.Gebäude import Ui_Gebäude
from Strom.Strom import Ui_Strombedarf
from Warmwasser.Warmwasser import Ui_Warmwasser
from PV_Batterie.PV_Batterie import Ui_PV_Batterie


class Ui_Main(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(278, 324)
        self.pushButton_Simulate = QtWidgets.QPushButton(Form)
        self.pushButton_Simulate.setGeometry(QtCore.QRect(150, 240, 75, 23))
        self.pushButton_Simulate.setObjectName("pushButton_Simulate")
        self.pushButton_Simulate.setText("Simulate!")

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

        self.pushButton_openWärmepumpe = QtWidgets.QPushButton(Form)
        self.pushButton_openWärmepumpe.setGeometry(QtCore.QRect(40, 160, 75, 23))
        self.pushButton_openWärmepumpe.setObjectName("pushButton_openWärmepumpe")
        self.pushButton_openWärmepumpe.setText("Wärmepumpe")

        self.pushButton_openErdwärme = QtWidgets.QPushButton(Form)
        self.pushButton_openErdwärme.setGeometry(QtCore.QRect(40, 120, 75, 23))
        self.pushButton_openErdwärme.setObjectName("pushButton_openErdwärme")
        self.pushButton_openErdwärme.setText("Erdwärme")

        self.pushButton_openWarmwasser = QtWidgets.QPushButton(Form)
        self.pushButton_openWarmwasser.setGeometry(QtCore.QRect(40, 80, 75, 23))
        self.pushButton_openWarmwasser.setObjectName("pushButton_openWarmwasser")
        self.pushButton_openWarmwasser.setText("Warmwasser")
        self.pushButton_openWarmwasser.clicked.connect(self.OpenWarmwasser)

        self.pushButton_openKosten = QtWidgets.QPushButton(Form)
        self.pushButton_openKosten.setGeometry(QtCore.QRect(40, 240, 75, 23))
        self.pushButton_openKosten.setObjectName("pushButton_openKosten")
        self.pushButton_openKosten.setText("Kosten")

        self.pushButton_Gebäude = QtWidgets.QPushButton(Form)
        self.pushButton_Gebäude.setGeometry(QtCore.QRect(40, 40, 75, 23))
        self.pushButton_Gebäude.setObjectName("pushButton_Gebäude")
        self.pushButton_Gebäude.setText("Gebäude")
        self.pushButton_Gebäude.clicked.connect(self.OpenGebaude)




    def OpenGebaude(self):
        self.Gebäude = Ui_Gebäude()
        self.Gebäude.show()

    def OpenStrombedarf(self):
        self.Strombedarf = Ui_Strombedarf()
        self.Strombedarf.show()

    def OpenWarmwasser(self):
        self.Warmwasser = Ui_Warmwasser()
        self.Warmwasser.show()

    def OpenPV_Batterie(self):
        self.PV_Batterie = Ui_PV_Batterie()
        self.PV_Batterie.show()



            
       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
main = MainWindow()
w = Ui_Main()
w.setupUi(main)
main.show()
app.exec()