# -*- coding: latin-1 -*-
import os
import sys
import pandas as pd
import csv
#from pandas.core.frame import DataFrame
from data.Stylesheets import GetFancySlider
from Warmwasser_Nutzungsmischung import WindowGesamtprofil
import importlib
Import = importlib.import_module("EMS-Backend.Classes.Import")

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(QMainWindow):

    def __init__(self):
        super().__init__()
   

 
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1050, 550)
        Form.setStyleSheet(GetFancySlider())
        self.graphWindow = WindowGesamtprofil()

        #Hier werden beide Fenster richtig positioniert
        #Die Fenstergröße wird hierbei dynamisch an die Bildschirmgröße angepasst
        #Desktopmaße
        coords = QApplication.desktop().availableGeometry()
        left_Coord = int(coords.height() / 2 - Form.frameGeometry().height() / 2)
        Form.move(10,left_Coord)
        self.graphWindow.move(Form.pos().x() + Form.frameGeometry().width() + 10, Form.pos().y())
        self.graphWindow.resize(coords.width() - Form.frameGeometry().width() - 30, 550)

        #Stündliche Summe
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(984, 220, 40, 20))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        #Monatliche Summe
        self.lineEdit_sumMonth = QtWidgets.QLineEdit(Form)
        self.lineEdit_sumMonth.setGeometry(QtCore.QRect(620, 470, 40, 20))
        self.lineEdit_sumMonth.setReadOnly(True)
        self.lineEdit_sumMonth.setObjectName("lineEdit_sumMonth")

        #Auswahl Profilname
        self.label_Profil = QtWidgets.QLabel(Form)
        self.label_Profil.setGeometry(QtCore.QRect(730, 255, 200, 30))
        self.label_Profil.setText("Eingabe Profilname")
        self.lineEdit_Profil = QtWidgets.QLineEdit(Form)
        self.lineEdit_Profil.setGeometry(QtCore.QRect(730, 280, 150, 20))
        self.lineEdit_Profil.setObjectName("lineEdit_Profil")

        #Combobox für Benutzerprofile
        self.label_AuswahlProfil = QtWidgets.QLabel(Form)
        self.label_AuswahlProfil.setGeometry(QtCore.QRect(730, 300, 200, 30))
        self.label_AuswahlProfil.setText("Auswahl benutzerdefinierter Profile")
        self.comboBox_SelectProfile = QtWidgets.QComboBox(Form)
        self.comboBox_SelectProfile.setGeometry(QtCore.QRect(730, 325, 150, 22))
        self.comboBox_SelectProfile.setObjectName("comboBox_SelectProfile")

        #Profil speichern
        self.pushButton_SaveProfile = QtWidgets.QPushButton(Form)
        self.pushButton_SaveProfile.setGeometry(QtCore.QRect(900, 278, 75, 23))
        self.pushButton_SaveProfile.setObjectName("pushButton_SaveProfile")
        self.pushButton_SaveProfile.setText("Save Profile")

        #Profil löschen
        self.pushButton_DeleteProfile = QtWidgets.QPushButton(Form)
        self.pushButton_DeleteProfile.setGeometry(QtCore.QRect(900, 323, 75, 23))
        self.pushButton_DeleteProfile.setObjectName("pushButton_DeleteProfile")
        self.pushButton_DeleteProfile.setText("Delete Profile")

        #Combobox für Standardprofile
        self.label_DefaultProfil = QtWidgets.QLabel(Form)
        self.label_DefaultProfil.setGeometry(QtCore.QRect(730, 345, 200, 30))
        self.label_DefaultProfil.setText("Auswahl default Profile")
        self.comboBox_DefaultProfile = QtWidgets.QComboBox(Form)
        self.comboBox_DefaultProfile.setGeometry(QtCore.QRect(730, 370, 150, 22))
        self.comboBox_DefaultProfile.setObjectName("comboBox_DefaultProfile")

        #Input Warmwasserverbrauch
        self.label_WWVerbrauch = QtWidgets.QLabel(Form)
        self.label_WWVerbrauch.setGeometry(QtCore.QRect(730, 390, 200, 30))
        self.label_WWVerbrauch.setText("Eingabe Warmwasserverbrauch")
        self.doubleSpinBox_WWValue = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_WWValue.setGeometry(QtCore.QRect(730, 415, 62, 22))
        self.doubleSpinBox_WWValue.setObjectName("doubleSpinBox_WWValue")
        self.doubleSpinBox_WWValue.setRange(0,1000)
        self.radioButton_Person = QtWidgets.QRadioButton(Form)
        self.radioButton_Person.setGeometry(QtCore.QRect(800, 410, 82, 17))
        self.radioButton_Person.setObjectName("radioButton_Person")
        self.radioButton_Person.setText("Liter/Person")
        self.radioButton_m2 = QtWidgets.QRadioButton(Form)
        self.radioButton_m2.setGeometry(QtCore.QRect(800, 427, 82, 16))
        self.radioButton_m2.setObjectName("radioButton_m2")
        self.radioButton_m2.setText("Liter/m2")      
        self.radioButton_Person.toggled['bool'].connect(self.radioButton_m2.repaint) 
        self.radioButton_m2.toggled['bool'].connect(self.radioButton_Person.repaint) 

        #Fertig mit Eingabe
        self.pushButton_UseProfile = QtWidgets.QPushButton(Form)
        self.pushButton_UseProfile.setGeometry(QtCore.QRect(730, 450, 150, 30))
        self.pushButton_UseProfile.setObjectName("pushButton_UseProfile")
        self.pushButton_UseProfile.setText("Use Profile for Simulation")

        
        
        
        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./EMS-Frontend/data/Warmwasser_Profile.csv", usecols = [0], delimiter = ",", encoding='latin1')["Name"])
        self.comboBox_SelectProfile.addItems(names)
        names = list(pd.read_csv("./EMS-Frontend/data/Warmwasser_Profile_Default.csv", usecols = [0], delimiter = ",", encoding='latin1')["Name"])
        self.comboBox_DefaultProfile.addItems(names)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.comboBox_DefaultProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)
        self.pushButton_UseProfile.clicked.connect(self.UseProfile)

        #Stuff zum schöner machen der Form
        self.frame_Hourly = QtWidgets.QFrame(Form)
        self.frame_Hourly.setGeometry(QtCore.QRect(10, 10, 1023, 240))
        self.frame_Hourly.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Hourly.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_Hourly.setObjectName("frame_Hourly")
        self.label_Hourly = QtWidgets.QLabel(Form)
        self.label_Hourly.setGeometry(QtCore.QRect(20, 8, 200, 30))
        self.label_Hourly.setObjectName("label_Hourly")
        self.label_Hourly.setText("Eingabe Profil Stundenwerte")

        self.frame_Monthly = QtWidgets.QFrame(Form)
        self.frame_Monthly.setGeometry(QtCore.QRect(10, 260, 700, 240))
        self.frame_Monthly.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Monthly.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_Monthly.setObjectName("frame_Monthly")
        self.label_Monthly = QtWidgets.QLabel(Form)
        self.label_Monthly.setGeometry(QtCore.QRect(20, 255, 200, 30))
        self.label_Monthly.setObjectName("label_Monthly")
        self.label_Monthly.setText("Eingabe Profil Monatswerte")


        def Create_Slider_Hourly(i):
            Slider = {}
            verticalSlider = QtWidgets.QSlider(Form)
            verticalSlider.setGeometry(QtCore.QRect(30, 180, 16, 160))
            verticalSlider.setMaximum(20)
            verticalSlider.setPageStep(2)
            verticalSlider.setOrientation(QtCore.Qt.Vertical)
            verticalSlider.setInvertedAppearance(False)
            verticalSlider.setObjectName("verticalSlider" + str(i))
            spinBox = QtWidgets.QSpinBox(Form)
            spinBox.setGeometry(QtCore.QRect(20, 350, 35, 22))
            spinBox.setObjectName("spinBox" + str(i))
            label = QtWidgets.QLabel(Form)
            label.setGeometry(QtCore.QRect(35, 160, 16, 16))
            label.setObjectName("label" + str(i))

            spinBox.valueChanged['int'].connect(verticalSlider.setValue) # type: ignore
            verticalSlider.valueChanged['int'].connect(spinBox.setValue) # type: ignore
            spinBox.textChanged.connect(self.PrintSum)
            
            move = 40
            verticalSlider.move(i * move+30,50)
            spinBox.move(i * move+20,220)
            label.move(i * move+33,30)
            label.setText(str(i))

            Slider["Label"] = label
            Slider["Slider"] = verticalSlider
            Slider["SpinBox"] = spinBox
            
            return Slider

        self.li_Widgets = []
        for i in range(24):
            self.li_Widgets.append(Create_Slider_Hourly(i))

        def Create_Slider_Monthly(i):
            Slider = {}
            verticalSlider = QtWidgets.QSlider(Form)
            verticalSlider.setGeometry(QtCore.QRect(30, 360, 16, 160))
            verticalSlider.setMaximum(20)
            verticalSlider.setPageStep(2)
            verticalSlider.setOrientation(QtCore.Qt.Vertical)
            verticalSlider.setInvertedAppearance(False)
            verticalSlider.setObjectName("verticalSlider" + str(i))
            spinBox = QtWidgets.QSpinBox(Form)
            spinBox.setGeometry(QtCore.QRect(20, 700, 41, 22))
            spinBox.setObjectName("spinBox" + str(i))
            label = QtWidgets.QLabel(Form)
            label.setGeometry(QtCore.QRect(35, 320, 20, 16))
            label.setObjectName("label" + str(i))

            spinBox.valueChanged['int'].connect(verticalSlider.setValue) # type: ignore
            verticalSlider.valueChanged['int'].connect(spinBox.setValue) # type: ignore
            spinBox.textChanged.connect(self.PrintSum)
            
            move = 50
            verticalSlider.move(i * move+30,20+280)
            spinBox.move(i * move+20,190+280)
            label.move(i * move+30,0+280)
            months = ["Jan","Feb","Mar","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"]
            label.setText(months[i])

            Slider["Label"] = label
            Slider["Slider"] = verticalSlider
            Slider["SpinBox"] = spinBox
            
            return Slider
        self.li_Widgets_months = []
        
        for i in range(12):
            self.li_Widgets_months.append(Create_Slider_Monthly(i))



    def SaveProfile(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Warmwasser_Profile.csv", usecols = [0], delimiter = ",", encoding='latin1')["Name"])
        names_default = list(pd.read_csv("./EMS-Frontend/data/Warmwasser_Profile_Default.csv", usecols = [0], delimiter = ",", encoding='latin1')["Name"])

        name = self.lineEdit_Profil.text() 
        #Kontrolle ob der Profilname bereits in der Defaultliste vorhanden ist
        if name in names_default:
            dlg = QMessageBox()
            dlg.setWindowTitle("Hinweis")
            dlg.setText("Profilname kann nicht Defaultname sein!")
            dlg.exec()
            return
        
        li_toSave = []
        li_toSave.append(name)
        for w in self.li_Widgets:
            li_toSave.append(w["SpinBox"].value())
        if self.radioButton_Person.isChecked():
            li_toSave.append("None")
            value = self.doubleSpinBox_WWValue.value()
            li_toSave.append(value)
        elif self.radioButton_m2.isChecked():
            value = self.doubleSpinBox_WWValue.value()
            li_toSave.append(value)
            li_toSave.append("None")
        for w in self.li_Widgets_months:
            li_toSave.append(w["SpinBox"].value())

        #Kontrolle ob ein Profil mit diesem Namen bereits existiert
        if name in names:
            self.DeleteProfile()
        #Neues Profil hinzufügen
        with open("./EMS-Frontend/data/Warmwasser_Profile.csv",'a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave)
        self.UpdateProfiles()
   
    def DeleteProfile(self):
        name = self.comboBox_SelectProfile.currentText()
        with open("./EMS-Frontend/data/Warmwasser_Profile.csv", 'r') as inp:
            lines = inp.readlines()
        with open("./EMS-Frontend/data/Warmwasser_Profile.csv",'w', newline='') as f:
            for line in lines:
                if line.split(",")[0] != name:
                    f.write(line)
        self.UpdateProfiles()
        

    def UpdateProfiles(self):
        names = list(pd.read_csv("./EMS-Frontend/data/Warmwasser_Profile.csv", usecols = [0], delimiter = ",", encoding='latin1')["Name"])
        self.comboBox_SelectProfile.clear() 
        self.comboBox_SelectProfile.addItems(names)        
        self.comboBox_SelectProfile.setCurrentText(self.lineEdit_Profil.text())
                   

    def LoadProfile(self):
        
        sender = self.sender()
        name = sender.currentText()
        if sender.objectName() == "comboBox_DefaultProfile":
            df = pd.read_csv("./EMS-Frontend/data/Warmwasser_Profile_Default.csv", delimiter = ",", encoding='latin1')
        elif sender.objectName() == "comboBox_SelectProfile":
            df = pd.read_csv("./EMS-Frontend/data/Warmwasser_Profile.csv", delimiter = ",", encoding='latin1')


        self.lineEdit_Profil.setText(name)
        df = df[df.values == name].values.flatten().tolist()

        values = df[1:25]        
        for i,w in enumerate(self.li_Widgets):
            w["SpinBox"].setValue(values[i])

        ww_values = df[25:27]
        if ww_values[0] != "None":
            self.doubleSpinBox_WWValue.setValue(float(ww_values[0]))
            self.radioButton_m2.setChecked(True)
        elif ww_values[1] != "None":
            self.doubleSpinBox_WWValue.setValue(float(ww_values[1]))
            self.radioButton_Person.setChecked(True)
        
        values_monthly = df[27:]        
        for i,w in enumerate(self.li_Widgets_months):
            w["SpinBox"].setValue(values_monthly[i])

    def PrintSum(self):
        var_sum_hourly = 0
        for w in self.li_Widgets:
           var_sum_hourly += w["SpinBox"].value()
        self.lineEdit.setText(str(var_sum_hourly) + "%")

        var_sum_monthly = 0
        for w in self.li_Widgets_months:
            var_sum_monthly += w["SpinBox"].value()
        self.lineEdit_sumMonth.setText(str(var_sum_monthly) + "%")

        li_lineEdits = [self.lineEdit,self.lineEdit_sumMonth]
        li_sums = [var_sum_hourly,var_sum_monthly]
        for i,it_sum in enumerate(li_sums):
            if it_sum > 100:
                li_lineEdits[i].setStyleSheet("QLineEdit"
                                    "{"
                                    "background : red;"
                                    "}")
                
            else:
                li_lineEdits[i].setStyleSheet("QLineEdit"
                                    "{"
                                    "background : white;"
                                    "}")
        return li_sums

    def UseProfile(self):
        if any(x != 100 for x in self.PrintSum()):
            dlg = QMessageBox()
            dlg.setWindowTitle("Fehler")
            dlg.setText("Summe Warmwasserprofil stündlich oder monatlich ist nicht 100%")
            dlg.exec()
            return
        self.SaveProfile()
        df = pd.read_csv("./EMS-Frontend/data/Warmwasser_Profile.csv", delimiter = ",", encoding='latin1')
        name = self.comboBox_SelectProfile.currentText()
        data = df[df.values == name].values.flatten().tolist()
        Import.importGUI.Import_WarmWater(data)

        data = {
			"Profilname" : data[0],
			"WW-Verbrauch_Stunde [%]" : data[1:25],
            "WW-Verbrauch_Monat [%]" : data[27:],
			"Verbrauchsart" : data[25:27],
                }
        self.graphWindow.AddProfile(data)
        self.ShowGraph()
        
       

    def ShowGraph(self):
        self.graphWindow.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)
main = MainWindow()
w = Ui_Form()
w.setupUi(main)
main.show()
app.exec()