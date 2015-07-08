"""
### BEGIN NODE INFO
[info]
name = Line Tracker
version = 1.0
description = 

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""
from labrad.server import setting, LabradServer, Signal
from labrad.units import WithUnit
from twisted.internet.defer import returnValue, inlineCallbacks
import time
from Line_tracker_config import config as conf
from Line_calculator import Transitions_Hg, fitter
import numpy
from Line_tracker_class import Line

class LineTracker(LabradServer):
    """Provides ability to track drifts of the SD line"""
    name = 'Line Tracker'
    
    onNewFit = Signal( 768120, 'signal: new fit', '' )
    
    @inlineCallbacks
    def initServer(self):
        self.start_time = time.time() ## start time upon initialization of the server
#         self.keep_line_center_measurements = conf.keep_line_center_measurements
#         self.keep_B_measurements = conf.keep_B_measurements
#         self.tr = Transitions_SD()
#         self.fitter = fitter()
#         self.t_measure_line_center = numpy.array([])
#         self.t_measure_B = numpy.array([])
#         self.B_field = numpy.array([])
#         self.line_center = numpy.array([])
#         self.B_fit = None
#         self.line_center_fit = None
#         self.dv = None
        self.numbers_of_tracker = 0
        self.Line_tracker = [] ## array to keep track of all the line tracker object
        self.dv_save_context = [] ## array to keep track of all the save context
#         yield self.connect_data_vault()
        yield self.setupListeners()
    

    
    @inlineCallbacks
    def setup_dv_dataset(self, number_of_tracker):
        try:
            context_ID = number_of_tracker
            
            self.dv = yield self.client.data_vault
            directory = list(conf.save_folder)
            localtime = time.localtime()
            dirappend = [time.strftime("%Y%b%d",localtime), time.strftime("%H%M_%S", localtime)]
            directory.extend(dirappend)
            yield self.dv.cd(directory, True, context = (0, context_ID))
            
            dataset_name = str(number_of_tracker)

            yield self.dv.new(dataset_name, [('t', 'sec')], [('Line Center','Line Center','kHz')], context = (0, context_ID))
            yield self.dv.add_parameter('start_time', self.start_time, context = (0, context_ID))
        except AttributeError:
            pass
        
    @inlineCallbacks
    def setupListeners(self):
        yield self.client.manager.subscribe_to_named_message('Server Connect', conf.signal_id, True)
        yield self.client.manager.subscribe_to_named_message('Server Disconnect', conf.signal_id+1, True)
        yield self.client.manager.addListener(listener = self.followServerConnect, source = None, ID = conf.signal_id)
        yield self.client.manager.addListener(listener = self.followServerDisconnect, source = None, ID = conf.signal_id+1)
    
    @inlineCallbacks
    def followServerConnect(self, cntx, serverName):
        serverName = serverName[1]
        if serverName == 'Data Vault':
            yield self.connect_data_vault()
        else:
            yield None
    
    @inlineCallbacks
    def followServerDisconnect(self, cntx, serverName):
        serverName = serverName[1]
        if serverName == 'Data Vault':
            self.dv = None
        yield None
        
    @setting(1, 'Add Tracker', returns = '')
    def add_tracker(self, c):
        '''Add the instance of the tracker'''
        self.Line_tracker.append(Line(self.start_time,len(self.Line_tracker))) ## create an instance of Line with given start time and incremental ID
        self.numbers_of_tracker = self.numbers_of_tracker + 1
        self.setup_dv_dataset(self.numbers_of_tracker)
    
        
    @setting(2, 'Set Measurement', freq = 'v[kHz]', time_offset = 'v', tracker_number = 'i', returns = '') ## input tracker number start from 1
    def set_measurement(self, c, freq, time_offset = 0.0, tracker_number = 1):
        '''set_measurement to the corresponding tracker'''
        tracker_id = tracker_number - 1
        tracker = self.Line_tracker[tracker_id]
        tracker.set_measurement(freq)
        t_measure = time.time() - self.start_time
        self.save_result_datavault(t_measure, freq, tracker_number)
        
    @inlineCallbacks
    def save_result_datavault(self, t_measure, freq, tracker_number):
        try:
            yield self.dv.add((t_measure, freq), context = (0, tracker_number))
        except AttributeError:
            print 'Data Vault Not Available, not saving'
            yield None
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    @setting(4, "Get Fit Parameters", name = 's', returns = '*v')
    def get_fit_parameters(self, c, name):
        '''returns the parameters for the latest fit, name can be linecenter or bfield'''
        if name == 'linecenter':
            fit = self.line_center_fit
        elif name =='bfield':
            fit = self.B_fit
        else:
            raise Exception("Provided name not found")
        if fit is not None:
            return fit
        else:
            raise Exception("Fit has not been calculated")
    
    @setting(5, "Get Current Lines", time_offset = 'v', returns = '*(sv[MHz])')
    def get_current_lines(self, c, time_offset = 0.0):
        '''get the frequency of the current line specified by name. if name is not provided, get all lines'''
        lines = []
        current_time = time.time() - self.start_time
        ## add additional offset to predict frequency in the future
        current_time = current_time + time_offset
        try:
            B = self.fitter.evaluate(current_time, self.B_fit)
            center = self.fitter.evaluate(current_time, self.line_center_fit)
        except TypeError:
            raise Exception ("Fit is not available")
        B = WithUnit(B, 'gauss')
        center = WithUnit(center, 'MHz')
        result = self.tr.get_transition_energies(B, center)
        for name,freq in result:
            lines.append((name, freq))
        return lines
    
    @setting(6, "Get Current Line", name = 's', time_offset = 'v', returns = 'v[MHz]')
    def get_current_line(self, c, name, time_offset = 0.0):
        lines = yield self.get_current_lines(c, time_offset)
        d = dict(lines)
        try:
            returnValue(d[name])
        except KeyError:
            raise Exception ("Requested line not found")
    
    @setting(7, "Get Current B", time_offset = 'v', returns = 'v[gauss]')
    def get_current_b(self, c, time_offset = 0.0):
        current_time = time.time() - self.start_time
        current_time = current_time + time_offset
        B = self.fitter.evaluate(current_time, self.B_fit)
        B = WithUnit(B, 'gauss')
        return B
        #returnValue(B)
        
    @setting(13, "Get Current Center", time_offset = 'v', returns = 'v[MHz]')
    def get_current_center(self, c, time_offset = 0.0):
        current_time = time.time() - self.start_time
        current_time = current_time + time_offset
        center = self.fitter.evaluate(current_time, self.line_center_fit)
        center = WithUnit(center, 'MHz')
        return center
        #returnValue(center)
    
    @setting(10, 'Remove B Measurement', point = 'i')
    def remove_B_measurement(self, c, point):
        '''removes the point w, can also be negative to count from the end'''
        try:
            self.t_measure_B = numpy.delete(self.t_measure_B, point)
            self.B_field = numpy.delete(self.B_field, point)
        except ValueError or IndexError:
            raise Exception("Point not found")
        self.do_fit()

    @setting(11, 'Remove Line Center Measurement', point = 'i')
    def remove_line_center_measurement(self, c, point):
        '''removes the point w, can also be negative to count from the end'''
        try:
            self.t_measure_line_center = numpy.delete(self.t_measure_line_center, point)
            self.line_center = numpy.delete(self.line_center, point)
        except ValueError or IndexError:
            raise Exception("Point not found")
        self.do_fit()

    @setting(8, 'Get Fit History', returns = '(*(v[s]v[gauss]) *(v[s]v[MHz]))')
    def get_fit_history(self, c):
        history_B = []
        history_line_center = []
        for t,b_field in zip(self.t_measure_B, self.B_field):
            history_B.append((WithUnit(t,'s'),WithUnit(b_field,'gauss')))
        for t, freq in zip(self.t_measure_line_center, self.line_center):
            history_line_center.append((WithUnit(t,'s'), WithUnit(freq, 'MHz')))
        return [history_B, history_line_center]
    
    @setting(9, 'History Duration', duration = '*v[s]', returns = '*v[s]')
    def get_history_duration(self, c, duration = None):
        if duration is not None:
            self.keep_B_measurements = duration[0]['s']
            self.keep_line_center_measurements = duration[1]['s']
        return [ WithUnit(self.keep_B_measurements,'s'), WithUnit(self.keep_line_center_measurements, 's') ]
    
    def do_fit(self):
        self.remove_old_measurements()
        if (len(self.t_measure_B) and len(self.t_measure_line_center)):
            self.B_fit = self.fitter.fit(self.t_measure_B, self.B_field)
            self.line_center_fit = self.fitter.fit(self.t_measure_line_center, self.line_center)
        self.onNewFit(None)
    
    def remove_old_measurements(self):
        current_time = time.time() - self.start_time
        
        keep_line_center = numpy.where( (current_time - self.t_measure_line_center) < self.keep_line_center_measurements)
        keep_B = numpy.where( (current_time - self.t_measure_B) < self.keep_B_measurements)

        self.t_measure_line_center = self.t_measure_line_center[keep_line_center]
        self.t_measure_B = self.t_measure_B[keep_B]
        self.B_field = self.B_field[keep_B]
        self.line_center = self.line_center[keep_line_center]

if __name__ == '__main__':
    from labrad import util
    util.runServer(LineTracker())
