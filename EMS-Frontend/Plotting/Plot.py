# -*- coding: utf-8 -*-
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

        
        self.m_output = QtWebEngineWidgets.QWebEngineView()
        lay_Vertical = QtWidgets.QVBoxLayout(self)
        lay_Horizontal = QtWidgets.QHBoxLayout(self)
        self.setLayout(lay_Horizontal)
        lay_Horizontal.addLayout(lay_Vertical,1)
        lay_Horizontal.addWidget(self.m_output,9)
        
        self.pushButton_Test = QtWidgets.QPushButton(self)
        #self.pushButton_Test.setGeometry(QtCore.QRect(350, 180, 75, 23))
        self.pushButton_Test.setObjectName("pushButton_Test")
        self.pushButton_Test.setText("Test")        

        lay_Vertical.addWidget(self.pushButton_Test)

        p = figure(width=800, height=300)
        html = embed.file_html(p, resources.CDN, "my plot")
        self.m_output.setHtml(html)