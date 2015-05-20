
##### a gui to display NI AO data






from PyQt4 import QtGui
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.task import LoopingCall
# from helper_widgets.helper_widgets import saved_frequencies_table
# from helper_widgets.compound_widgets import table_dropdowns_with_entry
import numpy
import time

class AO_plotter(QtGui.QWidget):
    def __init__(self, reactor, clipboard = None, cxn = None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.reactor = reactor
        self.clipboard = clipboard
        self.cxn = cxn
        self.subscribed = False
        #updater.start(c.update_rate)
        
        ## number of total analog channels

        ##self.channel = 3
        ## sampling rate

        ##self.sampling_rate = 100000
        self.load_plot_data()

        self.create_plot_layout()
        self.plot_ao_channel()
        #self.connect_labrad()
    
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
            print "channel ",i
            #plot = self.fig.add_subplot(gs[i,0])
            
            if i == 0:
                plot = self.fig.add_subplot(gs[i,0])
            else:
                plot = self.fig.add_subplot(gs[i,0],sharex=plot) ## scale the x-axis to be the same as the first plot for subsequent plots
                
            plot.set_ylabel('V')
            plot.grid(True)
            ## show x label only for the lowest channel
            plot.tick_params(axis='x',which='both',labelbottom='off')
            if i == (self.channel-1):
                plot.set_xlabel('Time (s)')
                plot.tick_params(axis='x',which='both',labelbottom='on')
            plot.set_title("Analog "+str(i))
            ## add plot to the analog_plot list
            self.analog_plot.append(plot)

        self.mpl_toolbar = NavigationToolbar2QT(self.plot_canvas, self)
        layout.addWidget(self.mpl_toolbar)
        layout.addWidget(self.plot_canvas)
        return layout
            
    def plot_ao_channel(self):
        
        #method for plotting channel p on the analog plot
        
        for p in range(self.channel):
            self.analog_plot[p].plot(self.plot_data[0], self.plot_data[p+1], '-r')
        self.plot_canvas.draw()
        
    def load_plot_data(self):
#         self.plot_data = numpy.load("test_ao_sequence1.npy")
        self.plot_data = numpy.load("ramp.npy")
        self.channel = self.plot_data.shape[0]-1 ## get the number of channel from the file
        #print self.plot_data
        
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
    widget = AO_plotter(reactor, clipboard)
    widget.show()
    reactor.run()