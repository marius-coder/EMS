# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import csv
import importlib
Import = importlib.import_module("EMS-Backend.Classes.Import")
import warnings
warnings.filterwarnings("error")

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PV_Batterie(QWidget):

    def __init__(self, parent):
        super(Ui_PV_Batterie, self).__init__()
        
        self.parent = parent
        self.setObjectName("self")
        self.resize(601, 254)
        self.setWindowTitle("PV-Batterie")

        #Eingabe PV-Daten
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(110, 0, 20, 431))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_PV = QtWidgets.QLabel(self)
        self.label_PV.setGeometry(QtCore.QRect(20, 10, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_PV.setFont(font)
        self.label_PV.setScaledContents(False)
        self.label_PV.setObjectName("label_PV")
        self.label_PV.setText("PV")
        self.doubleSpinBox_PV_kWp = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_PV_kWp.setGeometry(QtCore.QRect(20, 70, 62, 22))
        self.doubleSpinBox_PV_kWp.setMaximum(9999999999.0)
        self.doubleSpinBox_PV_kWp.setObjectName("doubleSpinBox_PV_kWp")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Eingabe kWp")

        #Eingabe Batteriedaten
        #Eingabe Speichergröße
        self.label_Bat = QtWidgets.QLabel(self)
        self.label_Bat.setGeometry(QtCore.QRect(140, 10, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_Bat.setFont(font)
        self.label_Bat.setScaledContents(False)
        self.label_Bat.setObjectName("label_Bat")
        self.label_Bat.setText("Batterie")
        self.doubleSpinBox_Bat_kWh = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_Bat_kWh.setGeometry(QtCore.QRect(140, 70, 62, 22))
        self.doubleSpinBox_Bat_kWh.setMaximum(9999999999.0)
        self.doubleSpinBox_Bat_kWh.setObjectName("doubleSpinBox_Bat_kWh")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(140, 50, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Speichergröße kWh")

        #Entladetiefe
        self.spinBox_Entladetiefe = QtWidgets.QSpinBox(self)
        self.spinBox_Entladetiefe.setGeometry(QtCore.QRect(140, 120, 42, 22))
        self.spinBox_Entladetiefe.setMaximum(100)
        self.spinBox_Entladetiefe.setObjectName("spinBox_Entladetiefe")
        self.label_Entladetiefe = QtWidgets.QLabel(self)
        self.label_Entladetiefe.setGeometry(QtCore.QRect(140, 100, 81, 16))
        self.label_Entladetiefe.setObjectName("label_Entladetiefe")
        self.label_Entladetiefe.setText("Entladetiefe [%]")

        #Batterie Effizienz
        self.spinBox_Effizienz = QtWidgets.QSpinBox(self)
        self.spinBox_Effizienz.setGeometry(QtCore.QRect(140, 183, 42, 22))
        self.spinBox_Effizienz.setMaximum(100)
        self.spinBox_Effizienz.setObjectName("spinBox_Effizienz")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(140, 150, 81, 31))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Effizienz [%] (Laden&Entladen)")

        #Eingabe Batterieleistung
        self.spinBox_Leistung = QtWidgets.QSpinBox(self)
        self.spinBox_Leistung.setGeometry(QtCore.QRect(240, 183, 42, 22))
        self.spinBox_Leistung.setMaximum(100)
        self.spinBox_Leistung.setObjectName("spinBox_Leistung")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(240, 150, 91, 31))
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("Leistung (Laden&Entladen)")
        self.radioButton_BatLeistungAbsolute = QtWidgets.QRadioButton(self)
        self.radioButton_BatLeistungAbsolute.setGeometry(QtCore.QRect(290, 197, 82, 17))
        self.radioButton_BatLeistungAbsolute.setObjectName("radioButton_BatLeistungAbsolute")
        self.radioButton_BatLeistungAbsolute.setText("Absolut [kW]")
        self.radioButton_BatLeistungPercent = QtWidgets.QRadioButton(self)
        self.radioButton_BatLeistungPercent.setGeometry(QtCore.QRect(290, 180, 82, 17))
        self.radioButton_BatLeistungPercent.setObjectName("radioButton_BatLeistungPercent")       
        self.radioButton_BatLeistungPercent.setText("Prozent [%]")

        #Selbstentladung
        self.spinBox_Selbstentladung = QtWidgets.QSpinBox(self)
        self.spinBox_Selbstentladung.setGeometry(QtCore.QRect(240, 120, 42, 22))
        self.spinBox_Selbstentladung.setMaximum(100)
        self.spinBox_Selbstentladung.setObjectName("spinBox_Selbstentladung")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(240, 100, 111, 16))
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("Selbstentladung [%/a]")

        #Profil Stuff (Laden,Speichern,löschen etc.)
        self.pushButton_SaveProfile = QtWidgets.QPushButton(self)
        self.pushButton_SaveProfile.setGeometry(QtCore.QRect(510, 70, 75, 23))
        self.pushButton_SaveProfile.setObjectName("pushButton_SaveProfile")
        self.pushButton_SaveProfile.setText("Save Profile")
        self.comboBox_SelectProfile = QtWidgets.QComboBox(self)
        self.comboBox_SelectProfile.setGeometry(QtCore.QRect(390, 120, 111, 22))
        self.comboBox_SelectProfile.setObjectName("comboBox_SelectProfile")
        self.lineEdit_Profil = QtWidgets.QLineEdit(self)
        self.lineEdit_Profil.setGeometry(QtCore.QRect(390, 70, 113, 20))
        self.lineEdit_Profil.setObjectName("lineEdit")
        self.label_ProfilEingabe = QtWidgets.QLabel(self)
        self.label_ProfilEingabe.setGeometry(QtCore.QRect(390, 50, 111, 16))
        self.label_ProfilEingabe.setWordWrap(True)
        self.label_ProfilEingabe.setObjectName("label_ProfilEingabe")
        self.label_ProfilEingabe.setText("Eingabe Profilname")
        self.pushButton_DeleteProfile = QtWidgets.QPushButton(self)
        self.pushButton_DeleteProfile.setGeometry(QtCore.QRect(510, 120, 75, 23))
        self.pushButton_DeleteProfile.setObjectName("pushButton_DeleteProfile")
        self.pushButton_DeleteProfile.setText("Delete Profile")
        self.label_ProfilAuswahl = QtWidgets.QLabel(self)
        self.label_ProfilAuswahl.setGeometry(QtCore.QRect(390, 100, 111, 16))
        self.label_ProfilAuswahl.setWordWrap(True)
        self.label_ProfilAuswahl.setObjectName("label_ProfilAuswahl")
        self.label_ProfilAuswahl.setText("Auswahl Profil")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(370, -10, 20, 461))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_Bat_2 = QtWidgets.QLabel(self)
        self.label_Bat_2.setGeometry(QtCore.QRect(390, 10, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_Bat_2.setFont(font)
        self.label_Bat_2.setScaledContents(False)
        self.label_Bat_2.setObjectName("label_Bat_2")
        self.label_Bat_2.setText("Profil")
        self.pushButton_UseProfile = QtWidgets.QPushButton(self)
        self.pushButton_UseProfile.setGeometry(QtCore.QRect(400, 200, 91, 31))
        self.pushButton_UseProfile.setObjectName("pushButton_UseProfile")
        self.pushButton_UseProfile.setText("Profil benutzen")
        self.pushButton_UseProfile.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}") 
        self.pushButton_Back = QtWidgets.QPushButton(self)
        self.pushButton_Back.setGeometry(QtCore.QRect(500, 200, 91, 31))
        self.pushButton_Back.setObjectName("pushButton_Back")
        self.pushButton_Back.setText("Zurück")

        self.li_inputWidgets = [self.doubleSpinBox_PV_kWp,self.doubleSpinBox_Bat_kWh,self.spinBox_Entladetiefe,
                           self.spinBox_Selbstentladung,self.spinBox_Effizienz,self.spinBox_Leistung]

        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./EMS-Frontend/data/PV_Bat_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.addItems(names)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)
        self.pushButton_UseProfile.clicked.connect(self.UseProfile)

    def SaveProfile(self):
        names = list(pd.read_csv("./EMS-Frontend/data/PV_Bat_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        
        name = self.lineEdit_Profil.text()
        #Wenn nichts im Lineedit steht oder kein Radiobutton ausgewählt ist wird das Profil nicht gespeichert
        if name == "" or self.radioButton_BatLeistungAbsolute.isChecked() == False and self.radioButton_BatLeistungPercent.isChecked() == False:
            return
   
        li_toSave = []
        li_toSave.append(name)

        for widget in self.li_inputWidgets:
            if widget.objectName() == "spinBox_Leistung":
                if self.radioButton_BatLeistungPercent.isChecked():
                    li_toSave.append("None")
                    li_toSave.append(self.spinBox_Leistung.value())
                else:
                     li_toSave.append(self.spinBox_Leistung.value())
                     li_toSave.append("None")
            else:
                li_toSave.append(widget.value())


        #Kontrolle ob ein Profil mit diesem Namen bereits existiert
        if name in names:
            self.DeleteProfile()
        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/PV_Bat_Profile.csv",'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave)
        self.UpdateProfiles()
   
    def DeleteProfile(self):
        name = self.comboBox_SelectProfile.currentText()
        with open("./EMS-Frontend/data/PV_Bat_Profile.csv", 'r', encoding="utf-8") as inp:
            lines = inp.readlines()
        with open("./EMS-Frontend/data/PV_Bat_Profile.csv",'w', newline='', encoding="utf-8") as f:
            for line in lines:
                if line.split(",")[0] != name:
                    f.write(line)
        self.UpdateProfiles()
        

    def UpdateProfiles(self):
        names = list(pd.read_csv("./EMS-Frontend/data/PV_Bat_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.clear() 
        self.comboBox_SelectProfile.addItems(names)        
        self.comboBox_SelectProfile.setCurrentText(self.lineEdit_Profil.text())
                   

    def LoadProfile(self):
     
        df = pd.read_csv("./EMS-Frontend/data/PV_Bat_Profile.csv", delimiter = ",", encoding='utf-8')

        name = self.comboBox_SelectProfile.currentText()

        self.lineEdit_Profil.setText(name)
        values = df[df.values == name].values.flatten().tolist()
        df = df[df.values == name]

        for i,widget in enumerate(self.li_inputWidgets,1):
            if widget.objectName() == "spinBox_Leistung":
                if df["Leistung [kW]"].values[0] != "None":
                    self.radioButton_BatLeistungAbsolute.setChecked(True)
                    try:
                        widget.setValue(float(df["Leistung [kW]"].values[0]))
                    except TypeError:
                        widget.setValue(int(df["Leistung [kW]"].values[0]))
                    
                else:
                    self.radioButton_BatLeistungPercent.setChecked(True)
                    try:
                        widget.setValue(float(df["Leistung [%]"].values[0]))
                    except TypeError:
                        widget.setValue(int(df["Leistung [%]"].values[0]))
            else:
                try:
                    widget.setValue(float(values[i]))
                except TypeError:
                    widget.setValue(int(values[i]))

    def UseProfile(self):

        self.SaveProfile()


        df = pd.read_csv("./EMS-Frontend/data/PV_Bat_Profile.csv", delimiter = ",", encoding='utf-8')
        name = self.lineEdit_Profil.text()



        data = df[df.values == name].values.flatten().tolist()


        PV_Batterie = {
            "PV_kWp" : data[1],
            "Bat_kWh": data[2],
            "Entladetiefe" : data[3],
            "Selbstentladung" : data[4],
            "Effizienz" : data[5],
            "Leistung [kW]" : data[6],
            "Leistung [%]" : data[7],
            }
        Import.importGUI.Import_PV_Batterie(PV_Batterie)
        self.pushButton_UseProfile.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        self.parent.lineEdit_PVBatterie.setText(self.lineEdit_Profil.text())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


