## Add path to library (just for examples; you do not need this)
#import initExample

import numpy as np
#import scipy
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

pg.mkQApp()
win = pg.GraphicsLayoutWidget()
p1 = win.addPlot()
img = pg.ImageItem()
p1.addItem(img)


roi = pg.RectROI([8, 14], [6, 5])
#roi.addScaleHandle([0.5, 1], [0.5, 0.5])
#roi.addScaleHandle([0, 0.5], [0.5, 0.5])
p1.addItem(roi)
roi.setZValue(10)

label = win.addLabel('')
label.setText('hdoo')

# app = QtGui.QApplication([])
# 
# ## Create window with ImageView widget
# win = QtGui.QMainWindow()
# win.resize(800,800)
# imv = pg.ImageItem()
# win.setCentralWidget(imv)
# win.show()
# win.setWindowTitle('pyqtgraph example: ImageView')

## Create random 3D data set with noisy signals
data = np.random.normal(size=(200, 200))

img.setImage(data)
win.show()

def updatePlot():
    global roi, label
    position = roi.pos()
    position =np.rint(np.array(position))
    print position
    label.setText(position)

roi.sigRegionChanged.connect(updatePlot)
#updatePlot()

#img = img[np.newaxis,:,:]
# decay = np.exp(-np.linspace(0,0.3,100))[:,np.newaxis,np.newaxis]
# data = np.random.normal(size=(100, 200, 200))
# data += img * decay
# data += 2

# data = img

# ## Add time-varying signal
# sig = np.zeros(data.shape[0])
# sig[30:] += np.exp(-np.linspace(1,10, 70))
# sig[40:] += np.exp(-np.linspace(1,10, 60))
# sig[70:] += np.exp(-np.linspace(1,10, 30))
# 
# sig = sig[:,np.newaxis,np.newaxis] * 3
# data[:,50:60,50:60] += sig


## Display the data and assign each frame a time value from 1.0 to 3.0
# imv.setImage(data, xvals=np.linspace(1., 3., data.shape[0]))
# imv.setImage(data)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        #print "hell"