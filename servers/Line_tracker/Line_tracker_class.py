import time
from Line_tracker_config import config as conf
from Line_calculator import Transitions_Hg, fitter
import numpy
from labrad.units import WithUnit
from twisted.internet.defer import returnValue, inlineCallbacks

class Line(object):
    '''
    Class that do the line tracking for one line.
    Method list:
    - add measurement
    - get fit
    '''
    def __init__(self, start_time, tracker_id = 0):
        self.tracker_id = tracker_id # for identification of the Line object in case of multiple tracker being used
        self.start_time = start_time
        self.keep_line_measurements = conf.keep_line_measurements
        self.tr = Transitions_Hg()
        self.fitter = fitter()
        self.t_measure = numpy.array([]) # Array to keep all the time used for fitting
        self.line_center = numpy.array([]) # Array to keep all the line_center used for fitting
        self.all_line_array = numpy.array([])
        self.all_time_array = numpy.array([])
        self.line_fit = None # fit object
        
    
    #@inlineCallbacks    
    def set_measurement(self, freq, time_offset = 0.0): ## frequency is labrad unit object
        '''takes frequency measurement of the line and performs tracking'''
        t_measure = time.time() - self.start_time
        ### add a possibility of having offset from the measurement
        t_measure = t_measure + time_offset
        ## add to the actively being fit data array
        self.t_measure = numpy.append(self.t_measure , t_measure)
        self.line_center = numpy.append(self.line_center , freq['kHz'])
        ## add to the overall data array
        
        self.all_line_array = numpy.append(self.line_center , freq['kHz'])
        self.all_time_array = numpy.append(self.t_measure, t_measure)
        
        #try to save to data vault
        #yield self.save_result_datavault(t_measure, freq['kHz'])
        self.do_fit()
        
    def get_current_line(self, time_offset = 0.0):
        '''get the frequency of the current line now. Have an option to put in a time offset'''
        current_time = time.time() - self.start_time
        ## add additional offset to predict frequency in the future
        current_time = current_time + time_offset
        try:
            freq = self.fitter.evaluate(current_time, self.line_fit)
        except TypeError:
            raise Exception ("Fit is not available")
        freq = WithUnit(freq, 'kHz')
        return freq
    
    def get_fit_history(self):
        '''
        return all the lines which are currently active in the fit
        '''
        history_line = []
        for t, freq in zip(self.t_measure, self.line_center):
            history_line.append((WithUnit(t,'s'), WithUnit(freq, 'kHz')))
        return history_line
        
    def do_fit(self):
        '''
        perform fitting
        '''
        self.remove_old_measurements()
        if (len(self.t_measure)):
            self.line_fit = self.fitter.fit(self.t_measure, self.line_center)
            
    def remove_line_measurement(self, point):
        '''removes the point w, can also be negative to count from the end'''
        try:
            self.t_measure = numpy.delete(self.t_measure, point)
            self.line_center = numpy.delete(self.line_center, point)
        except ValueError or IndexError:
            raise Exception("Point not found")
        self.do_fit()
            
    def remove_old_measurements(self):
        '''
        remove measurement points older than a specified time
        '''
        current_time = time.time() - self.start_time
        keep_line_center = numpy.where( (current_time - self.t_measure) < self.keep_line_measurements)
        self.t_measure = self.t_measure[keep_line_center]
        self.line_center = self.line_center[keep_line_center]
