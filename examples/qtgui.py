from __future__ import print_function
from PyQt4 import QtCore, QtGui


app = None
qtwin = None


def do(win):
    global qtwin
    qtwin = win

    # FILE
    fm = win.menuBar().addMenu("&File")
    fm.addAction(
        QtGui.QAction("O&pen", win, shortcut="Ctrl+O", triggered=openFile)
    )



def openFile():
    filename = QtGui.QFileDialog.getOpenFileName(qtwin, 'OpenFile', "./", "text files (*.txt)")
    print(filename)




