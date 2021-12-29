# -*- coding: latin-1 -*-
import pandas as pd
import numpy as np
import os
import sys
from bokeh import plotting, embed, resources
from bokeh.plotting import figure
from bokeh.models import HoverTool, DataRange1d
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
        #Zwischenvariablen
        self.y_hour = []
        self.y_month = []

        #Layout
        self.m_output = QtWebEngineWidgets.QWebEngineView()
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.m_output)
        lay.addWidget(self.table)

        #Radiobuttons fürs umschalten zwischen Stunden und Monatsbetrachtung
        self.radioButton_hour = QtWidgets.QRadioButton(self)
        self.radioButton_hour.setGeometry(QtCore.QRect(20, 8, 82, 17))
        self.radioButton_hour.setObjectName("radioButton_hour")
        self.radioButton_hour.setText("Stunde")
        self.radioButton_month = QtWidgets.QRadioButton(self)
        self.radioButton_month.setGeometry(QtCore.QRect(80, 8, 82, 16))
        self.radioButton_month.setObjectName("radioButton_month")
        self.radioButton_month.setText("Monat")      
        self.radioButton_hour.toggled['bool'].connect(self.radioButton_month.repaint)
        self.radioButton_hour.toggled['bool'].connect(self.UpdatePlot)
        self.radioButton_month.toggled['bool'].connect(self.radioButton_hour.repaint)
        self.radioButton_month.toggled['bool'].connect(self.UpdatePlot)
        
        #lineEdit in der die Summen angegeben sind zur Kontrolle
        self.lineEdit_SumNutzung = QtWidgets.QLineEdit(self)
        self.lineEdit_SumNutzung.setGeometry(QtCore.QRect(160, 8, 50, 20))
        self.lineEdit_SumNutzung.setReadOnly(True)

    def UpdatePlot(self):
        try:
            if self.radioButton_month.isChecked():
                y_choose = self.y_month
                self.x = np.linspace(1,12,12)
                str_var = "Monat"

            else:
                y_choose = self.y_hour
                self.x = np.linspace(1,24,24)
                str_var = "Stunde"



            self.y = [0 for i in range(24)]
            sum_Nutzung = 0
            for row in range(self.table.rowCount()): 
                sum_Nutzung += float(self.table.item(row, 1).text())
                temp_y = [element * float(self.table.item(row, 1).text()) / 100 for element in y_choose[row]]

                self.y = [a + b for a, b in zip(self.y, temp_y)]

            self.lineEdit_SumNutzung.setText(str(sum_Nutzung) + "%")
            
            hover_tool = HoverTool(tooltips=[
            ("x", "@x"),
            ("y", "$y"),
                ])  
            hover_tool.point_policy='snap_to_data'
  
            p = figure(title="Gesamtprofil " + str_var, x_axis_label="Stunde", y_axis_label="Verbrauch [%]", width=800, height=300,
                       tools=[hover_tool,"pan,wheel_zoom,box_zoom,reset,save"], y_range=DataRange1d(start=0))

          
            # add a line renderer with legend and line thickness
            p.line(self.x, self.y, line_width=2)
            #p.legend.visible = False
        
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
       