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
        
        self.lay_base = QtWidgets.QHBoxLayout(self)
        self.lay_Vertical = QtWidgets.QVBoxLayout(self)
        self.lay_Grid = QtWidgets.QGridLayout(self)

        self.setLayout(self.lay_base)
        self.lay_base.addLayout(self.lay_Vertical,1)
        self.lay_base.addLayout(self.lay_Grid,9)    

        self.pushButton_ResetPlots = QtWidgets.QPushButton(self)
        self.pushButton_ResetPlots.setText("Reset Plots") 
        self.pushButton_ResetPlots.clicked.connect(self.OpenDialog)
        self.lay_Vertical.addWidget(self.pushButton_ResetPlots)

        self.label_AuswahlDatagroup = QtWidgets.QLabel(self)
        self.label_AuswahlDatagroup.setText("Auswahl Profil")
        self.lay_Vertical.addWidget(self.label_AuswahlDatagroup)
        self.comboBox_SelectProfile = QtWidgets.QComboBox(self)
        self.lay_Vertical.addWidget(self.comboBox_SelectProfile)

        self.ListWidget_DataPoints = QListWidget()
        self.ListWidget_DataPoints.setSelectionMode(QAbstractItemView.MultiSelection)
        self.ListWidget_DataPoints.addItem("Item 1")
        self.ListWidget_DataPoints.addItem("Item 2")
        self.ListWidget_DataPoints.addItem("Item 3")
        self.ListWidget_DataPoints.addItem("Item 4")
        self.lay_Vertical.addWidget(self.ListWidget_DataPoints)

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
        self.pushButton_DisplayPlot.clicked.connect(self.AddFigure)
        self.lay_Vertical.addWidget(self.pushButton_DisplayPlot)

        self.li_plots = []
        self.AddFigure()

    def OpenDialog(self):
        self.dlgWindow = DialogWindow()
        self.dlgWindow.show()
        

    def AddFigure(self): 
        
        li_coords = [[0,0],[0,1],[1,0],[1,1]]

        for i in range(len(li_coords)):


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

            self.lay_Grid.addWidget(webView, li_coords[i][0], li_coords[i][1])
            self.li_plots.append(dic_Plot)    

       
            
class DialogWindow(QWidget):
    def __init__(self):
        super(DialogWindow, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("Plots auswählen")

        self.lay_Grid = QtWidgets.QGridLayout(self)
        
        li_coords = [[0,0],[0,1],[1,0],[1,1]]
       
        self.btn_grp = QButtonGroup()
        self.btn_grp.buttonClicked.connect(self.colorChange)
           
        self.li_Buttons = []
        
        for i in range(4):
            pushButton_PLot = QtWidgets.QPushButton(self)
            pushButton_PLot.setText(f"Plot: {i+1}")
            pushButton_PLot.setStyleSheet("QPushButton { background-color: gray; }\n"
                                        "QPushButton:enabled { background-color: red; }\n") 
            self.li_Buttons.append(pushButton_PLot)

        for i in range(4):
            self.lay_Grid.addWidget(self.li_Buttons[i],li_coords[i][0], li_coords[i][1])
            self.btn_grp.addButton(self.li_Buttons[i])           

    def colorChange(self, btn):        
        color = btn.palette().color(QtGui.QPalette.Background).name()
        if color == "#ff0000":
            btn.setStyleSheet('background-color: green')            
        else :
            btn.setStyleSheet('background-color: red')

            
            