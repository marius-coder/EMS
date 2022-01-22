# -*- coding: latin-1 -*-
import os
import sys
import pandas as pd
import csv
from bokeh import plotting, embed, resources
from bokeh.plotting import figure
import importlib
Import = importlib.import_module("EMS-Backend.Classes.Import")
import warnings
warnings.filterwarnings("error")

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Plotting(QWidget):

    def __init__(self, parent):
        super(Ui_Plotting, self).__init__()
        
        self.parent = parent
        self.setObjectName("self")
        self.resize(601, 254)
        self.setWindowTitle("Ergebnisse")

        self.dlgWindow = DialogWindow(self)
        
        self.lay_base = QtWidgets.QHBoxLayout(self)
        self.lay_Vertical = QtWidgets.QVBoxLayout(self)
        self.lay_Grid = QtWidgets.QGridLayout(self)

        self.setLayout(self.lay_base)
        self.lay_base.addLayout(self.lay_Vertical,1)
        self.lay_base.addLayout(self.lay_Grid,9)    

        self.pushButton_ResetPlots = QtWidgets.QPushButton(self)
        self.pushButton_ResetPlots.setText("Reset Plots") 
        self.pushButton_ResetPlots.setObjectName("pushButton_ResetPlots")
        self.pushButton_ResetPlots.clicked.connect(self.OpenDialog)
        self.lay_Vertical.addWidget(self.pushButton_ResetPlots)

        self.label_AuswahlDatagroup = QtWidgets.QLabel(self)
        self.label_AuswahlDatagroup.setText("Auswahl Profil")
        self.lay_Vertical.addWidget(self.label_AuswahlDatagroup)
        self.comboBox_SelectDatagroup = QtWidgets.QComboBox(self)
        self.comboBox_SelectDatagroup.activated.connect(self.LoadDatagroup)
        self.lay_Vertical.addWidget(self.comboBox_SelectDatagroup)
        li_DataGroup = ["Gebäude","Warmwasser","Heizen_Kühlen","Strom","Erdwärme","Energiedaten"]
        self.comboBox_SelectDatagroup.addItems(li_DataGroup)

        self.ListWidget_DataPoints = QListWidget()
        self.ListWidget_DataPoints.setSelectionMode(QAbstractItemView.MultiSelection)
        self.lay_Vertical.addWidget(self.ListWidget_DataPoints)
        self.DataPoints_Gebäude = {"Innentemperatur" : 0,
                              "Außentemperatur" : 1,
                              "Solltemperatur" : 2,
                              }
        self.DataPoints_Warmwasser = {"Bedarf [liter]" : 0,
                                 "Bedarf [kW]" : 1,                                 
                                 "Speicherstand [kW]" : 2,
                                 "WP_Status" : 3,
                                 "WP Stromverbrauch" : 4
            }
        self.DataPoints_Heizen_Kühlen = {"Bedarf [kW]" : 0,
                                   "Speicherstand [kW]" : 1,
                                   "WP_Status" : 2,
                                   "WP Stromverbrauch" : 3}
        self.DataPoints_Strom = {}
        self.DataPoints_Erdwärme = {}
        self.DataPoints_Energiedaten = {}

        self.lay_GridRadiobuttons = QtWidgets.QGridLayout(self)
        self.radioButton_Stunde = QtWidgets.QRadioButton(self)
        self.radioButton_Stunde.setText("Stunde")
        self.radioButton_Stunde.setChecked(True)
        self.lay_GridRadiobuttons.addWidget(self.radioButton_Stunde,0,0)
        self.radioButton_Tag = QtWidgets.QRadioButton(self)
        self.radioButton_Tag.setText("Tag")
        self.lay_GridRadiobuttons.addWidget(self.radioButton_Tag,0,1)
        self.radioButton_Monat = QtWidgets.QRadioButton(self)
        self.radioButton_Monat.setText("Monat")
        self.lay_GridRadiobuttons.addWidget(self.radioButton_Monat,1,0)
        self.radioButton_Jahr = QtWidgets.QRadioButton(self)
        self.radioButton_Jahr.setText("Jahr")
        self.lay_GridRadiobuttons.addWidget(self.radioButton_Jahr,1,1)
        self.lay_Vertical.addLayout(self.lay_GridRadiobuttons)   

        self.pushButton_ResetSelection = QtWidgets.QPushButton(self)
        self.pushButton_ResetSelection.setText("Reset Selection") 
        self.pushButton_ResetSelection.clicked.connect(self.AddFigure)
        self.lay_Vertical.addWidget(self.pushButton_ResetSelection)

        self.pushButton_DisplayPlot = QtWidgets.QPushButton(self)
        self.pushButton_DisplayPlot.setText("Draw Plot") 
        self.pushButton_DisplayPlot.clicked.connect(self.OpenDialog)
        self.lay_Vertical.addWidget(self.pushButton_DisplayPlot)

        self.li_plots = [None,None,None,None]
        self.li_coords = [[0,0],[0,1],[1,0],[1,1]]
        for i in range(len(self.li_coords)):
            self.AddFigure(i)

    def OpenDialog(self): 
        if self.sender().objectName() == "pushButton_ResetPlots":
            self.dlgWindow.sender = "Reset"
        else:
            self.dlgWindow.sender = "Draw"
        print(self.dlgWindow.sender)
        for button in self.dlgWindow.btn_grp.buttons():
            button.setStyleSheet('background-color: red')
            button.setChecked(False)
        self.dlgWindow.show()
        

    def AddFigure(self,i): 
        webView = QtWebEngineWidgets.QWebEngineView()
        checkBox = QtWidgets.QCheckBox()
        p = figure(width=800, height=450)
        html = embed.file_html(p, resources.CDN, "my plot")
        webView.setHtml(html)
        dic_Plot = {
            "Widget" : webView,
            "Figure" : p,
            "html" : html,
            "checkBox" : checkBox
            }

        self.lay_Grid.addWidget(webView, self.li_coords[i][0], self.li_coords[i][1])
        self.li_plots[i] = dic_Plot

    def ResetPlots(self):        
        for item in self.dlgWindow.idList:
            self.AddFigure(item)
            print("Reset id: ", item)

    def DrawPlot(self):
        
        if len(self.dlgWindow.idList) != 1:
            return
        ID = self.dlgWindow.idList[0]
        print("Drawing in Slot: ", ID)
        p = figure(width=800, height=450)
        p.rect(x=1, y=2, width= 5, height=50, fill_color= "red")
        html = embed.file_html(p, resources.CDN, "my plot")
        self.li_plots[ID]["Widget"].setHtml(html)
        

    def LoadDatagroup(self):
        name = self.comboBox_SelectDatagroup.currentText()
        Datapoints = getattr(self,"DataPoints_" + name)
        self.ListWidget_DataPoints.clear()
        self.ListWidget_DataPoints.addItems(Datapoints.keys())



            
