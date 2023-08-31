from __future__ import print_function
from PyQt6 import QtCore, QtWidgets, QtGui


app = None
qtwin = None


def do(win):
    global qtwin
    qtwin = win

    # FILE
    fm = win.menuBar().addMenu("&File")
    action = QtGui.QAction('Import mail', win)
    action.triggered.connect(openFile)
    fm.addAction(action)



def openFile():
    print("opening dialogue window")
    filename = QtWidgets.QFileDialog.getOpenFileName(qtwin, "OpenFile", "./", "text files (*.txt)")
    print(filename)




