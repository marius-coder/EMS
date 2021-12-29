# -*- coding: latin-1 -*-
import pandas as pd
import numpy as np
import os
import sys
from bokeh import plotting, embed, resources
from bokeh.plotting import figure
from PyQt5 import *
#from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets


class WindowGesamtprofil(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableWidget()
        self.table.itemChanged.connect(self.UpdatePlot)
        self.table.setColumnCount(2)  # We install three columns
        # Set table headers
        self.table.setHorizontalHeaderLabels(["Profilname", "Anteil Nutzung"])
        # Set tooltips for headers
        self.table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.y_hour = []
        self.y_month = []

        self.m_output = QtWebEngineWidgets.QWebEngineView()
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.m_output)
        lay.addWidget(self.table)
        
        # prepare some data
        self.x = np.linspace(1,24,24)

    def UpdatePlot(self):
        try:
            self.y = [0 for i in range(24)]
            print(self.y)
            for row in range(self.table.rowCount()): 
                temp_y = [element * float(self.table.item(row, 1).text()) / 100 for element in self.y_hour[row]]

                self.y = [a + b for a, b in zip(self.y, temp_y)]

            p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y", width=800, height=300)

            # add a line renderer with legend and line thickness
            p.line(self.x, self.y, legend_label="Temp.", line_width=2)
        
        
            html = embed.file_html(p, resources.CDN, "my plot")
            self.m_output.setHtml(html)
        except Exception as e:
           if e.__class__.__name__ == "AttributeError":
               pass
           else:
               raise




    def AddProfile(self, data):
			#"Profilname" : data[0],
			#"WW-Verbrauch_Stunde [%]" : data[1:25],
           # "WW-Verbrauch_Monat [%]" : data[27:],
			#"Verbrauchsart" : data[25:27],
        
        self.y_hour.append(data["WW-Verbrauch_Stunde [%]"])
        self.y_month.append(data["WW-Verbrauch_Monat [%]"])
        #row = [data["Profilname"], 10]
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(data["Profilname"]))
        self.table.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem("100"))
        self.table.resizeColumnsToContents()

        self.UpdatePlot()
       