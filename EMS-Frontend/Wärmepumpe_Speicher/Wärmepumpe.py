# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import csv
from bokeh import plotting, embed, resources
from bokeh.plotting import figure
import importlib
Import = importlib.import_module("EMS-Backend.Classes.Import")
#Speicher = importlib.import_module("EMS-Frontend.Wärmepumpe_Speicher.Wärmespeicher")
from Wärmepumpe_Speicher.Wärmespeicher import Ui_Speicher

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WP(QWidget):
    #Eigenes Signal definieren
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    #Dieses Signal erkennt ob ein Tastaturkey gedrückt worden ist 
    def keyPressEvent(self, event):
        super(Ui_WP, self).keyPressEvent(event)
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
                    #del self.y_hour[index.row()]
                    #del self.y_month[index.row()]
                except Exception as e:
                    if e.__class__.__name__ == "AttributeError":                    
                        pass
            self.UpdatePlot()

    def __init__(self,typ, parent):
        super(Ui_WP, self).__init__()

        self.parent = parent
        self.setWindowTitle("Auswahl Wärmepumpe")
        self.resize(1200, 322)    
        self.typ = typ

        self.lay = QtWidgets.QVBoxLayout(self)

        #Überschriften
        self.lay_Überschrift = QtWidgets.QHBoxLayout(self)
        self.label_Eingabe = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_Eingabe.setFont(font)
        self.label_Eingabe.setObjectName("label_Eingabe")
        self.label_Eingabe.setText("Eingabe")
        self.lay_Überschrift.addWidget(self.label_Eingabe,2)

        self.label_Vis = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_Vis.setFont(font)
        self.label_Vis.setObjectName("label__Vis")
        self.label_Vis.setText("Visualisierung")
        self.lay_Überschrift.addWidget(self.label_Vis,4)

        self.label_COP = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_COP.setFont(font)
        self.label_COP.setObjectName("label_COP")
        self.label_COP.setText("Eingabe COP-Kennlinie")
        self.lay_Überschrift.addWidget(self.label_COP,2)

        self.label_ProfilBig = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_ProfilBig.setFont(font)
        self.label_ProfilBig.setObjectName("label_Profil")
        self.label_ProfilBig.setText("Profil")
        self.lay_Überschrift.addWidget(self.label_ProfilBig,2)

        self.lay.addLayout(self.lay_Überschrift)

        

        
        self.lay_base = QtWidgets.QHBoxLayout(self)
        self.lay.addLayout(self.lay_base)
        self.lay_vertical_Eingabe = QtWidgets.QVBoxLayout(self)
        self.lay_base.addLayout(self.lay_vertical_Eingabe,2)

        #Ansicht WP Auswahl
        self.radioButton_Heizen = QtWidgets.QRadioButton(self)
        self.radioButton_Heizen.setObjectName("radioButton_Heizen")
        self.radioButton_Heizen.setText("Heizen/Kühlen")
        self.radioButton_Heizen.setEnabled(False)
        self.radioButton_WW = QtWidgets.QRadioButton(self)
        self.radioButton_WW.setObjectName("radioButton_WW")
        self.radioButton_WW.setText("Warmwasser")
        self.radioButton_WW.setEnabled(False)
        self.lay_hori_rbn = QtWidgets.QHBoxLayout(self)
        self.lay_hori_rbn.addWidget(self.radioButton_Heizen)
        self.lay_hori_rbn.addWidget(self.radioButton_WW)
        self.lay_vertical_Eingabe.addLayout(self.lay_hori_rbn)

        
        if typ == "Heizen":
            self.radioButton_Heizen.setChecked(True)
        elif typ == "Warmwasser":
            self.radioButton_WW.setChecked(True)

        #Eingabe Stromverbrauch
        self.doubleSpinBox_Stromverbrauch = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_Stromverbrauch.setObjectName("doubleSpinBox_Stromverbrauch")
        self.label_Stromverbrauch = QtWidgets.QLabel(self)
        self.label_Stromverbrauch.setObjectName("label_Stromverbrauch")
        self.label_Stromverbrauch.setText("Stromverbrauch [kW]")
        self.lay_vert_strom = QtWidgets.QVBoxLayout(self)
        self.lay_vert_strom.addWidget(self.label_Stromverbrauch)
        self.lay_vert_strom.addWidget(self.doubleSpinBox_Stromverbrauch)
        self.lay_vertical_Eingabe.addLayout(self.lay_vert_strom)

        #Eingabe VL Temperaturen WP
        self.label_VL_HZG = QtWidgets.QLabel(self)
        self.label_VL_HZG.setObjectName("label_VL_HZG")
        self.label_VL_HZG.setText("VL HZG [°C]")
        self.doubleSpinBox_VL_HZG = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_VL_HZG.setObjectName("doubleSpinBox_VL_HZG")
        self.label_VL_KLG = QtWidgets.QLabel(self)
        self.label_VL_KLG.setObjectName("label_VL_KLG")
        self.label_VL_KLG.setText("VL KLG [°C]")
        self.doubleSpinBox_VL_KLG = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_VL_KLG.setObjectName("doubleSpinBox_VL_KLG")   
        
        self.lay_Grid = QtWidgets.QGridLayout(self)
        self.lay_Grid.addWidget(self.label_VL_HZG,0, 0)
        self.lay_Grid.addWidget(self.label_VL_KLG,0, 1)
        self.lay_Grid.addWidget(self.doubleSpinBox_VL_HZG,1, 0)
        self.lay_Grid.addWidget(self.doubleSpinBox_VL_KLG,1, 1)
        self.lay_vertical_Eingabe.addLayout(self.lay_Grid)        

        #Button um zur Speicherauswahl zu gelangen
        self.pushButton_Speicherauswahl = QtWidgets.QPushButton(self)
        self.pushButton_Speicherauswahl.setObjectName("pushButton_Speicherauswahl")
        self.pushButton_Speicherauswahl.setText("Speicherauswahl")
        self.lay_vertical_Eingabe.addWidget(self.pushButton_Speicherauswahl) 

        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lay_vertical_Eingabe.addItem(verticalSpacer)

        #Visualisierung
        self.lay_vertical_Vis = QtWidgets.QVBoxLayout(self)        
        self.lay_base.addLayout(self.lay_vertical_Vis,4)



        self.WebEngine = QtWebEngineWidgets.QWebEngineView(self)
        p = figure(width=400, height=200)        
        html = embed.file_html(p, resources.CDN, "my plot")
        self.WebEngine.setHtml(html)
        self.lay_vertical_Vis.addWidget(self.WebEngine,9)

        #Eingabe COP
        self.lay_vertical_COP = QtWidgets.QVBoxLayout(self)        
        self.lay_hori_COP_Eingabe = QtWidgets.QHBoxLayout(self)       
        self.lay_base.addLayout(self.lay_vertical_COP,2)

        
        self.pushButton_AddRow = QtWidgets.QPushButton(self)
        self.pushButton_AddRow.setGeometry(QtCore.QRect(800, 20, 101, 31))
        self.pushButton_AddRow.setObjectName("pushButton_AddRow")
        self.pushButton_AddRow.setText("Add Row")
        self.pushButton_AddRow.clicked.connect(self.AddRow)
        self.lay_hori_COP_Eingabe.addWidget(self.pushButton_AddRow,3)
        self.lay_vertical_COP.addLayout(self.lay_hori_COP_Eingabe,1)

        self.table = QtWidgets.QTableWidget()
        self.table.setObjectName("table")
        self.lay_vertical_COP.addWidget(self.table,9)
        self.table.itemChanged.connect(self.UpdatePlot)
        self.table.setColumnCount(4)  # We install six columns
        # Set table headers
        self.table.setHorizontalHeaderLabels(["Temp_1","Temp_2","COP_1","COP_2"])
        #connect Signal
        self.keyPressed.connect(self.on_key)
        self.table.resizeColumnsToContents()

        #Profil        
        self.lay_vertical_Profil = QtWidgets.QVBoxLayout(self)
        #Auswahl Profilname
        self.lay_hori_speichern = QtWidgets.QHBoxLayout(self)  
        self.lay_vertical_label1 = QtWidgets.QVBoxLayout(self)  
        self.label_Profil = QtWidgets.QLabel(self)
        self.label_Profil.setText("Eingabe Profilname")
        self.lineEdit_Profil = QtWidgets.QLineEdit(self)
        self.lineEdit_Profil.setObjectName("lineEdit_Profil")
        self.lay_vertical_label1.addWidget(self.label_Profil)
        self.lay_vertical_label1.addWidget(self.lineEdit_Profil)
        self.lay_hori_speichern.addLayout(self.lay_vertical_label1)

        #Profil speichern
        self.lay_vertical_invis1 = QtWidgets.QVBoxLayout(self)  
        self.label_Profil_invisible = QtWidgets.QLabel(self)
        self.pushButton_SaveProfile = QtWidgets.QPushButton(self)
        self.pushButton_SaveProfile.setObjectName("pushButton_SaveProfile")
        self.pushButton_SaveProfile.setText("Save Profile")
        self.lay_vertical_invis1.addWidget(self.label_Profil_invisible)
        self.lay_vertical_invis1.addWidget(self.pushButton_SaveProfile)
        self.lay_hori_speichern.addLayout(self.lay_vertical_invis1)
        self.lay_vertical_Profil.addLayout(self.lay_hori_speichern)

        #Combobox für Benutzerprofile
        self.lay_hori_Auswahl = QtWidgets.QHBoxLayout(self)  
        self.lay_vertical_label2 = QtWidgets.QVBoxLayout(self)  
        self.label_AuswahlProfil = QtWidgets.QLabel(self)
        self.label_AuswahlProfil.setText("Auswahl Profil")
        self.comboBox_SelectProfile = QtWidgets.QComboBox(self)
        self.comboBox_SelectProfile.setObjectName("comboBox_SelectProfile")
        self.lay_vertical_label2.addWidget(self.label_AuswahlProfil)
        self.lay_vertical_label2.addWidget(self.comboBox_SelectProfile)
        self.lay_hori_Auswahl.addLayout(self.lay_vertical_label2)

        #Profil löschen
        self.lay_vertical_invis2 = QtWidgets.QVBoxLayout(self)  
        self.label_Profil_invisible2 = QtWidgets.QLabel(self)

        self.pushButton_DeleteProfile = QtWidgets.QPushButton(self)
        self.pushButton_DeleteProfile.setObjectName("pushButton_DeleteProfile")
        self.pushButton_DeleteProfile.setText("Delete Profile")  
        
        self.lay_vertical_invis2.addWidget(self.label_Profil_invisible2)
        self.lay_vertical_invis2.addWidget(self.pushButton_DeleteProfile)
        self.lay_hori_Auswahl.addLayout(self.lay_vertical_invis2)
        self.lay_vertical_Profil.addLayout(self.lay_hori_Auswahl)
        
        #Fertig mit Eingabe
        self.pushButton_UseProfile = QtWidgets.QPushButton(self)
        self.pushButton_UseProfile.setObjectName("pushButton_UseProfile")
        self.pushButton_UseProfile.setText("Profil benutzen") 
        self.pushButton_UseProfile.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}") 
        self.lay_vertical_Profil.addWidget(self.pushButton_UseProfile)
        self.lay_base.addLayout(self.lay_vertical_Profil,2)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lay_vertical_Profil.addItem(verticalSpacer)
        
        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.addItems(names)        
        self.comboBox_SelectProfile.activated.connect(self.SetText)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)
        self.pushButton_UseProfile.clicked.connect(self.UseProfile)
        self.pushButton_Speicherauswahl.clicked.connect(self.OpenSpeicher)
        
        self.li_inputWidgets = [self.doubleSpinBox_Stromverbrauch, self.doubleSpinBox_VL_HZG,
                                self.doubleSpinBox_VL_KLG,self.table]

    def AddRow(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        for column in range(4):
            self.table.setItem(rowPosition , column, QtWidgets.QTableWidgetItem("0"))

    def UpdatePlot(self):
        try:
            
            self.x = []
            self.y = []
            for row in range(self.table.rowCount()):
                if is_number_tryexcept(self.table.item(row, 0).text()) and is_number_tryexcept(self.table.item(row, 1).text()) and is_number_tryexcept(self.table.item(row, 2).text()) and is_number_tryexcept(self.table.item(row, 3).text()):

                    temp1 = float(self.table.item(row, 0).text())
                    temp2 = float(self.table.item(row, 1).text())
                    COP1 = float(self.table.item(row, 2).text())
                    COP2 = float(self.table.item(row, 3).text())
                    self.x.append(temp1)
                    self.x.append(temp2)
                    self.y.append(COP1)
                    self.y.append(COP2)

            p = figure(width=440, height=240,
                       title="COP-Kennlinie", x_axis_label= "Außentemperatur [°C]", y_axis_label = "COP")  
            p.line(x=self.x, y=self.y, line_width=3, color="black")
                  
            html = embed.file_html(p, resources.CDN, "my plot")
            self.WebEngine.setHtml(html)
        except Exception as e:
           if e.__class__.__name__ == "AttributeError":
               pass
           else:
               raise

    def SetText(self):
        self.lineEdit_Profil.setText(self.comboBox_SelectProfile.currentText())

    def OpenSpeicher(self):
        if hasattr(self, 'speicherWindow') == False:
            self.speicherWindow = Ui_Speicher(float(self.doubleSpinBox_VL_HZG.value()),self.typ)
        self.speicherWindow.show()
        
    def SaveProfile(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        
        name = self.lineEdit_Profil.text()
        #Wenn nichts im Lineedit steht oder kein Radiobutton ausgewählt ist wird das Profil nicht gespeichert
        if self.lineEdit_Profil == "" or hasattr(self, 'speicherWindow') == False:
            return

        li_toSave = []
        li_toSave.append(name)

        if self.radioButton_Heizen.isChecked():
            li_toSave.append("Heizen")
        elif self.radioButton_WW.isChecked():
            li_toSave.append("Warmwasser")      

        for widget in self.li_inputWidgets: 
            if widget.objectName() != "table":
                li_toSave.append(widget.value())
            else:
                columnString = ""
                for row in range(self.table.rowCount()):
                    for column in range(4):
                        columnString += self.table.item(row, column).text() + "----"
                li_toSave.append(columnString)
            
        li_toSave.append(self.speicherWindow.lineEdit_Profil.text())

        #Kontrolle ob ein Profil mit diesem Namen bereits existiert
        if name in names:
            self.DeleteProfile()
        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/Wärmepumpe_Profile.csv",'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave)
        self.UpdateProfiles()
   
    def DeleteProfile(self):
        name = self.lineEdit_Profil.text()
        with open("./EMS-Frontend/data/Wärmepumpe_Profile.csv", 'r', encoding="utf-8") as inp:
            lines = inp.readlines()
        with open("./EMS-Frontend/data/Wärmepumpe_Profile.csv",'w', newline='', encoding="utf-8") as f:
            for line in lines:
                if line.split(",")[0] != name:
                    f.write(line)
        self.UpdateProfiles()
        

    def UpdateProfiles(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", usecols = [0], delimiter = ",", encoding='utf-8')["Name"])
        self.comboBox_SelectProfile.clear() 
        self.comboBox_SelectProfile.addItems(names)        
        self.comboBox_SelectProfile.setCurrentText(self.lineEdit_Profil.text())
                   

    def LoadProfile(self):
     
        df = pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", delimiter = ",", encoding='utf-8')

        name = self.lineEdit_Profil.text()

        self.lineEdit_Profil.setText(name)
        values = df[df.values == name].values.flatten().tolist()
        if values[1] == "Heizen":
            self.radioButton_Heizen.setChecked(True)
        elif values[1] == "Warmwasser":
            self.radioButton_WW.setChecked(True)

        for i,widget in enumerate(self.li_inputWidgets,2):
            if widget.objectName() != "table":
                widget.setValue(float(values[i]))
            else:
                self.table.setRowCount(0)
                dataString = values[i].split("----")[:-1]
                rows = int(len(dataString) / 4)
                i = 0
                for row in range(rows):
                    rowPosition = self.table.rowCount()
                    self.table.insertRow(rowPosition)
                    for column in range(4):
                        self.table.setItem(rowPosition , column, QtWidgets.QTableWidgetItem(str(dataString[i])))
                        i += 1

        self.speicherWindow = Ui_Speicher(float(self.doubleSpinBox_VL_HZG.value()),self.typ)
        self.speicherWindow.LoadProfile(values[-1])

    def UseProfile(self):
        if self.lineEdit_Profil.text() == "":
            return

        self.SaveProfile()

        df = pd.read_csv("./EMS-Frontend/data/Wärmepumpe_Profile.csv", delimiter = ",", encoding='utf-8')
        name = self.comboBox_SelectProfile.currentText()

        data = df[df.values == name].values.flatten().tolist()
        Wärmepumpe = {
            "Art" : self.typ,
            "Stromverbrauch" : data[2],            
            "VL_HZG" : data[3],
            "VL_KLG" : data[4],
            "Table" : data[5],
            "speichername" : data[6],
            }
        Import.importGUI.Import_WP(Wärmepumpe)
        self.pushButton_UseProfile.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        self.speicherWindow.UseProfile()
        if self.typ == "Heizen":
            self.parent.lineEdit_Wärmepumpe_HZG.setText(self.lineEdit_Profil.text())
        else:
            self.parent.lineEdit_Wärmepumpe_WW.setText(self.lineEdit_Profil.text())
      

    
        

def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

#app = QApplication(sys.argv)
#main = QWidget()
#w = Ui_WP()
#w.show()
#app.exec()