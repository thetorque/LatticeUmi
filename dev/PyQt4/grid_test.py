import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):      
    
        hbox = QtGui.QHBoxLayout()
        grid = QtGui.QGridLayout()
    
        #Definition des Tracing Parameters widgets
        WindowSize = QtGui.QLabel("Window size (m)")
        SampPts = QtGui.QLabel("Sampling points")
        WindowSizeEdit = QtGui.QLineEdit()
        SampPtsEdit = QtGui.QLineEdit()
        TracParamFrame = QtGui.QGroupBox(self)
        TracParamFrame.setTitle("Tracing Parameters")

        hbox.addLayout(grid)
    
        grid.addWidget(WindowSize,0,0)
        grid.addWidget(WindowSizeEdit,0,1)
        grid.addWidget(SampPts,1,0)
        grid.addWidget(SampPtsEdit,1,1)
    
        self.setLayout(hbox)
    
        self.setGeometry(300,300,350,300)
        self.show()
    
    
def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()