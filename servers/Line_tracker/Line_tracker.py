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
from Line_tracker_config import config as conf
from Line_tracker_class import Line
import time
import numpy


class LineTracker(LabradServer):
    """Provides ability to track drifts of the multiple lines"""
    name = 'Line Tracker'
    
    onNewFit = Signal( 768121, 'signal: new fit', '' )
    
    @inlineCallbacks
    def initServer(self):
        self.start_time = time.time() ## start time upon initialization of the server

        self.numbers_of_tracker = 0
        self.Line_tracker = [] ## array to keep track of all the line tracker object
        self.dv_save_context = [] ## array to keep track of all the save context

        yield self.setupListeners()
        
        default_channel_number = 4
        for i in range(default_channel_number):
            print i
            self.add_tracker(0)
        

    
    @inlineCallbacks
    def setup_dv_dataset(self, number_of_tracker):
        '''
        create a new session in DV for each tracker initiated.
        '''
        try:
            context_ID = number_of_tracker
            
            self.dv = yield self.client.data_vault
            directory = list(conf.save_folder)
            localtime = time.localtime(self.start_time)
            dirappend = [time.strftime("%Y%b%d",localtime), time.strftime("%H%M_%S", localtime)]
            directory.extend(dirappend)
            yield self.dv.cd(directory, True, context = (0, context_ID))
            
            dataset_name = str(number_of_tracker)
            print "data set number is ", context_ID
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
    
        
    @setting(2, 'Set Measurement', freq = 'v[kHz]', tracker_number = 'i', time_offset = 'v', returns = '') ## input tracker number start from 1
    def set_measurement(self, c, freq, tracker_number = 1, time_offset = 0.0):
        '''set_measurement to the corresponding tracker. tracker_number by default is 1 and we start counting from 1 for this.'''
        #print freq
        tracker_id = tracker_number - 1
        try:
            tracker = self.Line_tracker[tracker_id] # access the correct tracker
            tracker.set_measurement(freq) # set freq
            t_measure = time.time() - self.start_time
            t_measure = t_measure + time_offset
        
            self.save_result_datavault(t_measure, freq, tracker_number)
            ## fit
            tracker.do_fit()
            self.onNewFit(None)
        except IndexError:
            raise Exception("Tracker out of range.")
        
        

        
    @inlineCallbacks
    def save_result_datavault(self, t_measure, freq, tracker_number):
        try:
            print "track number is ", tracker_number
            yield self.dv.add([t_measure, freq['kHz']] , context = (0, tracker_number))
        except AttributeError:
            print 'Data Vault Not Available, not saving'
            yield None
            
    @setting(3, "Get Fit Parameters", tracker_number = 'i', returns = '*v')
    def get_fit_parameters(self, c, tracker_number = 1):
        '''returns the parameters for the latest fit for a given tracker'''
        tracker_id = tracker_number - 1
        try:
            tracker = self.Line_tracker[tracker_id] # access the correct tracker
            fit = tracker.line_fit
        except IndexError:
            raise Exception("Tracker out of range.")
        
        
        if fit is not None:
            return fit
        else:
            raise Exception("Fit has not been calculated")                

    
    @setting(4, "Get Current Line", tracker_number = 'i', time_offset = 'v', returns = 'v[kHz]')
    def get_current_line(self, c, tracker_number = 1, time_offset = 0.0):
        '''get the current line prediction for a given tracker number'''
        
        tracker_id = tracker_number - 1
        try:
            tracker = self.Line_tracker[tracker_id] # access the correct tracker
        except IndexError:
            raise Exception("Tracker out of range.")
        
        current_time = time.time() - self.start_time
        ## add additional offset to predict frequency in the future
        current_time = current_time + time_offset
        
        try:
            freq = tracker.fitter.evaluate(current_time, tracker.line_fit)
        except TypeError:
            raise Exception ("Fit is not available")
        freq = WithUnit(freq, 'kHz')
        return freq

    @setting(5, 'Remove Measurement', tracker_number = 'i', point = 'i')
    def remove_measurement(self, c, tracker_number = 1, point = 0):
        '''removes the point w, can also be negative to count from the end'''
        tracker_id = tracker_number - 1
        try:
            tracker = self.Line_tracker[tracker_id] # access the correct tracker
        except IndexError:
            raise Exception("Tracker out of range.")
        
        try:
            tracker.t_measure = numpy.delete(tracker.t_measure, point)
            tracker.line_center = numpy.delete(tracker.line_center, point)
            tracker.do_fit()
            self.onNewFit(None)
        except ValueError or IndexError:
            raise Exception("Point not found")


    @setting(6, 'Get Fit History', tracker_number = 'i', returns = '*(v[s]v[kHz])')
    def get_fit_history(self, c, tracker_number = 1):
        '''
        Return all points participating in the fit
        '''
        tracker_id = tracker_number - 1
        try:
            tracker = self.Line_tracker[tracker_id] # access the correct tracker
        except IndexError:
            raise Exception("Tracker out of range.")
        
        return tracker.get_fit_history()
    
        
    @setting(7, 'History Duration', tracker_number = 'i', duration = 'v[s]', returns = 'v[s]')
    def history_duration(self, c, tracker_number = 1, duration = None):
        '''
        Set the duration in the history for points participate in the fit
        '''
        tracker_id = tracker_number - 1
        try:
            tracker = self.Line_tracker[tracker_id] # access the correct tracker
        except IndexError:
            raise Exception("Tracker out of range.")
        
        if duration is not None:
            tracker.keep_line_measurements = duration['s']
            tracker.remove_old_measurements()
        return WithUnit(tracker.keep_line_measurements,'s')
    
    @setting(8, 'Get All History', tracker_number = 'i', returns = '*(v[s]v[kHz])')
    def get_all_history(self, c, tracker_number = 1):
        '''
        Return all points participating in the fit
        '''
        tracker_id = tracker_number - 1
        try:
            tracker = self.Line_tracker[tracker_id] # access the correct tracker
        except IndexError:
            raise Exception("Tracker out of range.")
        
        return tracker.get_all_history()
    
    @setting(9, 'Get Tracker Number', returns = 'i')
    def get_tracker_number(self, c):
        '''
        Return the number of tracker initialized
        '''
        return self.numbers_of_tracker

if __name__ == '__main__':
    from labrad import util
    util.runServer(LineTracker())
