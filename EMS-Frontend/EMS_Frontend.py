
import os
import sys

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Settings = QPushButton(self.centralwidget)
        self.Settings.setGeometry(QRect(640, 460, 75, 23))
        self.Settings.setObjectName("Settings")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QRect(630, 360, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Settings.setText(_translate("MainWindow", "Settings"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))



app = QApplication(sys.argv)
main = MainWindow()
w = Ui_MainWindow()
w.setupUi(main)
main.show()
app.exec()