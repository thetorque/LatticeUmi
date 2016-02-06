from PyQt4 import QtGui
from twisted.internet.defer import inlineCallbacks

class LATTICE_GUI(QtGui.QMainWindow):
    def __init__(self, reactor, clipboard, parent=None):
        super(LATTICE_GUI, self).__init__(parent)
        self.clipboard = clipboard
        self.reactor = reactor
        self.connect_labrad()

    @inlineCallbacks
    def connect_labrad(self):
        from connection import connection
        cxn = connection()
        yield cxn.connect()
        self.create_layout(cxn)
    
    def create_layout(self, cxn):
        contrl_widget = self.makeControlWidget(reactor, cxn)
        #histogram = self.make_histogram_widget(reactor, cxn)
        drift_tracker = self.make_drift_tracker_widget(reactor, cxn)
        centralWidget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        
        ### start script scanner GUI
        from clients.script_scanner_gui.script_scanner_gui import script_scanner_gui
        script_scanner = script_scanner_gui(reactor, cxn)
        script_scanner.show()
        
        ### start Andor video GUI
        from clients.AndorVideo import AndorVideo
        andor_video = AndorVideo(reactor, cxn)
        #andor_video.show()        
        

        line_tracker_widget = self.make_line_tracker_widet(reactor, cxn)
        
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.addTab(andor_video,'&Camera')
        self.tabWidget.addTab(contrl_widget,'&Control')
        self.tabWidget.addTab(line_tracker_widget,'&Line Tracker')
        
        #self.tabWidget.addTab(histogram, '&Readout Histogram')
        self.tabWidget.addTab(drift_tracker, '&Clock Drift Tracker')
        layout.addWidget(self.tabWidget)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        
    def make_line_tracker_widet(self, reactor, cxn):
        from clients.line_tracker.line_tracker import line_tracker
        widget = line_tracker(reactor, cxn = cxn, clipboard = self.clipboard)
        return widget
    
    def make_drift_tracker_widget(self, reactor, cxn):
        from clients.drift_tracker.drift_tracker import drift_tracker
        widget = drift_tracker(reactor, cxn = cxn, clipboard = self.clipboard)
        return widget
    
#     def make_histogram_widget(self, reactor, cxn):
#         histograms_tab = QtGui.QTabWidget()
#         from readout_histogram import readout_histogram
#         pmt_readout = readout_histogram(reactor, cxn)
#         histograms_tab.addTab(pmt_readout, "PMT")
#         from camera_histogram import camera_histogram
#         camera_histogram_widget = camera_histogram(reactor, cxn)
#         histograms_tab.addTab(camera_histogram_widget, "Camera")
#         return histograms_tab
    
    def makeTranslationStageWidget(self, reactor):
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()
        widget.setLayout(gridLayout)
        return widget
    
    def makeControlWidget(self, reactor, cxn):
        widget = QtGui.QWidget()
        #from electrode_client.electrode import electrode_widget
        #from clients.Simple_DAC_control import dac_widget
        #from common.clients.CAVITY_CONTROL import cavityWidget
        #from common.clients.multiplexer.MULTIPLEXER_CONTROL import multiplexerWidget
        #from PMT_CONTROL import pmtWidget
        from SWITCH_CONTROL import switchWidget
        from DDS_CONTROL import DDS_CONTROL
        from LINETRIGGER_CONTROL import linetriggerWidget
        #from quick_actions.quick_actions import actions_widget
        #from indicator.indicator import indicator_widget
        #from agilent_E3633A.agilent_E3633A import magnet_Control, oven_Control
        gridLayout = QtGui.QGridLayout()
        #gridLayout.addWidget(dac_widget(reactor, cxn),    0,0)
        #gridLayout.addWidget(actions_widget(reactor, cxn),      1,0,1,2)
        #gridLayout.addWidget(indicator_widget(reactor, cxn),    2,0,1,2)
        #gridLayout.addWidget(magnet_Control(reactor, cxn),      3,0,1,1)
        #gridLayout.addWidget(oven_Control(reactor, cxn),        3,1,1,1)
        #gridLayout.addWidget(cavityWidget(reactor),             0,2,3,2)
        #gridLayout.addWidget(multiplexerWidget(reactor),        0,4,3,1)
        gridLayout.addWidget(switchWidget(reactor, cxn),        0,0)
        #gridLayout.addWidget(pmtWidget(reactor),                3,2,1,1)
        
        gridLayout.addWidget(DDS_CONTROL(reactor, cxn),         1,0)
        gridLayout.addWidget(linetriggerWidget(reactor, cxn),   2,0)
        widget.setLayout(gridLayout)
        return widget

    def closeEvent(self, x):
        self.reactor.stop()

if __name__=="__main__":
    a = QtGui.QApplication( [] )
    clipboard = a.clipboard()
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    latticeGUI = LATTICE_GUI(reactor, clipboard)
    latticeGUI.setWindowTitle('Lattice GUI')
    latticeGUI.show()
    reactor.run()