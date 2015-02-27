from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.task import LoopingCall
from helper_widgets.helper_widgets import saved_frequencies_table
from helper_widgets.compound_widgets import table_dropdowns_with_entry
import numpy
import time
#from drift_tracker_config import config_729_tracker as c

'''
Drift Tracker GUI. 
Version 1.15
'''

class drift_tracker(QtGui.QWidget):
    def __init__(self, reactor, clipboard = None, cxn = None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.reactor = reactor
        self.clipboard = clipboard
        self.cxn = cxn
        self.subscribed = False
        #see if favoirtes are provided in the configuration. if not, use an empty dictionary
        #try:
        #    self.favorites =  c.favorites
        #except AttributeError:
        #    self.favorites = {}
        #updater = LoopingCall(self.update_lines)
        #updater.start(c.update_rate)
        
        ## number of total analog channels
        self.channel = 3
        ## sampling rate
        self.sampling_rate = 100000
        
        self.create_layout()
        self.load_plot_data()
        self.plot_ao_channel(0)
        self.plot_ao_channel(1)
        self.plot_ao_channel(2)
        #self.connect_labrad()
    
    def create_layout(self):
        layout = QtGui.QGridLayout()
        plot_layout = self.create_plot_layout()
        #widget_layout = self.create_widget_layout()
        #spectrum_layout = self.create_spectrum_layout()
        layout.addLayout(plot_layout, 0, 0, 1, 2)
        #layout.addLayout(widget_layout, 1, 0, 1, 1)
        #layout.addLayout(spectrum_layout, 1, 1, 1, 1)
        self.setLayout(layout)
        #self.plot_ao_channel(0)
   
    def create_plot_layout(self):
        layout = QtGui.QVBoxLayout()
        self.fig = Figure()
        self.plot_canvas = FigureCanvas(self.fig)
        self.plot_canvas.setParent(self)
        
        ## create empty list of plot
        self.analog_plot = []
        
        ## create a grid according to the number of channels
        gs = gridspec.GridSpec(self.channel, 1, wspace=0.15, left = 0.05, right = 0.95)
        
        ## loop and create all channel plots
        for i in range(self.channel):
            print i
            plot = self.fig.add_subplot(gs[i,0])
            plot.set_ylabel('V')
            ## show x label only for the lowest channel
            plot.tick_params(axis='x',which='both',labelbottom='off')
            if i == (self.channel-1):
                print "True"
                plot.set_xlabel('Time (s)')
                plot.tick_params(axis='x',which='both',labelbottom='on')
            plot.set_title("Analog "+str(i))
            ## add plot to the analog_plot list
            self.analog_plot.append(plot)

        #self.mpl_toolbar = NavigationToolbar2QT(self.drift_canvas, self)
        #layout.addWidget(self.mpl_toolbar)
        layout.addWidget(self.plot_canvas)
        return layout
            
    def plot_ao_channel(self, p):
        
        #method for plotting channel p on the analog plot

        self.analog_plot[p].plot(self.plot_data[0], self.plot_data[p+1], '-r')
        
        self.plot_canvas.draw()
        
    def load_plot_data(self):
        self.plot_data = numpy.array([[0,0.2,0.4,0.6,0.8,1.0],[0,1,2,3,4,5],[5,4,3,2,1,0],[1,2,3,2,1,0]])
        
    @inlineCallbacks
    def disable(self):
        self.setDisabled(True)
        yield None
        
    def displayError(self, text):
        #runs the message box in a non-blocking method
        message = QtGui.QMessageBox(self)
        message.setText(text)
        message.open()
        message.show()
        message.raise_()
    
    def closeEvent(self, x):
        self.reactor.stop()  
    
if __name__=="__main__":
    a = QtGui.QApplication( [] )
    clipboard = a.clipboard()
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    widget = drift_tracker(reactor, clipboard)
    widget.show()
    reactor.run()
