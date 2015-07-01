from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
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

class dac_widget(QtGui.QFrame, widget_ui):
    
    SIGNALID = 3902384
    
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
        
        ## setup a connection to listen to a signal from the server
        yield self.server.signal__new_voltage(self.SIGNALID, context = self.context)
        yield self.server.addListener(listener = self.followSignal, source = None, ID = self.SIGNALID, context = self.context)
        
        # get values from the registry and set the value of each spin box
        
        value1 = yield self.server.get_voltage('B_x')
        value2 = yield self.server.get_voltage('B_y')
        value3 = yield self.server.get_voltage('B_z')
        value4 = yield self.server.get_voltage('MOT')

        self.doubleSpinBox0.blockSignals(True)
        self.doubleSpinBox0.setValue(value1['V'])
        self.doubleSpinBox0.blockSignals(False)
        
        self.doubleSpinBox1.blockSignals(True)
        self.doubleSpinBox1.setValue(value2['V'])
        self.doubleSpinBox1.blockSignals(False)

        self.doubleSpinBox2.blockSignals(True)
        self.doubleSpinBox2.setValue(value3['V'])
        self.doubleSpinBox2.blockSignals(False)
        
        self.doubleSpinBox3.blockSignals(True)
        self.doubleSpinBox3.setValue(value4['V'])
        self.doubleSpinBox3.blockSignals(False)
        #self.doubleSpinBox0.value = value1['V']
        #yield self.load_initial_setting()
        print "connect"
        
    
    def connect_layout(self):
        # set the layout to display the name of the channel
        self.doubleSpinBox0.valueChanged.connect(lambda: self.setVoltage('B_x'))
        self.doubleSpinBox1.valueChanged.connect(lambda: self.setVoltage('B_y'))
        self.doubleSpinBox2.valueChanged.connect(lambda: self.setVoltage('B_z'))
        self.doubleSpinBox3.valueChanged.connect(lambda: self.setVoltage('MOT'))
        self.label0.setText('B_x')
        self.label1.setText('B_y')
        self.label2.setText('B_z')
        self.label3.setText('MOT')
        
    @inlineCallbacks
    def setVoltage(self, chan_name):
        '''
        Set the voltage according to the given channel name
        '''
        try:
            if chan_name == 'B_x':
                voltage = self.doubleSpinBox0.value()
                val = self.types.Value(voltage, 'V')
                yield self.server.set_voltage('B_x', val, context = self.context)
            elif chan_name == 'B_y':
                voltage = self.doubleSpinBox1.value()
                val = self.types.Value(voltage, 'V')
                yield self.server.set_voltage('B_y', val, context = self.context)
            elif chan_name == 'B_z':
                voltage = self.doubleSpinBox2.value()
                val = self.types.Value(voltage, 'V')
                yield self.server.set_voltage('B_z', val, context = self.context)
            elif chan_name == 'MOT':
                voltage = self.doubleSpinBox3.value()
                val = self.types.Value(voltage, 'V')
                yield self.server.set_voltage('MOT', val, context = self.context)
            
        except self.Error as e:
            #old_value =  yield self.server.frequency(self.chan, context = self.context)
            #self.setFreqNoSignal(old_value)
            #self.displayError(e.msg)
            pass
        
    def followSignal(self, x, y):
        '''
        Use to update the display of the channel once the signal is received from the server that the new values are there
        '''
        chan, param = y
        if chan == 'B_x':
            print "B_x just got updated"
            self.doubleSpinBox0.blockSignals(True)
            self.doubleSpinBox0.setValue(param['V'])
            self.doubleSpinBox0.blockSignals(False)
        elif chan == "B_y":
            print "B_y just got updated"
            self.doubleSpinBox1.blockSignals(True)
            self.doubleSpinBox1.setValue(param['V'])
            self.doubleSpinBox1.blockSignals(False)
        elif chan == "B_z":
            print "B_z just got updated"
            self.doubleSpinBox2.blockSignals(True)
            self.doubleSpinBox2.setValue(param['V'])
            self.doubleSpinBox2.blockSignals(False)
        elif chan == "MOT":
            print "MOT just got updated"
            self.doubleSpinBox3.blockSignals(True)
            self.doubleSpinBox3.setValue(param['V'])
            self.doubleSpinBox3.blockSignals(False)
    
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
    dac = dac_widget(reactor)
    dac.show()
    reactor.run()