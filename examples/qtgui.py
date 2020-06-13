from __future__ import print_function
from PyQt5 import QtCore, QtWidgets


app = None
qtwin = None


def do(win):
    global qtwin
    qtwin = win

    # FILE
    fm = win.menuBar().addMenu("&File")
    fm.addAction(
        QtWidgets.QAction("O&pen", win, shortcut="Ctrl+O", triggered=openFile)
    )



def openFile():
    filename = QtWidgets.QFileDialog.getOpenFileName(qtwin, 'OpenFile', "./", "text files (*.txt)")
    print(filename)




