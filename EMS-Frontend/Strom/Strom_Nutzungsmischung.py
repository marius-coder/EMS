# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import sys
from bokeh import plotting, embed, resources
from bokeh.plotting import figure
from bokeh.models import HoverTool, DataRange1d
import importlib
Import = importlib.import_module("EMS-Backend.Classes.Import")
from PyQt5 import *
#from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets


class WindowGesamtprofil_Strombedarf(QWidget):
    #Eigenes Signal definieren
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    #Dieses Signal erkennt ob ein Tastaturkey gedrückt worden ist 
    def keyPressEvent(self, event):
        super(WindowGesamtprofil_Strombedarf, self).keyPressEvent(event)
        self.keyPressed.emit(event) 

    #on_key kontrolliert welche Taste gedrückt worden ist und löscht den gewählten eintrag in der Tabelle
    def on_key(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            indices = self.table.selectionModel().selectedRows() 
            for index in sorted(indices):
                #Falls alle indices gleichzeitig ausgewählt sind beim löschen, gibts nen Error -> deswegen "pass"
                #damit das programm nicht abstürzt
                try:
                    self.table.removeRow(index.row()) 
                    del self.y_hour[index.row()]
                    del self.y_month[index.row()]
                except Exception as e:
                    if e.__class__.__name__ == "AttributeError":                    
                        pass
            self.UpdatePlot()


    def __init__(self, parent):
        super(WindowGesamtprofil_Strombedarf, self).__init__()

        self.parent = parent
        self.keyPressed.connect(self.on_key)
        self.setWindowTitle("Strom_Nutzungsmischung")
        self.table = QtWidgets.QTableWidget()
        self.table.itemChanged.connect(self.UpdatePlot)
        self.table.setColumnCount(6)  # We install six columns
        # Set table headers
        self.table.setHorizontalHeaderLabels(["Profilname", "Anteil Fläche [%]", "kWh/m²a","kWh/a", "Stückanzahl", "kW/Stück"])
        #connect Signal
        self.keyPressed.connect(self.on_key)

        #Zwischenvariablen
        self.y_hour = []
        self.y_month = []

        #Layout
        self.m_output = QtWebEngineWidgets.QWebEngineView()
        lay = QtWidgets.QVBoxLayout(self)
        self.setLayout(lay)
        lay.addWidget(self.m_output,6)
        
        verticalSpacer = QtWidgets.QSpacerItem(10, 45, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        lay.addItem(verticalSpacer)
        lay.addWidget(self.table,3)
        #Wir müssen die Figur vorrendern damit der PLot immer dargestellt wird
        p = figure(width=800, height=300)
        html = embed.file_html(p, resources.CDN, "my plot")
        self.m_output.setHtml(html)

        #Radiobuttons fürs umschalten zwischen Stunden und Monatsbetrachtung
        self.radioButton_hour = QtWidgets.QRadioButton(self)
        self.radioButton_hour.setGeometry(QtCore.QRect(20, 330, 82, 17))    
        self.radioButton_hour.setText("Stunde")
        self.radioButton_hour.setChecked(True)
        self.radioButton_month = QtWidgets.QRadioButton(self)
        self.radioButton_month.setGeometry(QtCore.QRect(20, 345, 82, 16))    
        self.radioButton_month.setText("Monat")      
        self.buttonGroup_Time = QtWidgets.QButtonGroup(self)
        self.buttonGroup_Time.setObjectName("buttonGroup_Time")
        self.buttonGroup_Time.addButton(self.radioButton_hour)
        self.buttonGroup_Time.addButton(self.radioButton_month)
        self.radioButton_hour.toggled['bool'].connect(self.UpdatePlot)
        self.radioButton_month.toggled['bool'].connect(self.UpdatePlot)

        #Radiobuttons fürs umschalten zwischen Prozentualer und Absoluter Verbrauchsdarstellung
        self.radioButton_Percent = QtWidgets.QRadioButton(self)
        self.radioButton_Percent.setGeometry(QtCore.QRect(80, 330, 150, 17))        
        self.radioButton_Percent.setText("Darstellung Prozent")
        self.radioButton_Percent.setChecked(True)
        self.radioButton_Absolute = QtWidgets.QRadioButton(self)
        self.radioButton_Absolute.setGeometry(QtCore.QRect(80, 345, 150, 16))        
        self.radioButton_Absolute.setText("Darstellung Absolut")     
        self.buttonGroup_Type = QtWidgets.QButtonGroup(self)
        self.buttonGroup_Type.setObjectName("buttonGroup_Type")
        self.buttonGroup_Type.addButton(self.radioButton_Percent)
        self.buttonGroup_Type.addButton(self.radioButton_Absolute)
        self.radioButton_Percent.toggled['bool'].connect(self.UpdatePlot)
        self.radioButton_Absolute.toggled['bool'].connect(self.UpdatePlot)

        #Eingabe Gesamtfläche
        self.label_Hourly = QtWidgets.QLabel(self)
        self.label_Hourly.setGeometry(QtCore.QRect(200, 324, 200, 30))
        self.label_Hourly.setText("Gesamtfläche [m²]")
        self.lineEdit_Fläche = QtWidgets.QLineEdit(self)
        self.lineEdit_Fläche.setGeometry(QtCore.QRect(290, 330, 50, 20))
        self.lineEdit_Fläche.setText("0")
        self.lineEdit_Fläche.textChanged.connect(self.UpdatePlot)
        #lineEdit in der die Summen angegeben sind zur Kontrolle
        self.label_Hourly = QtWidgets.QLabel(self)
        self.label_Hourly.setGeometry(QtCore.QRect(200, 344, 200, 30))
        self.label_Hourly.setText("Nutzung [%]")
        self.lineEdit_SumNutzung = QtWidgets.QLineEdit(self)
        self.lineEdit_SumNutzung.setGeometry(QtCore.QRect(290, 350, 50, 20))
        self.lineEdit_SumNutzung.setReadOnly(True)
        self.lineEdit_SumNutzung.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : lightgrey;"
                                    "}")
        #Nutzungsmischung verwenden
        self.pushButton_UseNutzungsmischung = QtWidgets.QPushButton(self)
        self.pushButton_UseNutzungsmischung.setGeometry(QtCore.QRect(350, 345, 180, 25))
        self.pushButton_UseNutzungsmischung.setObjectName("pushButton_UseNutzungsmischung")
        self.pushButton_UseNutzungsmischung.setText("Nutzungsmischung verwenden")
        self.pushButton_UseNutzungsmischung.clicked.connect(self.UseNutzungsmischung)
        self.pushButton_UseNutzungsmischung.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}") 


       

    def CalcStrom_KWHproFlächeJahr(self,row):
        #Rechnung mit kWh/m²a
        percent_consumption = float(self.table.item(row, 1).text())
        Fläche = float(self.lineEdit_Fläche.text())
        kWhproFläche = float(self.table.item(row, 2).text()) / 365
        y_temp = [element / 100 * percent_consumption / 100 * Fläche * kWhproFläche  for element in self.y_choose[row]]
        return y_temp

    def CalcStrom_KWHproJahr(self,row):
        #Rechnung mit kWh/a
        percent_consumption = float(self.table.item(row, 1).text())
        kWhproJahr = float(self.table.item(row, 3).text()) / 365
        y_temp = [element / 100 * percent_consumption / 100 * kWhproJahr  for element in self.y_choose[row]]
        return y_temp

    def CalcStrom_KWHproStück(self,row):
        #Rechnung mit kW/Stück
        percent_consumption = float(self.table.item(row, 1).text())
        kW = float(self.table.item(row, 5).text())
        anz_Verbraucher = float(self.table.item(row, 4).text())
        y_temp = [element / 100 * percent_consumption / 100 * anz_Verbraucher * kW  for element in self.y_choose[row]]
        return y_temp

    def CalcStrom_Prozent(self,row):
        y_temp = [element * float(self.table.item(row, 1).text()) / 100 for element in self.y_choose[row]]
        return y_temp

    
    def UseNutzungsmischung(self):
        if self.table.rowCount() == 0:
            return
        Strom_Gesamt = {}
        Strom_temp = [0 for i in range(24)]
        self.y_choose = self.y_month
        for row in range(self.table.rowCount()): 

            #Input Validation ob alle Werte Zahlen sind
            if is_number_tryexcept(self.lineEdit_Fläche.text()) and is_number_tryexcept(self.table.item(row, 1).text()) and is_number_tryexcept(self.table.item(row, 4).text()):
                if self.table.item(row, 2).text() != "None":
                    #Rechnung mit kWh/m²a
                    y_temp = self.CalcStrom_KWHproFlächeJahr(row)                                                        
                elif self.table.item(row, 3).text() != "None":
                    #Rechnung mit kWh/a
                    y_temp = self.CalcStrom_KWHproJahr(row)   
                elif self.table.item(row, 5).text() != "None":
                    #Rechnung mit kW/Stück
                    y_temp = self.CalcStrom_KWHproStück(row)  
                    
                Strom_temp = [a + b for a, b in zip(Strom_temp, y_temp)]
            else:
                return

        Strom_Gesamt["month [kWh]"] = [element * 365 for element in Strom_temp]
        #Prozent berechnen
        Strom_temp_percent = [0 for i in range(24)]
        self.y_choose = self.y_hour
        for row in range(self.table.rowCount()): 
            y_temp_percent = self.CalcStrom_Prozent(row)
            Strom_temp_percent = [a + b for a, b in zip(Strom_temp_percent, y_temp_percent)]
        Strom_Gesamt["percent [%/h]"] = Strom_temp_percent
        li_daysperMonth = [31,28,31,30,31,30,31,31,30,31,30,31]

        Strom_Gesamt["hour [kWh/h]"] = []
        for i,value in enumerate(Strom_Gesamt["month [kWh]"]):
            li_temp = []
            strom_daily = value / li_daysperMonth[i]
            for percent in Strom_Gesamt["percent [%/h]"]:
                
                li_temp.append(percent/100 * strom_daily)
            Strom_Gesamt["hour [kWh/h]"].append(li_temp)
        Import.importGUI.Import_Strombedarf(Strom_Gesamt)
        self.pushButton_UseNutzungsmischung.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        self.parent.lineEdit_Strombedarf.setText("Nutzungsmischung Fertig")



    def UpdatePlot(self):
        fläche = self.parent.Gebäude.doubleSpinBox_BGF.value()
        self.lineEdit_Fläche.setText(str(fläche))
        try:
            if self.radioButton_month.isChecked():
                self.y_choose = self.y_month
                self.x = np.linspace(1,12,12)
                str_xvar = "Monat"
                str_yvar = ""
                

            else:
                self.y_choose = self.y_hour
                self.x = np.linspace(1,24,24)
                str_xvar = "Stunde"
                str_yvar = ""

            
            self.y = [0 for i in range(24)]
            sum_Nutzung = 0
            #Alle Zeilen der Tabelle werden durchgegangen
            for row in range(self.table.rowCount()): 

                #Input Validation ob alle Werte Zahlen sind
                if is_number_tryexcept(self.lineEdit_Fläche.text()) and is_number_tryexcept(self.table.item(row, 1).text()) and is_number_tryexcept(self.table.item(row, 4).text()):

                    #Zuerst wird kontrolliert ob der Bedarf Absolut oder in Prozent angegeben werden soll
                    if self.radioButton_Absolute.isChecked():
                        #Je nach Eingabeart muss der Absolute Warmwasserbedarf anderst berechnet werden
                        str_yvar = "Verbrauch [kWh]"
                        if self.table.item(row, 2).text() != "None":
                            #Rechnung mit kWh/m²a
                            y_temp = self.CalcStrom_KWHproFlächeJahr(row)                                                        
                        elif self.table.item(row, 3).text() != "None":
                            #Rechnung mit kWh/a
                            y_temp = self.CalcStrom_KWHproJahr(row)   
                        elif self.table.item(row, 5).text() != "None":
                            #Rechnung mit kW/Stück
                            y_temp = self.CalcStrom_KWHproStück(row)   
                    else:
                        #Rechnung mit Prozent
                        str_yvar = "Verbrauch [%]"
                        y_temp = self.CalcStrom_Prozent(row)   

                else:
                    #Return falls ein Wert keine Zahl enthält
                    return
                #Neues y aufsummieren 
                self.y = [a + b for a, b in zip(self.y, y_temp)]
                #Dabei wird die Nutzung aussummiert um zu schauen ob diese 100 ergibt
                sum_Nutzung += float(self.table.item(row, 1).text())
                
            if self.radioButton_month.isChecked() and self.radioButton_Absolute.isChecked():
                #Falls Monat ausgewählt ist müssen die Tageswerte in Monatswerte umgewandelt werden
                self.y = [element * 365 for element in self.y]

            self.lineEdit_SumNutzung.setText(str(sum_Nutzung) + "%")
            
            hover_tool = HoverTool(tooltips=[
            ("x", "@x"),
            ("y", "$y"),
                ])  
            hover_tool.point_policy='snap_to_data'
  
            p = figure(title="Gesamtprofil " + str_xvar, x_axis_label= str_xvar, y_axis_label = str_yvar, width=800, height=300,
                       tools=[hover_tool,"pan,wheel_zoom,box_zoom,reset,save"], y_range=DataRange1d(start=0))

          
            # add a line renderer with legend and line thickness
            p.line(self.x, self.y, line_width=2)
            html = embed.file_html(p, resources.CDN, "my plot")
            self.m_output.setHtml(html)

        except Exception as e:
           if e.__class__.__name__ == "AttributeError":
               pass
           else:
               raise




    def AddProfile(self, data):
        self.table.itemChanged.disconnect()

			#"Profilname" : data[0],
			#"WW-Verbrauch_Stunde [%]" : data[1:25],
           # "WW-Verbrauch_Monat [%]" : data[27:],
			#"Verbrauchsart" : data[25:27],
        
        self.y_hour.append(data["WW-Verbrauch_Stunde [%]"])
        self.y_month.append(data["WW-Verbrauch_Monat [%]"])
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        #Profilname und die beiden Verbrauchsdaten werden auf Read-Only gestellt
        flags = QtCore.Qt.ItemFlags()
        flags != QtCore.Qt.ItemIsEditable

        item = QtWidgets.QTableWidgetItem(str(data["Profilname"]))
        item.setFlags(flags)
        self.table.setItem(rowPosition , 0, item)
        self.table.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem("100"))
        item = QtWidgets.QTableWidgetItem(str(data["Verbrauchsart"][0]))
        item.setFlags(flags)
        self.table.setItem(rowPosition , 2, item)
        item = QtWidgets.QTableWidgetItem(str(data["Verbrauchsart"][1]))
        item.setFlags(flags)
        self.table.setItem(rowPosition , 3, item)
        self.table.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem("0"))
        item = QtWidgets.QTableWidgetItem(str(data["Verbrauchsart"][2]))
        item.setFlags(flags)
        self.table.setItem(rowPosition , 5, item)

        self.table.resizeColumnsToContents()
        self.table.itemChanged.connect(self.UpdatePlot)

        self.UpdatePlot()
       


def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False