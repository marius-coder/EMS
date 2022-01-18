# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import csv
import importlib
Import = importlib.import_module("EMS-Backend.Classes.Import")
#Speicher = importlib.import_module("EMS-Frontend.Wärmepumpe_Speicher.Wärmespeicher")
from Wärmepumpe_Speicher.Wärmespeicher import Ui_Speicher

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WP(QWidget):


    def __init__(self,typ, parent):
        super(Ui_WP, self).__init__()

        self.parent = parent
        self.setWindowTitle("Auswahl Wärmepumpe")
        self.resize(553, 322)    
        self.typ = typ

        #Ansicht WP Auswahl
        self.label_ArtWP = QtWidgets.QLabel(self)
        self.label_ArtWP.setGeometry(QtCore.QRect(20, 50, 47, 13))
        self.label_ArtWP.setObjectName("label_ArtWP")
        self.label_ArtWP.setText("Art")
        self.radioButton_Heizen = QtWidgets.QRadioButton(self)
        self.radioButton_Heizen.setGeometry(QtCore.QRect(20, 70, 91, 17))
        self.radioButton_Heizen.setObjectName("radioButton_Heizen")
        self.radioButton_Heizen.setText("Heizen/Kühlen")
        self.radioButton_Heizen.setEnabled(False)
        self.radioButton_WW = QtWidgets.QRadioButton(self)
        self.radioButton_WW.setGeometry(QtCore.QRect(120, 70, 91, 17))
        self.radioButton_WW.setObjectName("radioButton_WW")
        self.radioButton_WW.setText("Warmwasser")
        self.radioButton_WW.setEnabled(False)

        if typ == "Heizen":
            self.radioButton_Heizen.setChecked(True)
        elif typ == "Warmwasser":
            self.radioButton_WW.setChecked(True)

        self.label_Eingabe = QtWidgets.QLabel(self)
        self.label_Eingabe.setGeometry(QtCore.QRect(20, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_Eingabe.setFont(font)
        self.label_Eingabe.setObjectName("label_Eingabe")
        self.label_Eingabe.setText("Eingabe")

        self.label_Profil = QtWidgets.QLabel(self)
        self.label_Profil.setGeometry(QtCore.QRect(240, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_Profil.setFont(font)
        self.label_Profil.setObjectName("label_Profil")
        self.label_Profil.setText("Profil")

        #Eingabe Stromverbrauch
        self.doubleSpinBox_Stromverbrauch = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_Stromverbrauch.setGeometry(QtCore.QRect(20, 120, 71, 22))
        self.doubleSpinBox_Stromverbrauch.setObjectName("doubleSpinBox_Stromverbrauch")
        self.label_Stromverbrauch = QtWidgets.QLabel(self)
        self.label_Stromverbrauch.setGeometry(QtCore.QRect(20, 100, 111, 16))
        self.label_Stromverbrauch.setObjectName("label_Stromverbrauch")
        self.label_Stromverbrauch.setText("Stromverbrauch [kW]")

        #Eingabe COP
        self.doubleSpinBox_COP = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_COP.setGeometry(QtCore.QRect(20, 170, 71, 22))
        self.doubleSpinBox_COP.setObjectName("doubleSpinBox_COP")
        self.label_COP = QtWidgets.QLabel(self)
        self.label_COP.setGeometry(QtCore.QRect(20, 150, 111, 16))
        self.label_COP.setObjectName("label_COP")
        self.label_COP.setText("COP")

        #Eingabe VL Temperaturen WP
        self.label_VL_HZG = QtWidgets.QLabel(self)
        self.label_VL_HZG.setGeometry(QtCore.QRect(20, 200, 61, 16))
        self.label_VL_HZG.setObjectName("label_VL_HZG")
        self.label_VL_HZG.setText("VL HZG [°C]")
        self.doubleSpinBox_VL_HZG = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_VL_HZG.setGeometry(QtCore.QRect(20, 220, 61, 22))
        self.doubleSpinBox_VL_HZG.setObjectName("doubleSpinBox_VL_HZG")
        self.label_VL_KLG = QtWidgets.QLabel(self)
        self.label_VL_KLG.setGeometry(QtCore.QRect(90, 200, 71, 16))
        self.label_VL_KLG.setObjectName("label_VL_KLG")
        self.label_VL_KLG.setText("VL KLG [°C]")
        self.doubleSpinBox_VL_KLG = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_VL_KLG.setGeometry(QtCore.QRect(90, 220, 61, 22))
        self.doubleSpinBox_VL_KLG.setObjectName("doubleSpinBox_VL_KLG")

        

        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(210, 0, 16, 451))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #Button um zur Speicherauswahl zu gelangen
        self.pushButton_Speicherauswahl = QtWidgets.QPushButton(self)
        self.pushButton_Speicherauswahl.setGeometry(QtCore.QRect(20, 260, 101, 31))
        self.pushButton_Speicherauswahl.setObjectName("pushButton_Speicherauswahl")
        self.pushButton_Speicherauswahl.setText("Speicherauswahl")

        #Auswahl Profilname
        self.label_Profil = QtWidgets.QLabel(self)
        self.label_Profil.setGeometry(QtCore.QRect(230, 50, 200, 30))
        self.label_Profil.setText("Eingabe Profilname")
        self.lineEdit_Profil = QtWidgets.QLineEdit(self)
        self.lineEdit_Profil.setGeometry(QtCore.QRect(230, 75, 100, 20))
        self.lineEdit_Profil.setObjectName("lineEdit_Profil")

        #Combobox für Benutzerprofile
        self.label_AuswahlProfil = QtWidgets.QLabel(self)
        self.label_AuswahlProfil.setGeometry(QtCore.QRect(230, 100, 200, 30))
        self.label_AuswahlProfil.setText("Auswahl Profil")
        self.comboBox_SelectProfile = QtWidgets.QComboBox(self)
        self.comboBox_SelectProfile.setGeometry(QtCore.QRect(230, 125, 100, 22))
        self.comboBox_SelectProfile.setObjectName("comboBox_SelectProfile")

        #Profil speichern
        self.pushButton_SaveProfile = QtWidgets.QPushButton(self)
        self.pushButton_SaveProfile.setGeometry(QtCore.QRect(340, 73, 75, 23))
        self.pushButton_SaveProfile.setObjectName("pushButton_SaveProfile")
        self.pushButton_SaveProfile.setText("Save Profile")

        #Profil löschen
        self.pushButton_DeleteProfile = QtWidgets.QPushButton(self)
        self.pushButton_DeleteProfile.setGeometry(QtCore.QRect(340, 125, 75, 23))
        self.pushButton_DeleteProfile.setObjectName("pushButton_DeleteProfile")
        self.pushButton_DeleteProfile.setText("Delete Profile")       
        
        #Fertig mit Eingabe
        self.pushButton_UseProfile = QtWidgets.QPushButton(self)
        self.pushButton_UseProfile.setGeometry(QtCore.QRect(230, 245, 200, 30))
        self.pushButton_UseProfile.setObjectName("pushButton_UseProfile")
        self.pushButton_UseProfile.setText("Profil zur Nutzungsmischung hinzufügen") 
        self.pushButton_UseProfile.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}") 
        
        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.addItems(names)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)
        self.pushButton_UseProfile.clicked.connect(self.UseProfile)
        self.pushButton_Speicherauswahl.clicked.connect(self.OpenSpeicher)
        
        self.li_inputWidgets = [self.doubleSpinBox_Stromverbrauch, self.doubleSpinBox_COP, self.doubleSpinBox_VL_HZG,
                                self.doubleSpinBox_VL_KLG]


    def OpenSpeicher(self):
        if hasattr(self, 'speicherWindow') == False:
            self.speicherWindow = Ui_Speicher(float(self.doubleSpinBox_VL_HZG.value()),self.typ)
        self.speicherWindow.show()
        
    def SaveProfile(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        
        name = self.lineEdit_Profil.text()
        #Wenn nichts im Lineedit steht oder kein Radiobutton ausgewählt ist wird das Profil nicht gespeichert
        if self.lineEdit_Profil == "" or hasattr(self, 'speicherWindow') == False:
            return

        li_toSave = []
        li_toSave.append(name)

        if self.radioButton_Heizen.isChecked():
            li_toSave.append("Heizen")
        elif self.radioButton_WW.isChecked():
            li_toSave.append("Warmwasser")      

        for widget in self.li_inputWidgets:                
            li_toSave.append(widget.value())
            
        li_toSave.append(self.speicherWindow.lineEdit_Profil.text())

        #Kontrolle ob ein Profil mit diesem Namen bereits existiert
        if name in names:
            self.DeleteProfile()
        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/Wärmepumpe_Profile.csv",'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave)
        self.UpdateProfiles()
   
    def DeleteProfile(self):
        name = self.comboBox_SelectProfile.currentText()
        with open("./EMS-Frontend/data/Wärmepumpe_Profile.csv", 'r', encoding="utf-8") as inp:
            lines = inp.readlines()
        with open("./EMS-Frontend/data/Wärmepumpe_Profile.csv",'w', newline='', encoding="utf-8") as f:
            for line in lines:
                if line.split(",")[0] != name:
                    f.write(line)
        self.UpdateProfiles()
        

    def UpdateProfiles(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.clear() 
        self.comboBox_SelectProfile.addItems(names)        
        self.comboBox_SelectProfile.setCurrentText(self.lineEdit_Profil.text())
                   

    def LoadProfile(self):
     
        df = pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", delimiter = ",", encoding='utf-8')

        name = self.lineEdit_Profil.text()

        self.lineEdit_Profil.setText(name)
        values = df[df.values == name].values.flatten().tolist()

        if values[1] == "Heizen":
            self.radioButton_Heizen.setChecked(True)
        elif values[1] == "Warmwasser":
            self.radioButton_WW.setChecked(True)

        for i,widget in enumerate(self.li_inputWidgets,2):
            widget.setValue(float(values[i]))

        #if hasattr(self, 'speicherWindow') == False:
        self.speicherWindow = Ui_Speicher(float(self.doubleSpinBox_VL_HZG.value()),self.typ)
        self.speicherWindow.LoadProfile(values[-1])

    def UseProfile(self):

        if self.lineEdit_Profil.text() == "":
            return

        self.SaveProfile()

        df = pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", delimiter = ",", encoding='utf-8')
        name = self.comboBox_SelectProfile.currentText()

        data = df[df.values == name].values.flatten().tolist()
        Wärmepumpe = {
            "Art" : self.typ,
            "Stromverbrauch" : data[1],
            "COP": data[2],
            "VL_HZG" : data[3],
            "VL_KLG" : data[4],
            "speichername" : data[5],
            }
        Import.importGUI.Import_WP(Wärmepumpe)
        self.pushButton_UseProfile.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        if self.typ == "Heizen":
            self.parent.lineEdit_Wärmepumpe_HZG.setText(self.lineEdit_Profil.text())
        else:
            self.parent.lineEdit_Wärmepumpe_WW.setText(self.lineEdit_Profil.text())
      

    
        



#app = QApplication(sys.argv)
#main = QWidget()
#w = Ui_WP()
#w.show()
#app.exec()