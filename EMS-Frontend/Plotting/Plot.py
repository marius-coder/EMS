# -*- coding: latin-1 -*-
import os
import sys
from bokeh.models.widgets.tables import SelectEditor
import pandas as pd
import numpy as np
import csv
from bokeh import plotting, embed, resources
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Legend
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
        self.dlgColorWindow = ColorPickWindow(self)
        self.move = True
        self.model = None
        
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
        self.selectionList = []
        self.selectionGroup = []
        self.DataPoints_Gebäude = {"Innentemperatur [°C]" : None,
                              "Außentemperatur [°C]" : None,
                              "Solltemperatur [°C]" : None,
                              "Strombedarf [kW]" : None,
                              "Bedarf Heizen [kW]" : None,
                              "Bedarf Kühlen [kW]" : None,
                              "Bedarf Warmwasser [kW]" : None,
                              "Transmissionsverluste [kW]" : None,
                              "Lüftungsverluste [kW]" : None,
                              "Solare Gewinne [kW]" : None,
                              "Innere Gewinne (Personen) [kW]" : None,
                              "Innere Gewinne (Maschinen) [kW]" : None,
                              "Innere Gewinne (Beleuchtung) [kW]" : None}

        self.DataPoints_Warmwasser = {"WP_Wärmeleistung [kW]" : None,
                                   "Speicherstand [%]" : None,
                                   "WP_Status" : None,
                                   "WP_Stromverbrauch" : None,
                                   "Mittlere Speichertemperatur [°C]" : None,
                                   "COP" : None}
        self.DataPoints_Heizen_Kühlen = {"WP_Wärmeleistung [kW]" : None,
                                   "Speicherstand [%]" : None,
                                   "WP_Status" : None,
                                   "WP_Stromverbrauch" : None,
                                   "Mittlere Speichertemperatur [°C]" : None,
                                   "COP" : None}
        self.DataPoints_Strom = { 
            "PV-Ertrag [kW]" : None,
            "Batteriekapazität [%]" : None,
            "Batteriekapazität [kWh]" : None,            
            "Batterieeinspeisung [kW]" : None,
            "Batterieentladung [kW]" : None,
            "Netzeinspeisung [kW]" : None,
            "Netzbezug [kW]" : None,}
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

    def SetupModel(self):
        if self.model == None:
            return

        #Heizen + Warmwasser
        li_WP = [self.DataPoints_Heizen_Kühlen,self.DataPoints_Warmwasser]
        li_var = ["HZG","WW"]
        for i,WP in enumerate(li_WP):            
            print(getattr(self.model, "WP_" + li_var[i]))
            print(getattr(self.model, "WP_" + li_var[i]).speicher)
            WP["WP_Status"] = getattr(self.model, "WP_" + li_var[i]).is_on 
            WP["WP_Stromverbrauch"] = getattr(self.model, "WP_" + li_var[i]).Pel_Betrieb
            WP["WP_Wärmeleistung [kW]"] = getattr(self.model, "WP_" + li_var[i]).Pel_Betrieb * getattr(self.model, "WP_" + li_var[i]).COP_betrieb
            WP["Speicherstand [%]"] = getattr(self.model, "WP_" + li_var[i]).speicher.ladezustand
            WP["Mittlere Speichertemperatur [°C]"] = getattr(self.model, "WP_" + li_var[i]).speicher.t_mean
            WP["COP"] = getattr(self.model, "WP_" + li_var[i]).COP_betrieb

        #Gebäude
        self.DataPoints_Gebäude["Innentemperatur [°C]"] = self.model.ti
        self.DataPoints_Gebäude["Außentemperatur [°C]"] = self.model.ta
        self.DataPoints_Gebäude["Solltemperatur [°C]"] = self.model.t_soll
        self.DataPoints_Gebäude["Strombedarf [kW]"] = self.model.Pel_gebäude / 1000
        self.DataPoints_Gebäude["Bedarf Heizen [kW]"] = self.model.qh / 1000
        self.DataPoints_Gebäude["Bedarf Kühlen [kW]"] = self.model.qc / 1000
        self.DataPoints_Gebäude["Bedarf Warmwasser [kW]"] = self.model.q_warmwater / 1000
        self.DataPoints_Gebäude["Transmissionsverluste [kW]"] = self.model.qt / 1000
        self.DataPoints_Gebäude["Lüftungsverluste [kW]"] = self.model.qv / 1000
        self.DataPoints_Gebäude["Solare Gewinne [kW]"] = self.model.qs / 1000
        self.DataPoints_Gebäude["Innere Gewinne (Personen) [kW]"] = self.model.q_personen / 1000
        self.DataPoints_Gebäude["Innere Gewinne (Maschinen) [kW]"] = self.model.q_maschinen / 1000
        self.DataPoints_Gebäude["Innere Gewinne (Beleuchtung) [kW]"] = self.model.q_beleuchtung / 1000

        


        #Strom
        self.DataPoints_Strom["PV-Ertrag [kW]"] = self.model.Stromnetz.PV_Anlage.PV_EK
        li_temp = np.ones(8760) *  self.model.Stromnetz.Batterie.Kapazität_MAX
        self.DataPoints_Strom["Batteriekapazität [%]"] = (self.model.Stromnetz.Batterieladung / li_temp) * 100 
        self.DataPoints_Strom["Batteriekapazität [kWh]"] = self.model.Stromnetz.Batterieladung
        self.DataPoints_Strom["Batterieeinspeisung [kW]"] = self.model.Stromnetz.Batterieeinspeisung
        self.DataPoints_Strom["Batterieentladung [kW]"] = self.model.Stromnetz.Batterieentladung
        self.DataPoints_Strom["Netzeinspeisung [kW]"] = self.model.Stromnetz.Netzeinspeisung
        self.DataPoints_Strom["Netzbezug [kW]"] = self.model.Stromnetz.Netzbezug


    def OpenDialog(self): 
        if self.sender().objectName() == "pushButton_ResetPlots":
            self.dlgWindow.sender = "Reset"
        else:
            self.dlgWindow.sender = "Draw"
        print(self.dlgWindow.sender)
        for button in self.dlgWindow.btn_grp.buttons():
            button.setStyleSheet('background-color: red')
            button.setChecked(False)

        selection = self.ListWidget_DataPoints.selectedItems()
        for item in selection:
            self.selectionList.append(item.text())
            self.selectionGroup.append(self.comboBox_SelectDatagroup.currentText())

        self.dlgColorWindow.SetupSelection(self.selectionList)
        self.dlgColorWindow.show()
        self.dlgWindow.show()
        if self.move == True:
            self.move = False
            x = self.dlgColorWindow.pos().x() + self.dlgWindow.frameGeometry().width()
            y = self.dlgColorWindow.pos().y()
            self.dlgColorWindow.move(x+30,y)


        

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

    #def UpdateSelection(self):
    #    selection = self.ListWidget_DataPoints.selectedItems()

    def SetTimeframe(self):
        if self.radioButton_Stunde.isChecked() == True:
            self.x_timeframe = "h"
        elif self.radioButton_Tag.isChecked() == True:
            self.x_timeframe = "d"
        elif self.radioButton_Monat.isChecked() == True:
            self.x_timeframe = "m"
        elif self.radioButton_Jahr.isChecked() == True:
            self.x_timeframe = "y"

    def DrawPlot(self):        

        time = np.arange('2022-01-01', '2023-01-01', dtype='datetime64[h]')

        df = pd.DataFrame(index = time)            
        
        for i,item in enumerate(self.selectionList):
            df[item] = getattr(self,"DataPoints_" + self.selectionGroup[i])[item]
            
        mypalette = self.dlgColorWindow.li_Colors
        
        if len(self.dlgWindow.idList) != 1:
            self.selectionList = []
            self.selectionGroup = []
            self.ListWidget_DataPoints.clearSelection()
            return
        ID = self.dlgWindow.idList[0]
        legend_it = []
        p = figure(width=800, height=450, x_axis_type='datetime')
        for i,column in enumerate(df):
            c = p.line(x = df.index.values, y = df[column].values,
                   line_color = mypalette[i], line_width = 2)
            legend_it.append((self.selectionList[i], [c]))

        p.xaxis.ticker.desired_num_ticks = 12
        legend = Legend(items = legend_it)
        legend.click_policy = "mute"
        p.add_layout(legend, 'below')
        p.legend.orientation = "horizontal"

        html = embed.file_html(p, resources.CDN, "my plot")
        self.li_plots[ID]["Widget"].setHtml(html)
        self.selectionList = []
        self.selectionGroup = []
        self.ListWidget_DataPoints.clearSelection()
        

    def LoadDatagroup(self):
        selection = self.ListWidget_DataPoints.selectedItems()
        for item in selection:
            self.selectionList.append(item.text())
            self.selectionGroup.append(self.comboBox_SelectDatagroup.currentText())
        name = self.comboBox_SelectDatagroup.currentText()
        Datapoints = getattr(self,"DataPoints_" + name)
        self.ListWidget_DataPoints.clear()
        self.ListWidget_DataPoints.addItems(Datapoints.keys())

        
