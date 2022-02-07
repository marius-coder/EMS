# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import csv
from Erdwärme.Erdwärme_Karte import WindowErdwärmeKarte
import importlib
Slider = importlib.import_module("EMS-Frontend.data.Stylesheets")
Import = importlib.import_module("EMS-Backend.Classes.Import")
BackErdwärme = importlib.import_module("EMS-Backend.Classes.Erdwärme")
import warnings
warnings.filterwarnings("error")

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Erdwärme(QWidget):
    
    def __init__(self, parent):
        super(Ui_Erdwärme, self).__init__()

        self.parent = parent
        self.setObjectName("self")
        self.resize(400, 270)
        self.setWindowTitle("Erdwärme")
        self.windowKarte = WindowErdwärmeKarte()

        #Hier werden beide Fenster richtig positioniert
        #Die Fenstergröße wird hierbei dynamisch an die Bildschirmgröße angepasst
        #Desktopmaße
        coords = QApplication.desktop().availableGeometry()
        left_Coord = int(coords.height() / 2 - self.frameGeometry().height() / 2)
        #self.move(10,left_Coord)
        self.windowKarte.move(self.pos().x() + self.frameGeometry().width() + 10, self.pos().y())
        self.windowKarte.resize(1100, 1100)

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Eingabe")
        
        #Eingabe Adresse
        self.lineEdit_ReadOnly = QtWidgets.QLineEdit(self)
        self.lineEdit_ReadOnly.setGeometry(QtCore.QRect(10, 70, 161, 20))
        self.lineEdit_ReadOnly.setReadOnly(True)
        self.lineEdit_ReadOnly.setObjectName("lineEdit_ReadOnly")
        self.lineEdit_ReadOnly.setText("Höchstädtplatz 6, 1200 Wien")
        self.lineEdit_ReadOnly.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : lightgrey;"
                                    "}")
        self.lineEdit_InputAdresse = QtWidgets.QLineEdit(self)
        self.lineEdit_InputAdresse.setGeometry(QtCore.QRect(10, 100, 161, 20))
        self.lineEdit_InputAdresse.setObjectName("lineEdit_InputAdresse")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 50, 47, 13))
        self.label.setObjectName("label")
        self.label.setText("Adresse")

        #Eingabe Anzahl Sonden
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Anzahl Sonden")
        self.spinBox_AnzSonden = QtWidgets.QSpinBox(self)
        self.spinBox_AnzSonden.setGeometry(QtCore.QRect(10, 150, 71, 22))
        self.spinBox_AnzSonden.setObjectName("spinBox_AnzSonden")
        self.spinBox_AnzSonden.setRange(0,1000)


        #Eingabe Bohrtiefe
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(110, 130, 71, 16))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Bohrtiefe [m]")
        self.doubleSpinBox_Bohrtiefe = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_Bohrtiefe.setGeometry(QtCore.QRect(110, 150, 62, 22))
        self.doubleSpinBox_Bohrtiefe.setObjectName("doubleSpinBox_Bohrtiefe")
        self.doubleSpinBox_Bohrtiefe.setRange(0,300)


        #Eingabe Sondenabstand
        self.label_SonAbstand = QtWidgets.QLabel(self)
        self.label_SonAbstand.setGeometry(QtCore.QRect(10, 180, 71, 16))
        self.label_SonAbstand.setObjectName("label_SonAbstand")
        self.label_SonAbstand.setText("Sondenabstand [m]")
        self.doubleSpinBox_SonAbstand = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_SonAbstand.setGeometry(QtCore.QRect(10, 200, 62, 22))
        self.doubleSpinBox_SonAbstand.setObjectName("doubleSpinBox_SonAbstand")
        self.doubleSpinBox_SonAbstand.setRange(0,300)


        #Ausgabe Wärmeleitfähigkeit/Leistung 
        self.label_WM_spez = QtWidgets.QLabel(self)
        self.label_WM_spez.setGeometry(QtCore.QRect(190, 145, 100, 32))
        self.label_WM_spez.setObjectName("label_WM_spez")
        self.label_WM_spez.setText("Wärmeleitfähigkeit Erdboden [W/m/K]")
        self.label_WM_spez.setWordWrap(True)   
        self.lineEdit_WM_spez = QtWidgets.QLineEdit(self)
        self.lineEdit_WM_spez.setGeometry(QtCore.QRect(190, 180, 50, 20))
        self.lineEdit_WM_spez.setReadOnly(True)
        self.lineEdit_WM_spez.setObjectName("lineEdit_WM_spez")
        #self.label_Leistung = QtWidgets.QLabel(self)
        #self.label_Leistung.setGeometry(QtCore.QRect(300, 145, 100, 32))
        #self.label_Leistung.setObjectName("label_WM_spez")
        #self.label_Leistung.setText("Leistung [kW] (5K Spreizung)")
        #self.label_Leistung.setWordWrap(True)
        #self.lineEdit_Leistung = QtWidgets.QLineEdit(self)
        #self.lineEdit_Leistung.setGeometry(QtCore.QRect(300, 180, 50, 20))
        #self.lineEdit_Leistung.setReadOnly(True)
        #self.lineEdit_Leistung.setObjectName("lineEdit_ReadOnly")

        #Profil Stuff (Laden,Speichern,löschen etc.)
        self.pushButton_SaveProfile = QtWidgets.QPushButton(self)
        self.pushButton_SaveProfile.setGeometry(QtCore.QRect(310, 70, 75, 23))
        self.pushButton_SaveProfile.setObjectName("pushButton_SaveProfile")
        self.pushButton_SaveProfile.setText("Save Profile")
        self.comboBox_SelectProfile = QtWidgets.QComboBox(self)
        self.comboBox_SelectProfile.setGeometry(QtCore.QRect(190, 120, 111, 22))
        self.comboBox_SelectProfile.setObjectName("comboBox_SelectProfile")
        self.lineEdit_Profil = QtWidgets.QLineEdit(self)
        self.lineEdit_Profil.setGeometry(QtCore.QRect(190, 70, 113, 20))
        self.lineEdit_Profil.setObjectName("lineEdit")
        self.label_ProfilEingabe = QtWidgets.QLabel(self)
        self.label_ProfilEingabe.setGeometry(QtCore.QRect(190, 50, 111, 16))
        self.label_ProfilEingabe.setWordWrap(True)
        self.label_ProfilEingabe.setObjectName("label_ProfilEingabe")
        self.label_ProfilEingabe.setText("Eingabe Profilname")
        self.pushButton_DeleteProfile = QtWidgets.QPushButton(self)
        self.pushButton_DeleteProfile.setGeometry(QtCore.QRect(310, 120, 75, 23))
        self.pushButton_DeleteProfile.setObjectName("pushButton_DeleteProfile")
        self.pushButton_DeleteProfile.setText("Delete Profile")
        self.label_ProfilAuswahl = QtWidgets.QLabel(self)
        self.label_ProfilAuswahl.setGeometry(QtCore.QRect(190, 100, 111, 16))
        self.label_ProfilAuswahl.setWordWrap(True)
        self.label_ProfilAuswahl.setObjectName("label_ProfilAuswahl")
        self.label_ProfilAuswahl.setText("Auswahl Profil")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(170, -10, 20, 461))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_Bat_2 = QtWidgets.QLabel(self)
        self.label_Bat_2.setGeometry(QtCore.QRect(190, 10, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_Bat_2.setFont(font)
        self.label_Bat_2.setScaledContents(False)
        self.label_Bat_2.setObjectName("label_Bat_2")
        self.label_Bat_2.setText("Profil")
        self.pushButton_UseProfile = QtWidgets.QPushButton(self)
        self.pushButton_UseProfile.setGeometry(QtCore.QRect(200, 220, 91, 31))
        self.pushButton_UseProfile.setObjectName("pushButton_UseProfile")
        self.pushButton_UseProfile.setText("Profil benutzen")
        self.pushButton_UseProfile.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : red,"
                             "}")  
        self.pushButton_Back = QtWidgets.QPushButton(self)
        self.pushButton_Back.setGeometry(QtCore.QRect(300, 220, 91, 31))
        self.pushButton_Back.setObjectName("pushButton_Back")
        self.pushButton_Back.setText("Zurück")

        self.pushButton_LookMap = QtWidgets.QPushButton(self)
        self.pushButton_LookMap.setGeometry(QtCore.QRect(300, 10, 75, 23))
        self.pushButton_LookMap.setObjectName("pushButton_LookMap")
        self.pushButton_LookMap.setText("Karte")

        self.li_inputWidgets = [self.lineEdit_InputAdresse,self.spinBox_AnzSonden,self.doubleSpinBox_Bohrtiefe,
                                self.doubleSpinBox_SonAbstand]

        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./EMS-Frontend/data/Erdwärme_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.addItems(names)
        self.comboBox_SelectProfile.activated.connect(self.SetText)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)
        self.pushButton_UseProfile.clicked.connect(self.UseProfile)
        self.pushButton_LookMap.clicked.connect(self.OpenMap)

    def SetText(self):
        self.lineEdit_Profil.setText(self.comboBox_SelectProfile.currentText())

    def SaveProfile(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Erdwärme_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        
        name = self.lineEdit_Profil.text()
        #Wenn nichts im Lineedit steht oder kein Radiobutton ausgewählt ist wird das Profil nicht gespeichert
        if name == "" or self.lineEdit_InputAdresse.text() == "":
            return
   
        li_toSave = []
        li_toSave.append(name)

        for widget in self.li_inputWidgets:
            if widget.objectName() == "lineEdit_InputAdresse":
                li_toSave.append(widget.text())
            else:
                li_toSave.append(widget.value())


        #Kontrolle ob ein Profil mit diesem Namen bereits existiert
        if name in names:
            self.DeleteProfile()
        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/Erdwärme_Profile.csv",'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave)
        self.UpdateProfiles()
   
    def DeleteProfile(self):
        name = self.lineEdit_Profil.text()
        with open("./EMS-Frontend/data/Erdwärme_Profile.csv", 'r', encoding="utf-8") as inp:
            lines = inp.readlines()
        with open("./EMS-Frontend/data/Erdwärme_Profile.csv",'w', newline='', encoding="utf-8") as f:
            for line in lines:
                if line.split(",")[0] != name:
                    f.write(line)
        self.UpdateProfiles()
        

    def UpdateProfiles(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Erdwärme_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.clear() 
        self.comboBox_SelectProfile.addItems(names)        
        self.comboBox_SelectProfile.setCurrentText(self.lineEdit_Profil.text())
                   

    def LoadProfile(self):
     
        df = pd.read_csv("./EMS-Frontend/data/Erdwärme_Profile.csv", delimiter = ",", encoding='utf-8')

        name = self.lineEdit_Profil.text()

        self.lineEdit_Profil.setText(name)
        values = df[df.values == name].values.flatten().tolist()

        for i,widget in enumerate(self.li_inputWidgets,1):
            if widget.objectName() == "lineEdit_InputAdresse":
                widget.setText(values[i])
            else:
                try:
                    widget.setValue(float(values[i]))
                except TypeError:
                    widget.setValue(int(values[i]))
        

    def UseProfile(self):
        if self.lineEdit_InputAdresse.text() == "" or self.doubleSpinBox_Bohrtiefe.value() == 0:
            return
        
        input_GeoData = {"Adresse" : self.lineEdit_InputAdresse.text(),
								"Bohrtiefe" : self.doubleSpinBox_Bohrtiefe.value(),
								"Anzahl_Sonden" : self.spinBox_AnzSonden.value()}
        Output_GeoData = BackErdwärme.Get_GeothermalData(input_GeoData)
        self.lineEdit_WM_spez.setText(str(round(Output_GeoData["MW_WL"],3)))
        #self.lineEdit_Leistung.setText(str(round(float(self.lineEdit_WM_spez.text()) * float(self.spinBox_AnzSonden.value()) * float(self.doubleSpinBox_Bohrtiefe.value()) * 5/1000,3)))


        self.SaveProfile()
        df = pd.read_csv("./EMS-Frontend/data/Erdwärme_Profile.csv", delimiter = ",", encoding='utf-8')
        name = self.comboBox_SelectProfile.currentText()

        data = df[df.values == name].values.flatten().tolist()

        self.pushButton_UseProfile.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        Erdwärme = {
            "Adresse" : data[1],            
            "Anzahl_Sonden" : data[2],
            "Bohrtiefe": data[3],
            "Abstand_Sonden" : data[4],
            "WM_spez" : float(self.lineEdit_WM_spez.text())}
            #"Leistung" : self.lineEdit_Leistung.text()}
        Import.importGUI.Import_Geothermal(Erdwärme)
        self.parent.lineEdit_Erdwärme.setText(self.lineEdit_Profil.text())


    def OpenMap(self):
        if self.lineEdit_InputAdresse.text() == "" or self.doubleSpinBox_Bohrtiefe.value() == 0:
            return
        
        input_GeoData = {"Adresse" : self.lineEdit_InputAdresse.text(),
								"Bohrtiefe" : self.doubleSpinBox_Bohrtiefe.value(),
								"Anzahl_Sonden" : self.spinBox_AnzSonden.value()}
        Output_GeoData = BackErdwärme.Get_GeothermalData(input_GeoData)
        self.lineEdit_WM_spez.setText(str(round(Output_GeoData["MW_WL"],3)))
        #self.lineEdit_Leistung.setText(str(round(float(self.lineEdit_WM_spez.text()) * float(self.spinBox_AnzSonden.value()) * float(self.doubleSpinBox_Bohrtiefe.value()) * 5/1000,3)))
        self.windowKarte.UpdatePlot(self.lineEdit_InputAdresse.text(),Output_GeoData["Layer"])
        self.windowKarte.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()



