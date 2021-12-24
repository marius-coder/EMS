# -*- coding: UTF-8 -*-
import os
import sys
import pandas as pd
import csv
from pandas.core.frame import DataFrame

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):

    def layout_widgets(self, Form):
        return (Form.itemAt(i) for i in range(Form.count()))

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1600, 600)
        Form.setStyleSheet("QSlider::groove:horizontal\n"
                        "{\n"
                        "border: 1px solid #bbb;\n"
                        "background: white;\n"
                        "width: 10px;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::sub-page:vertical\n"
                        "{\n"
                        "background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #fff, stop: 0.4999 #eee, stop: 0.5 #ddd, stop: 1 #eee );\n"
                        "border: 1px solid #777;\n"
                        "width: 10px;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::add-page:vertical {\n"
                        "background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #78d, stop: 0.4999 #46a, stop: 0.5 #45a, stop: 1 #238 );\n"
                        "\n"
                        "border: 1px solid #777;\n"
                        "width: 10px;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::handle:vertical {\n"
                        "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eee, stop:1 #ccc);\n"
                        "border: 1px solid #777;\n"
                        "height: 13px;\n"
                        "margin-top: -2px;\n"
                        "margin-bottom: -2px;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::handle:vertical:hover {\n"
                        "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fff, stop:1 #ddd);\n"
                        "border: 1px solid #444;\n"
                        "border-radius: 4px;\n"
                        "}\n"
                        "\n"
                        "QSlider::sub-page:vertical:disabled {\n"
                        "background: #bbb;\n"
                        "border-color: #999;\n"
                        "}\n"
                        "\n"
                        "QSlider::add-page:vertical:disabled {\n"
                        "background: #eee;\n"
                        "border-color: #999;\n"
                        "}\n"
                        "\n"
                        "QSlider::handle:vertical:disabled {\n"
                        "background: #eee;\n"
                        "border: 1px solid #aaa;\n"
                        "border-radius: 4px;\n"
                        "}")

        #Input
        self.radioButton_Person = QtWidgets.QRadioButton(Form)
        self.radioButton_Person.setGeometry(QtCore.QRect(1300, 120, 82, 17))
        self.radioButton_Person.setObjectName("radioButton_Person")
        self.radioButton_Person.setText("Liter/Person")
        self.radioButton_m2 = QtWidgets.QRadioButton(Form)
        self.radioButton_m2.setGeometry(QtCore.QRect(1300, 137, 82, 16))
        self.radioButton_m2.setObjectName("radioButton_m2")
        self.radioButton_m2.setText("Liter/m2")
        self.doubleSpinBox_WWValue = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_WWValue.setGeometry(QtCore.QRect(1230, 125, 62, 22))
        self.doubleSpinBox_WWValue.setObjectName("doubleSpinBox_WWValue")

        self.radioButton_Person.toggled['bool'].connect(self.radioButton_m2.repaint) # type: ignore
        self.radioButton_m2.toggled['bool'].connect(self.radioButton_Person.repaint) # type: ignore
        

        #Output der Summe
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(1230, 190, 40, 20))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")

        #Auswählen bzw. erstellen eines neuen Profils
        self.lineEdit_Profil = QtWidgets.QLineEdit(Form)
        self.lineEdit_Profil.setGeometry(QtCore.QRect(1230, 20, 81, 20))
        self.lineEdit_Profil.setObjectName("lineEdit_Profil")
        self.comboBox_SelectProfile = QtWidgets.QComboBox(Form)
        self.comboBox_SelectProfile.setGeometry(QtCore.QRect(1230, 40, 69, 22))
        self.comboBox_SelectProfile.setObjectName("comboBox_SelectProfile")
        self.pushButton_SaveProfile = QtWidgets.QPushButton(Form)
        self.pushButton_SaveProfile.setGeometry(QtCore.QRect(1230, 60, 75, 23))
        self.pushButton_SaveProfile.setObjectName("pushButton_SaveProfile")
        self.pushButton_SaveProfile.setText("Save Profile")
        self.pushButton_DeleteProfile = QtWidgets.QPushButton(Form)
        self.pushButton_DeleteProfile.setGeometry(QtCore.QRect(1260, 60, 75, 23))
        self.pushButton_DeleteProfile.setObjectName("pushButton_DeleteProfile")
        self.pushButton_DeleteProfile.setText("Delete Profile")
        #Combobox befüllen mit vorhandenen Daten
        names = list(pd.read_csv("./data/Warmwasser_Profile.csv", usecols = [0], delimiter = ",")["Name"])
        self.comboBox_SelectProfile.addItems(names)
        self.comboBox_SelectProfile.activated.connect(self.LoadProfile)
        self.pushButton_SaveProfile.clicked.connect(self.SaveProfile)
        self.pushButton_DeleteProfile.clicked.connect(self.DeleteProfile)
        


        def Create_Slider(i):
            Slider = {}
            verticalSlider = QtWidgets.QSlider(Form)
            verticalSlider.setGeometry(QtCore.QRect(30, 180, 16, 160))
            verticalSlider.setMaximum(20)
            verticalSlider.setPageStep(2)
            verticalSlider.setOrientation(QtCore.Qt.Vertical)
            verticalSlider.setInvertedAppearance(False)
            verticalSlider.setObjectName("verticalSlider" + str(i))
            spinBox = QtWidgets.QSpinBox(Form)
            spinBox.setGeometry(QtCore.QRect(20, 350, 41, 22))
            spinBox.setObjectName("spinBox" + str(i))
            label = QtWidgets.QLabel(Form)
            label.setGeometry(QtCore.QRect(35, 160, 16, 16))
            label.setObjectName("label" + str(i))

  
            spinBox.valueChanged['int'].connect(verticalSlider.setValue) # type: ignore
            verticalSlider.valueChanged['int'].connect(spinBox.setValue) # type: ignore
            spinBox.textChanged.connect(self.PrintSum)
            
            move = 50
            verticalSlider.move(i * move+30,20)
            spinBox.move(i * move+20,190)
            label.move(i * move+33,0)
            label.setText(str(i))




            Slider["Label"] = label
            Slider["Slider"] = verticalSlider
            Slider["SpinBox"] = spinBox
            
            return Slider

        self.li_Widgets = []
        for i in range(24):
            self.li_Widgets.append(Create_Slider(i))

    def SaveProfile(self):
        name = self.lineEdit_Profil.text() 
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
        df_append = pd.DataFrame(li_toSave)
        with open("./data/Warmwasser_Profile.csv",'a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(li_toSave)
        self.UpdateProfiles()
   
    def DeleteProfile(self):
        name = self.comboBox_SelectProfile.currentText()
        with open("./data/Warmwasser_Profile.csv", 'r') as inp:
            lines = inp.readlines()
        with open("./data/Warmwasser_Profile.csv",'w', newline='') as f:
            for line in lines:
                print(line.split(",")[0])
                if line.split(",")[0] != name:
                    f.write(line)
        self.UpdateProfiles()
    def UpdateProfiles(self):
        names = list(pd.read_csv("./data/Warmwasser_Profile.csv", usecols = [0], delimiter = ",")["Name"])
        self.comboBox_SelectProfile.clear() 
        self.comboBox_SelectProfile.addItems(names)        
                    
                   

      



    def LoadProfile(self):
        df = pd.read_csv("./data/Warmwasser_Profile.csv", delimiter = ",")
        name = self.comboBox_SelectProfile.currentText()
        self.lineEdit_Profil.setText(name)
        df = df[df.values == name].values.flatten().tolist()

        values = df[1:25]
        ww_values = df[25:]    
        for i,w in enumerate(self.li_Widgets):
            w["SpinBox"].setValue(values[i])

        if ww_values[0] != "None":
            self.doubleSpinBox_WWValue.setValue(float(ww_values[0]))
            self.radioButton_m2.setChecked(True)
        elif ww_values[1] != "None":
            self.doubleSpinBox_WWValue.setValue(float(ww_values[1]))
            self.radioButton_Person.setChecked(True)
        
    def PrintSum(self):
        var_sum = 0
        for w in self.li_Widgets:
           var_sum += w["SpinBox"].value()
        self.lineEdit.setText(str(var_sum) + "%")
        if var_sum > 100:
            self.lineEdit.setStyleSheet("QLineEdit"
                                "{"
                                "background : red;"
                                "}")
        else:
            self.lineEdit.setStyleSheet("QLineEdit"
                                "{"
                                "background : white;"
                                "}")
        print("Summe ist: ", var_sum)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)
main = MainWindow()
w = Ui_Form()
w.setupUi(main)
main.show()
app.exec()