# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import csv
import importlib
Import = importlib.import_module("EMS-Backend.Classes.Import")

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WP(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auswahl Wärmespeicher")
        self.resize(553, 322)

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
        
        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmespeicher_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.addItems(names)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)
        self.pushButton_UseProfile.clicked.connect(self.UseProfile)
        
        self.li_inputWidgets = [self.doubleSpinBox_Stromverbrauch, self.doubleSpinBox_COP, self.doubleSpinBox_VL_HZG,
                                self.doubleSpinBox_VL_KLG]
        
    def SaveProfile(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmespeicher_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        
        name = self.lineEdit_Profil.text()
        #Wenn nichts im Lineedit steht oder kein Radiobutton ausgewählt ist wird das Profil nicht gespeichert
        
        li_toSave = []
        li_toSave.append(name)

        if self.radioButton_Heizen.isChecked():
            li_toSave.append("Heizen")
        elif self.radioButton_WW.isChecked():
            li_toSave.append("Warmwasser")      

        for widget in self.li_inputWidgets:                
            li_toSave.append(widget.value())
            
        #Kontrolle ob ein Profil mit diesem Namen bereits existiert
        if name in names:
            self.DeleteProfile()
        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/Wärmespeicher_Profile.csv",'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave)
        self.UpdateProfiles()
   
    def DeleteProfile(self):
        name = self.comboBox_SelectProfile.currentText()
        with open("./EMS-Frontend/data/Wärmespeicher_Profile.csv", 'r', encoding="utf-8") as inp:
            lines = inp.readlines()
        with open("./EMS-Frontend/data/Wärmespeicher_Profile.csv",'w', newline='', encoding="utf-8") as f:
            for line in lines:
                if line.split(",")[0] != name:
                    f.write(line)
        self.UpdateProfiles()
        

    def UpdateProfiles(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmespeicher_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.clear() 
        self.comboBox_SelectProfile.addItems(names)        
        self.comboBox_SelectProfile.setCurrentText(self.lineEdit_Profil.text())
                   

    def LoadProfile(self):
     
        df = pd.read_csv("./EMS-Frontend/data/Wärmespeicher_Profile.csv", delimiter = ",", encoding='utf-8')

        name = self.comboBox_SelectProfile.currentText()

        self.lineEdit_Profil.setText(name)
        values = df[df.values == name].values.flatten().tolist()
        df = df[df.values == name]

        

    def UseProfile(self):

        self.SaveProfile()

        df = pd.read_csv("./EMS-Frontend/data/Wärmespeicher_Profile.csv", delimiter = ",", encoding='utf-8')
        name = self.comboBox_SelectProfile.currentText()

        data = df[df.values == name].values.flatten().tolist()

      
        #Import.importGUI.Import_Wärmespeicherterie()

    
        



app = QApplication(sys.argv)
main = QWidget()
w = Ui_WP()
w.show()
app.exec()