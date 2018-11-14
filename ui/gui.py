#! python3
# gui.py

### This file is just to experiment with GUI creation.

import os
os.chdir('D:\\Czarified\\Documents\\GitHub\\py4Dinner')
import sys
from PyQt5 import QtWidgets
from gui import Ui_MainWindow 


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())