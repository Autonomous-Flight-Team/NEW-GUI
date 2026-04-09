# THIS IS TRIAL CODE TO SEE HOW PYQTGRAPH WORKS.

# importing pyqtgraph as pg
import pyqtgraph as pg

# importing QtCore and QtGui from the pyqtgraph module
from pyqtgraph.Qt import QtCore, QtGui

# importing numpy as np
import numpy as np

# creating a pyqtgraph plot window
window = pg.plot()

# title
title = "Sample PyQtGraph"

# setting window title
window.setWindowTittle(title)

# create list for y-axis
y1 = [5, 5, 7, 10, 3, 8, 9, 1, 6, 2]

# create horizontal list i.e x-axis
x = [1, 10, 4, 5, 7, 3, 6, 8, 9, 2]

# create pyqt5graph bar graph item
# with bar colors = green
bargraph1 = pg.BarGraphItem(x = x, height = y1, width = 0.6, brush = 'g')

# adding bargraph item to the window
window.addItem(bargraph1)

# main method
if __name__ == '__main__':
    
    # importing system
    import sys

    # Start Qt event loop unless running in interactive mode or using
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

