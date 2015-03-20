from PyQt4 import QtGui, uic
import os
from clients.connection import connection
from twisted.internet.defer import inlineCallbacks

basepath =  os.path.dirname(__file__)
path = os.path.join(basepath, "DAC.ui")
base, form = uic.loadUiType(path)

class widget_ui(base, form):
    def __init__(self, parent = None):
        super(widget_ui, self).__init__(parent)
        self.setupUi(self)

class actions_widget(QtGui.QFrame, widget_ui):
    def __init__(self,reactor,cxn = None, parent=None):
        self.reactor = reactor
        self.cxn = cxn
        QtGui.QDialog.__init__(self)
        widget_ui.__init__(self)
        self.connect()
    
    @inlineCallbacks
    def connect(self):
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
        try:
            self.connect_layout()
        except Exception, e:
            print e
            self.setDisabled(True)
        self.server = yield self.cxn.get_server('NI Analog Server')
    
    def connect_layout(self):
        self.doubleSpinBox0.valueChanged.connect(self.setVoltage)
        
    @inlineCallbacks
    def setVoltage(self, voltage):
        print voltage
        val = self.types.Value(voltage, 'V')
        try:
            yield self.server.set_voltage('comp1', val, context = self.context)
        except self.Error as e:
            #old_value =  yield self.server.frequency(self.chan, context = self.context)
            #self.setFreqNoSignal(old_value)
            #self.displayError(e.msg)
            pass
    
    @inlineCallbacks
    def disable(self):
        self.setDisabled(True)
        yield None
    
    def closeEvent(self, x):
        self.reactor.stop()  
        
if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    electrodes = actions_widget(reactor)
    electrodes.show()
    reactor.run()