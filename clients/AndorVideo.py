from PyQt4 import QtGui, QtCore
from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from clients.connection import connection
#from connection import connection
import numpy as np
import pyqtgraph as pg


class AndorVideo(QtGui.QWidget):
    
    SIGNALID = 3925252
    
    
    def __init__(self, reactor, cxn = None, parent=None):
        super(AndorVideo, self).__init__()
        self.reactor = reactor
        self.cxn = cxn
        from labrad.units import WithUnit
        self.WithUnit = WithUnit
        self.connect()
        self.setup_layout()
        self.connect_layout()
        
    @inlineCallbacks
    def connect(self):
        print "here"
        from labrad import types
        self.types = types
        from labrad.units import WithUnit
        from labrad.types import Error
        self.WithUnit = WithUnit
        self.Error = Error
        if self.cxn is None:
            self.cxn = connection()
            yield self.cxn.connect()
        self.context = yield self.cxn.context()
        self.camera_server = yield self.cxn.get_server('Andor Server')
        
        yield self.camera_server.signal__new_image(self.SIGNALID, context = self.context)
        yield self.camera_server.addListener(listener = self.followSignal, source = None, ID = self.SIGNALID, context = self.context)
        
        self.parameter_server = yield self.cxn.get_server('ParameterVault')
        
        ## setup a connection to listen to a signal from the server
        #yield self.server.signal__new_voltage(self.SIGNALID, context = self.context)
        #yield self.server.addListener(listener = self.followSignal, source = None, ID = self.SIGNALID, context = self.context)
        
        
        print "Andor video connect"
        
    def followSignal(self, s, i):
        '''
        Use to update the display of the channel once the signal is received from the server that the new values are there
        '''
        message, image, image_main, pos, binning = i
        
        s_image = np.array(image[0])
        self.ccd_view_0.setImage(s_image)
        s_average = np.average(s_image) ## shows only two decimal point
        self.label_s.setText("Average S: %.2f" % s_average, bold=True, size = '18pt')
        
        p_image = np.array(image[1])
        self.ccd_view_1.setImage(p_image)
        p_average = np.average(p_image)
        self.label_p.setText("Average P: %.2f" % p_average, bold=True, size = '18pt')
        
        bg_image = np.array(image[2])
        self.ccd_view_2.setImage(bg_image)
        bg_average = np.average(bg_image)
        self.label_bg.setText("Average BG: %.2f" % bg_average, bold=True, size = '18pt')
        
        self.img_view.setImage(np.array(image_main))
        self.img_view.setPos(pos[0],pos[1])
        self.img_view.setScale(binning)
        
        print message
        
    def setup_layout(self):
        self.setWindowTitle("Andor Image Display")
        #layout
        layout = QtGui.QGridLayout()
        
        pg.mkQApp()
        main_win = pg.GraphicsLayoutWidget()
        self.p1 = main_win.addPlot()
        self.img_view = pg.ImageItem()
        self.p1.addItem(self.img_view)
        
        ### add ROI
        
        self.roi = pg.RectROI([268, 224], [6, 5])
        self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.p1.addItem(self.roi)
        self.roi.setZValue(10)
        
        
        layout.addWidget(main_win,0,0,1,6)
        
        ### add aux display for CCD images
        win_0 = pg.GraphicsLayoutWidget()
        self.p_sub_0 = win_0.addPlot()
        self.ccd_view_0 = pg.ImageItem()
        self.p_sub_0.addItem(self.ccd_view_0)
        
        self.label_s = win_0.addLabel('',1,0) # add label below the plot
        layout.addWidget(win_0, 1, 0,1,2)
        
        
        win_1 = pg.GraphicsLayoutWidget()
        self.p_sub_1 = win_1.addPlot()
        self.ccd_view_1 = pg.ImageItem()
        self.p_sub_1.addItem(self.ccd_view_1)
        self.label_p = win_1.addLabel('',1,0)
        layout.addWidget(win_1, 1, 2,1,2)
        
        win_2 = pg.GraphicsLayoutWidget()
        self.p_sub_2 = win_2.addPlot()
        self.ccd_view_2 = pg.ImageItem()
        self.p_sub_2.addItem(self.ccd_view_2)
        self.label_bg = win_2.addLabel('',1,0)
        layout.addWidget(win_2, 1, 4,1,2)
         

        #add lines for the cross
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.vLine.setZValue(11)
        self.hLine.setZValue(11)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)
        #set the layout and show
        self.setLayout(layout)
        self.show()
        #self.roi.sigRegionChanged.connect(self.updateROI)
        self.roi.sigRegionChangeFinished.connect(self.updateROI)
        #self.label = main_win.addLabel('')
        #self.label.setText('hdoo')
    

    def updateROI(self):
        position = self.roi.pos()
        size = self.roi.size()
        position =np.rint(np.array(position))
        size = np.floor(np.array(size))
        print position
        print size
        self.update_ROI_parameter_vault(position, size)
        
    @inlineCallbacks
    def update_ROI_parameter_vault(self, position, size):
        '''
        send the ROI region to parameter vault for cropping the image
        '''
        
        pv = self.parameter_server
        yield pv.set_parameter('CCD_settings','x_min_cropped',position[0])
        yield pv.set_parameter('CCD_settings','x_max_cropped',position[0]+size[0])
        yield pv.set_parameter('CCD_settings','y_min_cropped',position[1])
        yield pv.set_parameter('CCD_settings','y_max_cropped',position[1]+size[1])

        #self.label.setText(position)
     
    def mouse_clicked(self, event):
        '''
        draws the cross at the position of a double click
        '''
        pos = event.pos()
        if self.p1.sceneBoundingRect().contains(pos) and event.double():
            #only on double clicks within bounds
            mousePoint = self.p1.vb.mapToView(pos)
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
     
    def connect_layout(self):
        self.p1.scene().sigMouseClicked.connect(self.mouse_clicked)

    def on_auto_levels_button(self, checked):
        self.img_view.autoLevels()
     
    def on_auto_range_button(self, checked):
        self.img_view.autoRange()
 
    def closeEvent(self, event):
        self.reactor.stop() 

        
if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    dac = AndorVideo(reactor)
    dac.show()
    reactor.run()