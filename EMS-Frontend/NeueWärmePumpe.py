# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Marius/source/repos/EMS/GUI/NeueW?rmePumpe.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import sys

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_NeueWarmepumpe(object):
    def setupUi(self, Form_NeueWarmepumpe):
        Form_NeueWarmepumpe.setObjectName("Form_NeueWarmepumpe")
        Form_NeueWarmepumpe.resize(737, 394)
        Form_NeueWarmepumpe.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton = QtWidgets.QPushButton(Form_NeueWarmepumpe)
        self.pushButton.setGeometry(QtCore.QRect(530, 300, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(Form_NeueWarmepumpe)
        self.comboBox.setGeometry(QtCore.QRect(20, 40, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 71, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtWidgets.QComboBox(Form_NeueWarmepumpe)
        self.comboBox_2.setGeometry(QtCore.QRect(20, 90, 69, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.lineEdit = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit.setGeometry(QtCore.QRect(20, 140, 31, 20))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_2.setGeometry(QtCore.QRect(60, 140, 31, 20))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 111, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 140, 31, 20))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.checkBox_Trinkwassererwrmung = QtWidgets.QCheckBox(Form_NeueWarmepumpe)
        self.checkBox_Trinkwassererwrmung.setGeometry(QtCore.QRect(20, 170, 151, 17))
        self.checkBox_Trinkwassererwrmung.setProperty("a", False)
        self.checkBox_Trinkwassererwrmung.setObjectName("checkBox_Trinkwassererwrmung")
        self.label_HeizstabLeistung = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_HeizstabLeistung.setEnabled(False)
        self.label_HeizstabLeistung.setGeometry(QtCore.QRect(20, 190, 111, 16))
        self.label_HeizstabLeistung.setObjectName("label_HeizstabLeistung")
        self.lineEdit_trinkwasser_leistung = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_trinkwasser_leistung.setEnabled(False)
        self.lineEdit_trinkwasser_leistung.setGeometry(QtCore.QRect(20, 210, 31, 21))
        self.lineEdit_trinkwasser_leistung.setText("")
        self.lineEdit_trinkwasser_leistung.setObjectName("lineEdit_trinkwasser_leistung")
        self.label_trinkwasser_leistung = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_trinkwasser_leistung.setEnabled(False)
        self.label_trinkwasser_leistung.setGeometry(QtCore.QRect(60, 210, 16, 20))
        self.label_trinkwasser_leistung.setObjectName("label_trinkwasser_leistung")
        self.label_8 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_8.setGeometry(QtCore.QRect(140, 140, 16, 20))
        self.label_8.setObjectName("label_8")
        self.lineEdit_trinkwasser_liter = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_trinkwasser_liter.setEnabled(False)
        self.lineEdit_trinkwasser_liter.setGeometry(QtCore.QRect(110, 210, 31, 21))
        self.lineEdit_trinkwasser_liter.setText("")
        self.lineEdit_trinkwasser_liter.setObjectName("lineEdit_trinkwasser_liter")
        self.label_Speicherinhalt = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_Speicherinhalt.setEnabled(False)
        self.label_Speicherinhalt.setGeometry(QtCore.QRect(110, 190, 111, 16))
        self.label_Speicherinhalt.setObjectName("label_Speicherinhalt")
        self.label_trinkwasser_liter = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_trinkwasser_liter.setEnabled(False)
        self.label_trinkwasser_liter.setGeometry(QtCore.QRect(150, 210, 16, 20))
        self.label_trinkwasser_liter.setObjectName("label_trinkwasser_liter")
        self.label_5 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_5.setGeometry(QtCore.QRect(20, 240, 231, 16))
        self.label_5.setObjectName("label_5")
        self.label_10 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_10.setGeometry(QtCore.QRect(20, 260, 30, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_8 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_8.setGeometry(QtCore.QRect(53, 260, 21, 20))
        self.lineEdit_8.setText("")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.line = QtWidgets.QFrame(Form_NeueWarmepumpe)
        self.line.setGeometry(QtCore.QRect(74, 260, 20, 21))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form_NeueWarmepumpe)
        self.line_2.setGeometry(QtCore.QRect(140, 260, 20, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.lineEdit_9 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_9.setGeometry(QtCore.QRect(120, 260, 21, 20))
        self.lineEdit_9.setText("")
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_11 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_11.setGeometry(QtCore.QRect(90, 260, 30, 16))
        self.label_11.setObjectName("label_11")
        self.line_3 = QtWidgets.QFrame(Form_NeueWarmepumpe)
        self.line_3.setGeometry(QtCore.QRect(203, 260, 20, 21))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.lineEdit_10 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_10.setGeometry(QtCore.QRect(186, 260, 21, 20))
        self.lineEdit_10.setText("")
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.label_12 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_12.setGeometry(QtCore.QRect(156, 260, 30, 16))
        self.label_12.setObjectName("label_12")
        self.line_4 = QtWidgets.QFrame(Form_NeueWarmepumpe)
        self.line_4.setGeometry(QtCore.QRect(268, 260, 20, 21))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.lineEdit_11 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_11.setGeometry(QtCore.QRect(250, 260, 21, 20))
        self.lineEdit_11.setText("")
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.label_13 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_13.setGeometry(QtCore.QRect(220, 260, 30, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_14.setGeometry(QtCore.QRect(285, 260, 30, 16))
        self.label_14.setObjectName("label_14")
        self.lineEdit_12 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_12.setGeometry(QtCore.QRect(313, 260, 21, 20))
        self.lineEdit_12.setText("")
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.label_6 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_6.setGeometry(QtCore.QRect(20, 290, 80, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit_13 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_13.setGeometry(QtCore.QRect(30, 310, 41, 20))
        self.lineEdit_13.setText("")
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.label_trinkwasser_leistung_2 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_trinkwasser_leistung_2.setEnabled(True)
        self.label_trinkwasser_leistung_2.setGeometry(QtCore.QRect(80, 310, 16, 20))
        self.label_trinkwasser_leistung_2.setObjectName("label_trinkwasser_leistung_2")
        self.label_7 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_7.setGeometry(QtCore.QRect(20, 333, 100, 16))
        self.label_7.setObjectName("label_7")
        self.label_trinkwasser_leistung_3 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_trinkwasser_leistung_3.setEnabled(True)
        self.label_trinkwasser_leistung_3.setGeometry(QtCore.QRect(80, 353, 16, 20))
        self.label_trinkwasser_leistung_3.setObjectName("label_trinkwasser_leistung_3")
        self.lineEdit_14 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_14.setGeometry(QtCore.QRect(30, 353, 41, 20))
        self.lineEdit_14.setText("")
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.label_2 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_2.setGeometry(QtCore.QRect(340, 40, 271, 171))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/images/Pictures/Heatpump.png"))
        self.label_2.setObjectName("label_2")
        self.lineEdit_15 = QtWidgets.QLineEdit(Form_NeueWarmepumpe)
        self.lineEdit_15.setGeometry(QtCore.QRect(150, 310, 41, 20))
        self.lineEdit_15.setText("")
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.label_trinkwasser_leistung_4 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_trinkwasser_leistung_4.setEnabled(True)
        self.label_trinkwasser_leistung_4.setGeometry(QtCore.QRect(200, 310, 16, 20))
        self.label_trinkwasser_leistung_4.setObjectName("label_trinkwasser_leistung_4")
        self.label_9 = QtWidgets.QLabel(Form_NeueWarmepumpe)
        self.label_9.setGeometry(QtCore.QRect(140, 290, 100, 16))
        self.label_9.setObjectName("label_9")
        self.line_5 = QtWidgets.QFrame(Form_NeueWarmepumpe)
        self.line_5.setGeometry(QtCore.QRect(120, 290, 20, 90))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")

        self.retranslateUi(Form_NeueWarmepumpe)
        self.checkBox_Trinkwassererwrmung.toggled['bool'].connect(self.label_HeizstabLeistung.setEnabled) # type: ignore
        self.checkBox_Trinkwassererwrmung.toggled['bool'].connect(self.label_Speicherinhalt.setEnabled) # type: ignore
        self.checkBox_Trinkwassererwrmung.toggled['bool'].connect(self.label_trinkwasser_leistung.setEnabled) # type: ignore
        self.checkBox_Trinkwassererwrmung.toggled['bool'].connect(self.label_trinkwasser_liter.setEnabled) # type: ignore
        self.checkBox_Trinkwassererwrmung.toggled['bool'].connect(self.lineEdit_trinkwasser_leistung.setEnabled) # type: ignore
        self.checkBox_Trinkwassererwrmung.toggled['bool'].connect(self.lineEdit_trinkwasser_liter.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form_NeueWarmepumpe)

    def retranslateUi(self, Form_NeueWarmepumpe):
        _translate = QtCore.QCoreApplication.translate
        Form_NeueWarmepumpe.setWindowTitle(_translate("Form_NeueWarmepumpe", "Form"))
        self.pushButton.setText(_translate("Form_NeueWarmepumpe", "Fertig"))
        self.comboBox.setItemText(0, _translate("Form_NeueWarmepumpe", "Luft"))
        self.comboBox.setItemText(1, _translate("Form_NeueWarmepumpe", "Wasser"))
        self.comboBox.setItemText(2, _translate("Form_NeueWarmepumpe", "Sole"))
        self.label.setText(_translate("Form_NeueWarmepumpe", "Energiequelle"))
        self.label_3.setText(_translate("Form_NeueWarmepumpe", "Abgabemedium"))
        self.comboBox_2.setItemText(0, _translate("Form_NeueWarmepumpe", "Wasser"))
        self.comboBox_2.setItemText(1, _translate("Form_NeueWarmepumpe", "Luft"))
        self.label_4.setText(_translate("Form_NeueWarmepumpe", "Ma?e (L,B,H)"))
        self.checkBox_Trinkwassererwrmung.setText(_translate("Form_NeueWarmepumpe", "Mit Trinkwassererw?rmung?"))
        self.label_HeizstabLeistung.setText(_translate("Form_NeueWarmepumpe", "Heizstab Leistung"))
        self.label_trinkwasser_leistung.setText(_translate("Form_NeueWarmepumpe", "kW"))
        self.label_8.setText(_translate("Form_NeueWarmepumpe", "cm"))
        self.label_Speicherinhalt.setText(_translate("Form_NeueWarmepumpe", "Speicherinhalt"))
        self.label_trinkwasser_liter.setText(_translate("Form_NeueWarmepumpe", "l"))
        self.label_5.setText(_translate("Form_NeueWarmepumpe", "COP bei unterschiedlichen Au?entemperaturen"))
        self.label_10.setText(_translate("Form_NeueWarmepumpe", "-15?C"))
        self.label_11.setText(_translate("Form_NeueWarmepumpe", "-7?C"))
        self.label_12.setText(_translate("Form_NeueWarmepumpe", "2?C"))
        self.label_13.setText(_translate("Form_NeueWarmepumpe", "7?C"))
        self.label_14.setText(_translate("Form_NeueWarmepumpe", "12?C"))
        self.label_6.setText(_translate("Form_NeueWarmepumpe", "Stromaufnahme"))
        self.label_trinkwasser_leistung_2.setText(_translate("Form_NeueWarmepumpe", "kW"))
        self.label_7.setText(_translate("Form_NeueWarmepumpe", "Bivalenztemperatur"))
        self.label_trinkwasser_leistung_3.setText(_translate("Form_NeueWarmepumpe", "?C"))
        self.label_trinkwasser_leistung_4.setText(_translate("Form_NeueWarmepumpe", "dB"))
        self.label_9.setText(_translate("Form_NeueWarmepumpe", "Schallleistungspegel"))
#from . import Waterdrop_rc
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)
main = MainWindow()
w = Ui_Form_NeueWarmepumpe()
w.setupUi(main)
main.show()
app.exec()