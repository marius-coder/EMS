# -*- coding: utf-8 -*-
import os
import sys
from bokeh import plotting, embed, resources
from bokeh.plotting import figure
from colour import Color
import math
import pandas as pd
import csv
import importlib
Import = importlib.import_module("EMS-Backend.Classes.Import")

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Speicher(QWidget):

    def __init__(self,t_VL,typ):
        super().__init__()

        self.setWindowTitle("Auswahl Wärmespeicher")
        self.resize(747, 393)
        self.typ = typ

        self.label_Profil = QtWidgets.QLabel(self)
        self.label_Profil.setGeometry(QtCore.QRect(530, 20, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_Profil.setFont(font)
        self.label_Profil.setObjectName("label_Profil")
        self.label_Profil.setText("Profil")

        self.label_Eingabe = QtWidgets.QLabel(self)
        self.label_Eingabe.setGeometry(QtCore.QRect(10, 20, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_Eingabe.setFont(font)
        self.label_Eingabe.setObjectName("label_Eingabe")
        self.label_Eingabe.setText("Eingabe")

        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(230, 0, 16, 451))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label__Vis = QtWidgets.QLabel(self)
        self.label__Vis.setGeometry(QtCore.QRect(250, 20, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label__Vis.setFont(font)
        self.label__Vis.setObjectName("label__Vis")
        self.label__Vis.setText("Visualisierung")

        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(520, 0, 16, 451))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        #Autocomplete
        self.pushButton_Autocomplete = QtWidgets.QPushButton(self)
        self.pushButton_Autocomplete.setGeometry(QtCore.QRect(100, 30, 81, 21))
        self.pushButton_Autocomplete.setObjectName("pushButton_Autocomplete")
        self.pushButton_Autocomplete.setText("Autocomplete")
        self.pushButton_Autocomplete.clicked.connect(self.Autocomplete)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(10, 60, 216, 261))
        self.widget.setObjectName("widget")

        #Volumen
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_Volumen = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Volumen.setFont(font)
        self.label_Volumen.setObjectName("label_Volumen")
        self.label_Volumen.setText("Volumen [l]")
        self.verticalLayout_4.addWidget(self.label_Volumen)
        self.doubleSpinBox_Volumen = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_Volumen.setObjectName("doubleSpinBox_Volumen")
        self.doubleSpinBox_Volumen.setRange(0,999999999999)
        self.verticalLayout_4.addWidget(self.doubleSpinBox_Volumen)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        #Durchmesser
        self.label_Durchmesser = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Durchmesser.setFont(font)
        self.label_Durchmesser.setObjectName("label_Durchmesser")
        self.label_Durchmesser.setText("Durchmesser [m]")
        self.verticalLayout_2.addWidget(self.label_Durchmesser)
        self.doubleSpinBox_Durchmesser = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_Durchmesser.setObjectName("doubleSpinBox_Durchmesser")
        self.doubleSpinBox_Durchmesser.setRange(0,999999999999)
        self.verticalLayout_2.addWidget(self.doubleSpinBox_Durchmesser)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        #Eingabe Ladeschicht
        self.label_Ladeschicht = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Ladeschicht.setFont(font)
        self.label_Ladeschicht.setObjectName("label_Ladeschicht")
        self.label_Ladeschicht.setText("Ladeschicht")
        self.verticalLayout_6.addWidget(self.label_Ladeschicht)
        self.spinBox_Ladeschicht = QtWidgets.QSpinBox(self.widget)
        self.spinBox_Ladeschicht.setObjectName("spinBox_Ladeschicht")
        self.verticalLayout_6.addWidget(self.spinBox_Ladeschicht)
        self.gridLayout.addLayout(self.verticalLayout_6, 2, 1, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        #Eingabe Höhe
        self.label_Hohe = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Hohe.setFont(font)
        self.label_Hohe.setObjectName("label_Hohe")
        self.label_Hohe.setText("Höhe [m]")
        self.verticalLayout_3.addWidget(self.label_Hohe)
        self.doubleSpinBox_Hohe = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_Hohe.setObjectName("doubleSpinBox_Hohe")
        self.doubleSpinBox_Hohe.setRange(0,999999999999)
        self.verticalLayout_3.addWidget(self.doubleSpinBox_Hohe)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        #Eingabe Anzahl Schichten
        self.label_anzSchichten = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_anzSchichten.setFont(font)
        self.label_anzSchichten.setObjectName("label_anzSchichten")
        self.label_anzSchichten.setText("Anzahl Schichten")
        self.verticalLayout_5.addWidget(self.label_anzSchichten)
        self.spinBox_anzSchichten = QtWidgets.QSpinBox(self.widget)
        self.spinBox_anzSchichten.setObjectName("spinBox_anzSchichten")
        self.verticalLayout_5.addWidget(self.spinBox_anzSchichten)
        self.gridLayout.addLayout(self.verticalLayout_5, 2, 0, 1, 1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.spinBox_anzSchichten.valueChanged.connect(self.UpdateSpeicher)

        #Eingabe Wärmedämmung
        self.label_lambdaDammung = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_lambdaDammung.setFont(font)
        self.label_lambdaDammung.setWordWrap(True)
        self.label_lambdaDammung.setObjectName("label_lambdaDammung")
        self.label_lambdaDammung.setText("Wärmeleitfähigkeit Dämmung [W/mK]")
        self.verticalLayout_8.addWidget(self.label_lambdaDammung)
        self.doubleSpinBox_lamdaDammung = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_lamdaDammung.setObjectName("doubleSpinBox_lamdaDammung")
        self.verticalLayout_8.addWidget(self.doubleSpinBox_lamdaDammung)
        self.gridLayout.addLayout(self.verticalLayout_8, 3, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        #Eingabe Radius
        self.label_Radius = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Radius.setFont(font)
        self.label_Radius.setObjectName("label_Radius")
        self.label_Radius.setText("Radius [m]")
        self.verticalLayout.addWidget(self.label_Radius)
        self.doubleSpinBox_Radius = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_Radius.setObjectName("doubleSpinBox_Radius")
        self.doubleSpinBox_Radius.setRange(0,999999999999)
        self.verticalLayout.addWidget(self.doubleSpinBox_Radius)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        #Eingabe Dicke Dämmung
        self.label_dickeDammung = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_dickeDammung.setFont(font)
        self.label_dickeDammung.setWordWrap(True)
        self.label_dickeDammung.setObjectName("label_dickeDammung")
        self.label_dickeDammung.setText("Dicke Dämmung [m]")
        self.verticalLayout_7.addWidget(self.label_dickeDammung)
        self.doubleSpinBox_dickeDammung = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_dickeDammung.setObjectName("doubleSpinBox_dickeDammung")
        self.verticalLayout_7.addWidget(self.doubleSpinBox_dickeDammung)
        self.gridLayout.addLayout(self.verticalLayout_7, 3, 0, 1, 1)

        #Visualisierung
        self.t_VL = t_VL
        self.WebEngine = QtWebEngineWidgets.QWebEngineView(self)
        self.WebEngine.setGeometry(QtCore.QRect(250, 60, 260, 320))
        p = figure(width=250, height=300)
        p.rect(x=1, y=1, width=10, height=100, fill_color="#cab2d6")
        html = embed.file_html(p, resources.CDN, "my plot")
        self.WebEngine.setHtml(html)

        #Auswahl Profilname
        self.label_Profil = QtWidgets.QLabel(self)
        self.label_Profil.setGeometry(QtCore.QRect(540, 50, 200, 30))
        self.label_Profil.setText("Eingabe Profilname")
        self.lineEdit_Profil = QtWidgets.QLineEdit(self)
        self.lineEdit_Profil.setGeometry(QtCore.QRect(540, 75, 100, 20))
        self.lineEdit_Profil.setObjectName("lineEdit_Profil")

        #Combobox für Benutzerprofile
        self.label_AuswahlProfil = QtWidgets.QLabel(self)
        self.label_AuswahlProfil.setGeometry(QtCore.QRect(540, 100, 200, 30))
        self.label_AuswahlProfil.setText("Auswahl Profil")
        self.comboBox_SelectProfile = QtWidgets.QComboBox(self)
        self.comboBox_SelectProfile.setGeometry(QtCore.QRect(540, 125, 100, 22))
        self.comboBox_SelectProfile.setObjectName("comboBox_SelectProfile")

        #Profil speichern
        self.pushButton_SaveProfile = QtWidgets.QPushButton(self)
        self.pushButton_SaveProfile.setGeometry(QtCore.QRect(650, 73, 75, 23))
        self.pushButton_SaveProfile.setObjectName("pushButton_SaveProfile")
        self.pushButton_SaveProfile.setText("Save Profile")

        #Profil löschen
        self.pushButton_DeleteProfile = QtWidgets.QPushButton(self)
        self.pushButton_DeleteProfile.setGeometry(QtCore.QRect(650, 125, 75, 23))
        self.pushButton_DeleteProfile.setObjectName("pushButton_DeleteProfile")
        self.pushButton_DeleteProfile.setText("Delete Profile")       
        
        #Fertig mit Eingabe
        self.pushButton_UseProfile = QtWidgets.QPushButton(self)
        self.pushButton_UseProfile.setGeometry(QtCore.QRect(540, 245, 150, 30))
        self.pushButton_UseProfile.setObjectName("pushButton_UseProfile")
        self.pushButton_UseProfile.setText("Speicher Nutzen")         
        
        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmespeicher_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.addItems(names)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)
        self.pushButton_UseProfile.clicked.connect(self.UseProfile)
        
        self.li_inputWidgets = [self.doubleSpinBox_Radius, self.doubleSpinBox_Durchmesser, self.doubleSpinBox_Volumen,
                                self.doubleSpinBox_Hohe,self.spinBox_anzSchichten,self.spinBox_Ladeschicht,
                                self.doubleSpinBox_dickeDammung,self.doubleSpinBox_lamdaDammung]
     
    def UpdateSpeicher(self):
        anz_Schichten = int(self.spinBox_anzSchichten.value())
        if anz_Schichten == 0 or self.t_VL == 0:
            return
        height = 5
        y_base = self.t_VL - height
        p = figure(width=250, height=300,toolbar_location=None)
        p.xaxis.visible = False
        p.yaxis.axis_label = "Speichertemperatur [°C]"

        blue = Color("blue")
        colors = list(blue.range_to(Color("red"),anz_Schichten))
        for i in range(anz_Schichten):
            height_schicht = height / anz_Schichten
            y_draw = y_base + height_schicht/2
            p.rect(x=1, y=y_draw, width= 5, height=height_schicht, fill_color=colors[i].hex_l, line_color = colors[i].hex_l)
            y_base = y_base + height_schicht 
        p.rect(x=1, y=self.t_VL - height/2, width= 5, height=height, line_color = "#000000", fill_alpha = 0)

        html = embed.file_html(p, resources.CDN, "my plot")
        self.WebEngine.setHtml(html)

    def Autocomplete(self):
        radius = self.doubleSpinBox_Radius.value()
        durchmesser = self.doubleSpinBox_Durchmesser.value()
        volumen = self.doubleSpinBox_Volumen.value()
        höhe = self.doubleSpinBox_Hohe.value()  
        
        if radius != 0:
            durchmesser = radius * 2
        elif durchmesser != 0:
            radius = durchmesser / 2

        if radius != 0 and höhe != 0:
            grundfläche = radius * radius * math.pi
            volumen = grundfläche * höhe
        elif radius != 0 and volumen != 0:
            grundfläche = radius * radius * math.pi
            höhe = volumen / grundfläche
        elif höhe !=0 and volumen !=0:
            grundfläche = volumen / höhe
            radius = grundfläche / math.pi
            durchmesser = radius * 2

        self.doubleSpinBox_Radius.setValue(radius)
        self.doubleSpinBox_Durchmesser.setValue(durchmesser)
        self.doubleSpinBox_Volumen.setValue(volumen * 1000)
        self.doubleSpinBox_Hohe.setValue(höhe)

    def SaveProfile(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmespeicher_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        
        name = self.lineEdit_Profil.text()
        #Wenn nichts im Lineedit steht wird das Profil nicht gespeichert
        if name == "":
            return
        

        li_toSave = []
        li_toSave.append(name)      

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
        
        for i,widget in enumerate(self.li_inputWidgets,1):
            try:
                widget.setValue(float(values[i]))
            except TypeError:
                widget.setValue(int(values[i]))
        

    def UseProfile(self):

        self.SaveProfile()

        df = pd.read_csv("./EMS-Frontend/data/Wärmespeicher_Profile.csv", delimiter = ",", encoding='utf-8')
        name = self.comboBox_SelectProfile.currentText()

        data = df[df.values == name].values.flatten().tolist()
        Wärmespeicher = {
            "Art" : self.typ,
            "Radius" : data[1],
            "Durchmesser": data[2],
            "Höhe" : data[3],
            "Volumen" : data[4],
            "anz_Schichten" : data[5],
            "Ladeschicht" : data[6],
            "Dämmdicke" : data[7],
            "Lamda_Dämmung" : data[8],
            }
        Import.importGUI.Import_Speicher(Wärmespeicher)
        #Import.importGUI.Import_Wärmespeicherterie()

    
