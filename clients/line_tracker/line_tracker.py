from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.task import LoopingCall
from helper_widgets.helper_widgets import saved_frequencies_table
from helper_widgets.compound_widgets import table_dropdowns_with_entry
import numpy
import time
from line_tracker_config import config_tracker as c
from functools import partial

'''
Drift Tracker GUI. 
Version 1.15
'''

class line_tracker(QtGui.QWidget):
    def __init__(self, reactor, clipboard = None, cxn = None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.reactor = reactor
        self.clipboard = clipboard
        self.cxn = cxn
        self.subscribed = False
        #see if favoirtes are provided in the configuration. if not, use an empty dictionary
        try:
            self.favorites =  c.favorites
        except AttributeError:
            self.favorites = {}

        self.number_of_channel = 4
        
        self.create_layout()
        self.connect_labrad()
        
        updater = LoopingCall(self.update_lines)
        updater.start(c.update_rate)
        

    def create_layout(self):
        layout = QtGui.QGridLayout()
        plot_layout = self.create_drift_layout()
        layout.addLayout(plot_layout,0,0)
        
        widget_layout = self.create_widget_layout()
#         spectrum_layout = self.create_spectrum_layout()
#         layout.addLayout(plot_layout, 0, 0, 1, 2)
        layout.addLayout(widget_layout, 1, 0)
#         layout.addLayout(spectrum_layout, 1, 1, 1, 1)
        self.setLayout(layout)
   
    def create_drift_layout(self):
        layout = QtGui.QVBoxLayout()
        self.fig = Figure()
        self.plot_canvas = FigureCanvas(self.fig)
        self.plot_canvas.setParent(self)  
        #gs = gridspec.GridSpec(1, 2, wspace=0.15, left = 0.05, right = 0.95)
        line_drift = self.fig.add_subplot(1,1,1)
        line_drift.ticklabel_format(useOffset=False)
        line_drift.set_xlabel('Time (min)')
        line_drift.set_ylabel('kHz')
        line_drift.set_title("Line Drift")
        self.line_drift = line_drift
        self.line_drift_lines = []
        self.line_drift_fit_line = []
        self.line_all_line = []

        self.mpl_toolbar = NavigationToolbar2QT(self.plot_canvas, self)
        layout.addWidget(self.mpl_toolbar)
        layout.addWidget(self.plot_canvas)
        return layout

    def create_widget_layout(self):
        layout = QtGui.QGridLayout()
        self.submit_button = []
        self.freq_enter_box = []
        self.freq_label_id = []
        self.freq_label_current = []
        self.remove_button = []
        self.track_duration_box = []
        for i in range(self.number_of_channel):
            
            self.submit_button.append(QtGui.QPushButton("Submit"))
            
            spin_box = QtGui.QDoubleSpinBox()
            spin_box.setSuffix(' kHz')
            spin_box.setRange(-50000.0, 50000.0)
            spin_box.setDecimals(5)
            self.freq_enter_box.append(spin_box)
            
            label = QtGui.QLabel(str(i+1))
            self.freq_label_id.append(label)
            
            freq_value = 0.000
            freq_value_label = QtGui.QLabel("%.5f kHz" % freq_value)
            self.freq_label_current.append(freq_value_label)
            
            self.remove_button.append(QtGui.QPushButton("Remove"))
            
            track_duration_spin_box = QtGui.QDoubleSpinBox()
            track_duration_spin_box.setSuffix(' min')
            track_duration_spin_box.setDecimals(1)
            self.track_duration_box.append(track_duration_spin_box)
            
            layout.addWidget(self.freq_label_id[i],i,0)
            layout.addWidget(self.freq_enter_box[i],i,1)
            layout.addWidget(self.submit_button[i],i,2)
            layout.addWidget(self.freq_label_current[i],i,3)
            layout.addWidget(self.remove_button[i],i,4)
            layout.addWidget(self.track_duration_box[i],i,5)
            
        return layout

    def connect_layout(self):

        for i in range(self.number_of_channel):
            #self.submit_button[i].clicked.connect(lambda i=i: self.on_entry(i))
            self.track_duration_box[i].valueChanged.connect(partial(self.on_duration_change, i, 9))
            self.submit_button[i].clicked.connect(partial(self.on_entry , i))
            self.remove_button[i].clicked.connect(partial(self.on_remove , i))

    
    @inlineCallbacks
    def initialize_layout(self):
        server = yield self.cxn.get_server('Line Tracker')
#         transitions = yield server.get_transition_names()
#         self.entry_table.fill_out(transitions)
        for i in range(self.number_of_channel):
            duration = yield server.history_duration(i+1)
            self.track_duration_box[i].setValue(duration['min'])

        yield self.on_new_fit(None, None)
    
  
    @inlineCallbacks
    def on_entry(self, i, j):
        server = yield self.cxn.get_server('Line Tracker')
        freq = self.freq_enter_box[i].value()
        print freq
        print "submit button", i
        freq_with_units = self.WithUnit(freq, 'kHz')
        try:
            yield server.set_measurement(freq_with_units, i + 1)
        except self.Error as e:
            self.displayError(e.msg)
    
    @inlineCallbacks
    def on_duration_change(self, i, j, value):
        #print i, j, value
        server = yield self.cxn.get_server('Line Tracker')
        rate_line = self.WithUnit(value, 'min')
        print rate_line
        yield server.history_duration(i+1, rate_line)
                    
    @inlineCallbacks
    def on_remove(self, i, j):
        server = yield self.cxn.get_server('Line Tracker')
        try:
            yield server.remove_measurement(i + 1)
        except self.Error as e:
            self.displayError(e.msg)
        
    @inlineCallbacks
    def connect_labrad(self):
        from labrad.units import WithUnit
        from labrad.types import Error
        self.WithUnit = WithUnit
        self.Error = Error
        if self.cxn is None:
            from clients.connection import connection
            self.cxn = connection()
            yield self.cxn.connect()
        self.context = yield self.cxn.context()
        try:
            yield self.subscribe_tracker()
#             print "yes"
        except Exception as e:
#             print e
#             print 'no'
            self.setDisabled(True)
        self.cxn.add_on_connect('Line Tracker', self.reinitialize_tracker)
        self.cxn.add_on_disconnect('Line Tracker', self.disable)
        self.connect_layout()
        
    @inlineCallbacks
    def subscribe_tracker(self):
        server = yield self.cxn.get_server('Line Tracker')
        #print c.ID
        yield server.signal__new_fit(c.ID, context = self.context)
        yield server.addListener(listener = self.on_new_fit, source = None, ID = c.ID, context = self.context)
        yield self.initialize_layout()
        self.subscribed = True
    
    @inlineCallbacks
    def reinitialize_tracker(self):
        self.setDisabled(False)
        server = yield self.cxn.get_server('Line Tracker')
        yield server.signal__new_fit(c.ID, context = self.context)
        if not self.subscribed:
            yield server.addListener(listener = self.on_new_fit, source = None, ID = c.ID, context = self.context)
            yield self.initialize_layout()
            self.subscribed = True
    
    @inlineCallbacks
    def on_new_fit(self, x, y):
        yield self.update_lines()
        #print x, y
        yield self.update_fit()
    
    @inlineCallbacks
    def update_fit(self):
        try:
            server = yield self.cxn.get_server('Line Tracker')
            #number = yield server.get_tracker_number()

        except Exception as e:
            #no fit available
            print e
            pass
        else:
            ## clear all curves
            self.clear_plot_canvas(self.line_drift_lines)
            self.clear_plot_canvas(self.line_drift_fit_line)
            self.line_drift.set_color_cycle(None) # reset the color rotation such that line 1 is always the same color
    
            for i in range(self.number_of_channel):
                j = i+1
                
                ## get all lines
                history_line = yield server.get_fit_history(j)
                all_history_line = yield server.get_all_history(j)
                
                ## plot if lines are not empty
                if len(history_line)>0:
                    fit_param = yield server.get_fit_parameters(j)
                    inunits_f = [(t['min'], freq['kHz']) for (t,freq) in history_line]
                    self.update_track(inunits_f, self.line_drift, self.line_drift_lines)
                    self.plot_fit_f(fit_param, inunits_f[0][0], inunits_f[-1][0]) ## send fit parameter and range to line fitter

                if len(all_history_line)>0:
                    history_inunits_f = [(t['min'], freq['kHz']) for (t,freq) in all_history_line]
                    self.update_history_track(history_inunits_f, self.line_drift, self.line_drift_lines)

#     
    def plot_fit_f(self, p, xmin, xmax):

        points = 1000
        x = numpy.linspace(xmin, xmax, points) 
        y = numpy.polyval(p, 60*x)
        l = self.line_drift.plot(x, y, '-r')[0]
        #label = self.line_drift.annotate('Slope {0:.1f} Hz/sec'.format(10**6 * p[-2]), xy = (0.5, 0.8), xycoords = 'axes fraction', fontsize = 13.0)
        self.line_drift_fit_line.append(l)
        #self.line_drift_fit_line.append(label)
        self.plot_canvas.draw()
    
    @inlineCallbacks
    def update_lines(self):
        try:
            server = yield self.cxn.get_server('Line Tracker')
            for i in range(self.number_of_channel):
                freq = yield server.get_current_line(i+1)
                self.freq_label_current[i].setText("%.5f kHz" % freq['kHz'])
        except Exception as e:
            print e
            #no lines available
            returnValue(None)
        else:
            pass
            #self.update_spectrum(lines)
            #self.update_listing(lines)
            #returnValue(lines)
#     
    def clear_plot_canvas(self, lines):
                #clear all current lines
        for i in range(len(lines)):
            line = lines.pop()
            line.remove()
    
    def update_history_track(self, meas, axes, lines):

        x = numpy.array([m[0] for m in meas])
        y = [m[1] for m in meas]
        #annotate the last point
        try:
            last = y[-1]
        except IndexError:
            pass
#         else:
#             label = axes.annotate('Last: {0:.2f} {1}'.format(last, axes.get_ylabel()), xy = (0.5, 0.9), xycoords = 'axes fraction', fontsize = 13.0)
#             lines.append(label)
        #line = axes.plot(x,y, 'b*')[0]
        line = axes.plot(x,y, 'b.')[0]
        lines.append(line)
        self.plot_canvas.draw()
                    
    def update_track(self, meas, axes, lines):

        x = numpy.array([m[0] for m in meas])
        y = [m[1] for m in meas]
        #annotate the last point
        try:
            last = y[-1]
        except IndexError:
            pass
#         else:
#             label = axes.annotate('Last: {0:.2f} {1}'.format(last, axes.get_ylabel()), xy = (0.5, 0.9), xycoords = 'axes fraction', fontsize = 13.0)
#             lines.append(label)
        #line = axes.plot(x,y, 'b*')[0]
        line = axes.plot(x,y, '*')[0]
        lines.append(line)
        self.plot_canvas.draw()
#         

        
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
    widget = line_tracker(reactor, clipboard)
    widget.show()
    reactor.run()
