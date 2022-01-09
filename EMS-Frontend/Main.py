# -*- coding: latin-1 -*-
import sys
from bokeh.plotting import figure, show
import numpy as np
import pandas as pd
import csv

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import importlib
Sim = importlib.import_module("EMS-Backend.Classes.Simulation")

from Gebäude.Gebäude import Ui_Gebäude
from Strom.Strom import Ui_Strombedarf
from Warmwasser.Warmwasser import Ui_Warmwasser
from PV_Batterie.PV_Batterie import Ui_PV_Batterie
from Erdwärme.Erdwärme import Ui_Erdwärme


class Ui_Main(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 230)

        
        self.pushButton_Gebäude = QtWidgets.QPushButton(Form)
        self.pushButton_Gebäude.setGeometry(QtCore.QRect(20, 20, 75, 23))
        self.pushButton_Gebäude.setObjectName("pushButton_Gebäude")
        self.pushButton_Gebäude.setText("Gebäude")
        self.pushButton_Gebäude.clicked.connect(self.OpenGebaude)
        self.lineEdit_Gebäude = QtWidgets.QLineEdit(Form)
        self.lineEdit_Gebäude.setGeometry(QtCore.QRect(110, 20, 130, 20))
        self.lineEdit_Gebäude.setReadOnly(True)
        self.lineEdit_Gebäude.setObjectName("lineEdit_Gebäude")


        self.pushButton_openWarmwasser = QtWidgets.QPushButton(Form)
        self.pushButton_openWarmwasser.setGeometry(QtCore.QRect(20, 60, 75, 23))
        self.pushButton_openWarmwasser.setObjectName("pushButton_openWarmwasser")
        self.pushButton_openWarmwasser.setText("Warmwasser")
        self.pushButton_openWarmwasser.clicked.connect(self.OpenWarmwasser)
        self.lineEdit_Warmwasser = QtWidgets.QLineEdit(Form)
        self.lineEdit_Warmwasser.setGeometry(QtCore.QRect(110, 60, 130, 20))
        self.lineEdit_Warmwasser.setReadOnly(True)
        self.lineEdit_Warmwasser.setObjectName("lineEdit_Warmwasser")


        self.pushButton_openErdwärme = QtWidgets.QPushButton(Form)
        self.pushButton_openErdwärme.setGeometry(QtCore.QRect(20, 100, 75, 23))
        self.pushButton_openErdwärme.setObjectName("pushButton_openErdwärme")
        self.pushButton_openErdwärme.setText("Erdwärme")
        self.pushButton_openErdwärme.clicked.connect(self.OpenErdwarme)
        self.lineEdit_Erdwärme = QtWidgets.QLineEdit(Form)
        self.lineEdit_Erdwärme.setGeometry(QtCore.QRect(110, 100, 130, 20))
        self.lineEdit_Erdwärme.setReadOnly(True)
        self.lineEdit_Erdwärme.setObjectName("lineEdit_Erdwärme")


        self.pushButton_openWärmepumpe = QtWidgets.QPushButton(Form)
        self.pushButton_openWärmepumpe.setGeometry(QtCore.QRect(20, 140, 75, 23))
        self.pushButton_openWärmepumpe.setObjectName("pushButton_openWärmepumpe")
        self.pushButton_openWärmepumpe.setText("Wärmepumpe")
        self.lineEdit_Wärmepumpe = QtWidgets.QLineEdit(Form)
        self.lineEdit_Wärmepumpe.setGeometry(QtCore.QRect(110, 140, 130, 20))
        self.lineEdit_Wärmepumpe.setReadOnly(True)
        self.lineEdit_Wärmepumpe.setObjectName("lineEdit_Wärmepumpe")


        self.pushButton_openSpeicher = QtWidgets.QPushButton(Form)
        self.pushButton_openSpeicher.setGeometry(QtCore.QRect(20, 180, 75, 23))
        self.pushButton_openSpeicher.setObjectName("pushButton_openSpeicher")
        self.pushButton_openSpeicher.setText("Speicher")
        self.lineEdit_Speicher = QtWidgets.QLineEdit(Form)
        self.lineEdit_Speicher.setGeometry(QtCore.QRect(110, 180, 130, 20))
        self.lineEdit_Speicher.setReadOnly(True)
        self.lineEdit_Speicher.setObjectName("lineEdit_Speicher")

        self.pushButton_openStrombedarf = QtWidgets.QPushButton(Form)
        self.pushButton_openStrombedarf.setGeometry(QtCore.QRect(270, 20, 75, 23))
        self.pushButton_openStrombedarf.setObjectName("pushButton_openStrombedarf")
        self.pushButton_openStrombedarf.setText("Strombedarf")
        self.pushButton_openStrombedarf.clicked.connect(self.OpenStrombedarf)
        self.lineEdit_Strombedarf = QtWidgets.QLineEdit(Form)
        self.lineEdit_Strombedarf.setGeometry(QtCore.QRect(360, 20, 130, 20))
        self.lineEdit_Strombedarf.setReadOnly(True)
        self.lineEdit_Strombedarf.setObjectName("lineEdit_Strombedarf")


        self.pushButton_openPVBatterie = QtWidgets.QPushButton(Form)
        self.pushButton_openPVBatterie.setGeometry(QtCore.QRect(270, 60, 75, 23))
        self.pushButton_openPVBatterie.setObjectName("pushButton_openPVBatterie")
        self.pushButton_openPVBatterie.setText("PV/Batterie")
        self.pushButton_openPVBatterie.clicked.connect(self.OpenPV_Batterie)
        self.lineEdit_PVBatterie = QtWidgets.QLineEdit(Form)
        self.lineEdit_PVBatterie.setGeometry(QtCore.QRect(360, 60, 130, 20))
        self.lineEdit_PVBatterie.setReadOnly(True)
        self.lineEdit_PVBatterie.setObjectName("lineEdit_PVBatterie")


        self.pushButton_openEnergiedaten = QtWidgets.QPushButton(Form)
        self.pushButton_openEnergiedaten.setGeometry(QtCore.QRect(270, 100, 75, 23))
        self.pushButton_openEnergiedaten.setObjectName("pushButton_openEnergiedaten")
        self.pushButton_openEnergiedaten.setText("Energiedaten")


        self.pushButton_openKosten = QtWidgets.QPushButton(Form)
        self.pushButton_openKosten.setGeometry(QtCore.QRect(270, 140, 75, 23))
        self.pushButton_openKosten.setObjectName("pushButton_openKosten")
        self.pushButton_openKosten.setText("Kosten")


        self.pushButton_Simulate = QtWidgets.QPushButton(Form)
        self.pushButton_Simulate.setGeometry(QtCore.QRect(270, 180, 75, 23))
        self.pushButton_Simulate.setObjectName("pushButton_Simulate")
        self.pushButton_Simulate.setText("Simulate!")        
        self.pushButton_Simulate.clicked.connect(self.Simulate)


        #Vertikale Linie
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(510, 0, 16, 300))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")


        #Profil Stuff (Laden,Speichern,löschen etc.)
        self.label_Profilauswahl = QtWidgets.QLabel(Form)
        self.label_Profilauswahl.setGeometry(QtCore.QRect(530, 5, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_Profilauswahl.setFont(font)
        self.label_Profilauswahl.setScaledContents(False)
        self.label_Profilauswahl.setObjectName("label_Profilauswahl")
        self.label_Profilauswahl.setText("Profilauswahl")
        self.pushButton_SaveProfile = QtWidgets.QPushButton(Form)
        self.pushButton_SaveProfile.setGeometry(QtCore.QRect(650, 60, 75, 23))
        self.pushButton_SaveProfile.setObjectName("pushButton_SaveProfile")
        self.pushButton_SaveProfile.setText("Save Profile")
        self.comboBox_SelectProfile = QtWidgets.QComboBox(Form)
        self.comboBox_SelectProfile.setGeometry(QtCore.QRect(530, 110, 111, 22))
        self.comboBox_SelectProfile.setObjectName("comboBox_SelectProfile")
        self.lineEdit_Profil = QtWidgets.QLineEdit(Form)
        self.lineEdit_Profil.setGeometry(QtCore.QRect(530, 60, 113, 20))
        self.lineEdit_Profil.setObjectName("lineEdit")
        self.label_ProfilEingabe = QtWidgets.QLabel(Form)
        self.label_ProfilEingabe.setGeometry(QtCore.QRect(530, 40, 111, 16))
        self.label_ProfilEingabe.setWordWrap(True)
        self.label_ProfilEingabe.setObjectName("label_ProfilEingabe")
        self.label_ProfilEingabe.setText("Eingabe Profilname")
        self.pushButton_DeleteProfile = QtWidgets.QPushButton(Form)
        self.pushButton_DeleteProfile.setGeometry(QtCore.QRect(650, 110, 75, 23))
        self.pushButton_DeleteProfile.setObjectName("pushButton_DeleteProfile")
        self.pushButton_DeleteProfile.setText("Delete Profile")
        self.label_ProfilAuswahl = QtWidgets.QLabel(Form)
        self.label_ProfilAuswahl.setGeometry(QtCore.QRect(530, 90, 111, 16))
        self.label_ProfilAuswahl.setWordWrap(True)
        self.label_ProfilAuswahl.setObjectName("label_ProfilAuswahl")
        self.label_ProfilAuswahl.setText("Auswahl Profil")

        self.li_inputWidgets = [self.lineEdit_Gebäude,self.lineEdit_Warmwasser,self.lineEdit_Erdwärme,
                           self.lineEdit_Wärmepumpe,self.lineEdit_Speicher,self.lineEdit_Strombedarf,self.lineEdit_PVBatterie]

        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./EMS-Frontend/data/Simulation_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.addItems(names)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)

    def OpenErdwarme(self):
        self.Erdärme = Ui_Erdwärme()
        self.Erdärme.show()

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

    def Simulate(self):
        model = Sim.Simulation(b_geothermal = False)
        model.Setup_Simulation()
        model.Simulate()
        x = np.linspace(0,8760,8760)
        y = model.ti
        p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')

        p.line(x, y, legend_label="Temp.", line_width=2)
        show(p)
            

    def SaveProfile(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Simulation_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        
        name = self.lineEdit_Profil.text()
        #Wenn nichts im Lineedit steht oder kein Radiobutton ausgewählt ist wird das Profil nicht gespeichert
        if name == "":
            return
   
        li_toSave = []
        li_toSave.append(name)

        for widget in self.li_inputWidgets:            
                li_toSave.append(widget.text())

        #Save Warmwasser Nutzungsmischung
        li_toSave_WW = []
        li_toSave_WW.append(name)
        li_toSave_WW.append(self.Warmwasser.graphWindow.lineEdit_Fläche.text())
        for column in range(self.Warmwasser.graphWindow.table.columnCount()): 
            columnString = ""
            #Items aus der Tabelle
            for row in range(self.Warmwasser.graphWindow.table.rowCount()):
                columnString += self.Warmwasser.graphWindow.table.item(row, column).text() + "----"
            li_toSave_WW.append(columnString)

        columnString = ""
        for row in range(self.Warmwasser.graphWindow.table.rowCount()):
            #Stündliches Profil
            for item in self.Warmwasser.graphWindow.y_hour[row]:
                columnString += str(item) + "----"
            #Monatliches Profil
            for item in self.Warmwasser.graphWindow.y_month[row]:
                columnString += str(item) + "----"
            columnString = columnString[:-4]
            li_toSave_WW.append(columnString)

        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/Warmwasser_Nutzungsmischungen.csv",'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave_WW)

        #Save Strombedarf Nutzungsmischung
        li_toSave_Strom = []
        li_toSave_Strom.append(name)
        li_toSave_Strom.append(self.Strombedarf.graphWindow.lineEdit_Fläche.text())
        for column in range(self.Strombedarf.graphWindow.table.columnCount()): 
            columnString = ""
            #Items aus der Tabelle
            for row in range(self.Strombedarf.graphWindow.table.rowCount()):
                columnString += self.Strombedarf.graphWindow.table.item(row, column).text() + "----"
            li_toSave_Strom.append(columnString)

        columnString = ""
        for row in range(self.Warmwasser.graphWindow.table.rowCount()):    
            #Stündliches Profil
            for item in self.Strombedarf.graphWindow.y_hour[row]:
                columnString += str(item) + "----"
            #Monatliches Profil
            for item in self.Strombedarf.graphWindow.y_month[row]:
                columnString += str(item) + "----"
            columnString = columnString[:-4]
            li_toSave_Strom.append(columnString)

        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/Strombedarf_Nutzungsmischungen.csv",'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave_Strom)


        #Kontrolle ob ein Profil mit diesem Namen bereits existiert
        if name in names:
            self.DeleteProfile()
        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/Simulation_Profile.csv",'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave)
        self.UpdateProfiles()
   
    def DeleteProfile(self):
        name = self.comboBox_SelectProfile.currentText()
        def del_Profile(names):
            for name in names:
                with open(f"./EMS-Frontend/data/{name}.csv", 'r', encoding="utf-8") as inp:
                    lines = inp.readlines()
                with open(f"./EMS-Frontend/data/{name}.csv",'w', newline='', encoding="utf-8") as f:
                    for line in lines:
                        if line.split(",")[0] != name:
                            f.write(line)
        to_delete = ["Simulation_Profile","Warmwasser_Nutzungsmischungen","Strombedarf_Nutzungsmischungen"]
        del_Profile()
        self.UpdateProfiles()
        

    def UpdateProfiles(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Simulation_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.clear() 
        self.comboBox_SelectProfile.addItems(names)        
        self.comboBox_SelectProfile.setCurrentText(self.lineEdit_Profil.text())
                   

    def LoadProfile(self):
     
        df = pd.read_csv("./EMS-Frontend/data/Simulation_Profile.csv", delimiter = ",", encoding='utf-8')
        name = self.comboBox_SelectProfile.currentText()
        self.lineEdit_Profil.setText(name)
        values = df[df.values == name].values.flatten().tolist()

        #Profilnamen laden
        for i,widget in enumerate(self.li_inputWidgets,1):
            continue
            widget.setText(values[i])

        #Nutzungsmischung Warmwasser laden
        df = pd.read_csv("./EMS-Frontend/data/Warmwasser_Nutzungsmischungen.csv", delimiter = ",", encoding='utf-8')
        name = self.comboBox_SelectProfile.currentText()
        self.lineEdit_Profil.setText(name)
        values = df[df.values == name].values.flatten().tolist()
        #self.Warmwasser.graphWindow

        for i,value in enumerate(values[2:]):
            value = value.split("----")
            datapoints = ["Profilname","WW-Verbrauch_Stunde [%]","WW-Verbrauch_Monat [%]","Verbrauchsart"]
            for datapoint in datapoints:
                for i in range(len(value)):
                    continue
                    #data = {
                    #    "Profilname" : data[0],
                    #    }
        #
			#"WW-Verbrauch_Stunde [%]" : data[1:25],
           # "WW-Verbrauch_Monat [%]" : data[27:],
			#"Verbrauchsart" : data[25:27],
        


       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
main = MainWindow()
w = Ui_Main()
w.setupUi(main)
main.show()
app.exec()