class ColorPickWindow(QWidget):
    def __init__(self, parent):
        super(ColorPickWindow, self).__init__()

        self.height = 50
        self.resize(450,self.height)        
        self.setWindowTitle("Farben auswählen für Plot")
        self.sender = ""
        self.parent = parent                
        self.lay_Vertical = QtWidgets.QVBoxLayout(self)
        self.li_Widgets = []
        self.btn_grp = QButtonGroup()
        self.btn_grp.buttonClicked.connect(self.SetColor)
        self.btn_grp.setExclusive(False)
        

    def deleteItemsOfLayout(self,layout):
         if layout is not None:
             while layout.count():
                 item = layout.takeAt(0)
                 widget = item.widget()
                 if widget is not None:
                     widget.setParent(None)
                 else:
                     self.deleteItemsOfLayout(item.layout())


    def SetupSelection(self, selection):
        self.height = 50
        self.deleteItemsOfLayout(self.lay_Vertical)
        self.btn_grp = QButtonGroup()
        self.btn_grp.buttonClicked.connect(self.SetColor)
        self.btn_grp.setExclusive(False)
        self.li_Widgets = []
        self.li_Colors = []

        for i,item in enumerate(selection):
            lay_horizontal = QtWidgets.QHBoxLayout(self)

            lineEdit_Selection = QtWidgets.QLineEdit(self)
            lineEdit_Selection.setReadOnly(True)
            lineEdit_Selection.setText(item)
            lay_horizontal.addWidget(lineEdit_Selection,5)

            lineEdit_Color = QtWidgets.QLineEdit(self)
            lineEdit_Color.setReadOnly(True)
            lay_horizontal.addWidget(lineEdit_Color,3)

            pushButton_PickColor = QtWidgets.QPushButton(self)
            pushButton_PickColor.setText("Color")
            pushButton_PickColor.setCheckable(True)
            lay_horizontal.addWidget(pushButton_PickColor,2)
            dic_temp = {
                "Selection" : lineEdit_Selection,
                "Color" : lineEdit_Color,
                "Pick_Color" : pushButton_PickColor,
                    }
            self.li_Widgets.append(dic_temp)

            self.height += 40
            self.resize(450,self.height)  

            self.lay_Vertical.addLayout(lay_horizontal)
            self.btn_grp.addButton(self.li_Widgets[i]["Pick_Color"],i)
            self.li_Colors.append("#ffffff")
        
    def SetColor(self, btn):
        for i,button in enumerate(self.btn_grp.buttons()):
            if button.isChecked():
                ID = int(i)

        color = QColorDialog.getColor().name()
        self.li_Widgets[ID]["Color"].setStyleSheet('background-color:'+color) 
        self.li_Colors[ID] = color
        btn.setCheckable(False)
        btn.setCheckable(True)

        

            
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
        self.parent.dlgColorWindow.close()

    def colorChange(self, btn):  
        color = btn.palette().color(QtGui.QPalette.Background).name()

        if color == "#ff0000":
            btn.setStyleSheet('background-color: green')            
        else :
            btn.setStyleSheet('background-color: red')

        self.idList = []
        for i,button in enumerate(self.btn_grp.buttons()):
            if button.isChecked():
                self.idList.append(i)