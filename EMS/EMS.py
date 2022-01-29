from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import numpy as np
import time

class RandomDataGeneration(QtCore.QThread):
    """
    Mandatory Class. This Class must exist.
    """
    new_data = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)

    def data_generation(self):

        while True:
            waiting_time = np.random.randint(1,4) # waiting time is given by a random number.
            print(waiting_time)
            time.sleep(waiting_time)
            self.x = np.random.rand(10)
            self.y = np.random.rand(10)
            print(self.x)
            print(self.y)
            self.new_data.emit()

    def run(self):
        self.data_generation()




app = QtWidgets.QApplication(sys.argv)
MainWindow = MyMainWindow()
MainWindow.show()
sys.exit(app.exec_())