class DialogWindow(QWidget):
    def __init__(self, parent):
        super(DialogWindow, self).__init__()
        self.resize(400, 100)
        self.setWindowTitle("Plots auswählen")
        self.sender = ""
        self.lay_Grid = QtWidgets.QGridLayout(self)
        
        li_coords = [[0,0],[0,1],[1,0],[1,1]]
        self.parent = parent
        self.btn_grp = QButtonGroup()
        self.btn_grp.buttonClicked.connect(self.colorChange)
        self.btn_grp.setExclusive(False)
        self.li_Buttons = []        
        
        for i in range(4):
            pushButton_Plot = QtWidgets.QPushButton(self)
            pushButton_Plot.setText(f"Plot: {i+1}")
            pushButton_Plot.setStyleSheet("QPushButton { background-color: gray; }\n"
                                        "QPushButton:enabled { background-color: red; }\n") 
            pushButton_Plot.setCheckable(True)
            self.li_Buttons.append(pushButton_Plot)

        for i in range(4):
            self.lay_Grid.addWidget(self.li_Buttons[i],li_coords[i][0], li_coords[i][1])
            self.btn_grp.addButton(self.li_Buttons[i],i)

        self.pushButton_Confirm = QtWidgets.QPushButton(self)
        self.pushButton_Confirm.setText("Fertig")
        self.lay_Grid.addWidget(self.pushButton_Confirm, 2, 0,QtCore.Qt.AlignCenter,2)
        self.pushButton_Confirm.clicked.connect(self.Confirm)

    def Confirm(self):
        if self.sender == "Reset":
            self.parent.ResetPlots()
        else:
            self.parent.DrawPlot()
        self.close()


    def colorChange(self, btn):  
        color = btn.palette().color(QtGui.QPalette.Background).name()

        if color == "#ff0000":
            btn.setStyleSheet('background-color: green')            
        else :
            btn.setStyleSheet('background-color: red')

        self.idList = []
        for id,button in enumerate(self.btn_grp.buttons()):
            if button.isChecked():
                self.idList.append(id)

        #print("Clicked Buttons: ", self.idList)
            
            