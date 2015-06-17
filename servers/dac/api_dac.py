#!/usr/bin/env python
"""
This is an interpretation of the example program
C:\Program Files\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Analog Out\Generate Voltage\Cont Gen Volt Wfm-Int Clk\ContGen-IntClk.c
This routine will play an arbitrary-length waveform file.
This module depends on:
numpy
Adapted by Martin Bures [ mbures { @ } zoll { . } com ]
"""
# import system libraries
import ctypes
import numpy as np
import threading
import sys
import time

from twisted.internet.defer import inlineCallbacks, returnValue, DeferredLock
from twisted.internet.threads import deferToThread
# load any DLLs
nidaq = ctypes.windll.nicaiu # load the DLL
##############################
# Setup some typedefs and constants
# to correspond with values in
# C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h
# the typedefs
int32 = ctypes.c_long
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
float64 = ctypes.c_double
TaskHandle = uInt32
## add boolean
uBool = ctypes.c_bool
# the constants
DAQmx_Val_Cfg_Default = int32(-1)
DAQmx_Val_Volts = 10348
DAQmx_Val_Rising = 10280
DAQmx_Val_FiniteSamps = 10178
DAQmx_Val_ContSamps = 10123
DAQmx_Val_GroupByChannel = 0
##############################

class WaveformThread( threading.Thread ):
    """
    This class performs the necessary initialization of the DAQ hardware and
    spawns a thread to handle playback of the signal.
    It takes as input arguments the waveform to play and the sample rate at which
    to play it.
    This will play an arbitrary-length waveform file.
    """
    def __init__( self, waveform, triggering = False):
        
        self.running = True
        self.taskHandle = TaskHandle( 0 )
        
        self.data = waveform
        ## calculate the number of channels
        self.channel = self.data.shape[0]-1
        ## extract time array
        self.time_array = self.data[0]
        self.number_of_sample = np.size(self.time_array)
        #print self.number_of_sample
        self.duration = self.time_array[-1]
        self.sampling_rate = (self.number_of_sample-1)/self.duration
        
        self.trigger = triggering ## see if this waveform needed to wait for trigger or not 
        
        #print self.duration
        #print self.sampling_rate
        #print self.channel
        #print self.number_of_sample ##per channel
        
        ## generate channel name
        if self.channel == 1:
            self.channel_name = "PXI1Slot6/ao0"
        else:
            self.channel_name = "PXI1Slot6/ao0" + ":" + str(self.channel-1)
            
        #print self.channel_name
        
        ### parse data array into a single dimensional array
        
        self.data_1d = self.data[1]
        for i in range(self.channel-1):
            self.data_1d = np.concatenate((self.data_1d,self.data[i+2])) 
        #print self.data_1d
        
        ## initialize channel instance
        self.CHK(nidaq.DAQmxCreateTask("",ctypes.byref( self.taskHandle )))
        self.CHK(nidaq.DAQmxCreateAOVoltageChan( self.taskHandle,
                                   self.channel_name, #change to the correct channel name. Check with MAX software
                                   "", #name assignment
                                   float64(-10.0), #min value
                                   float64(10.0), #max value 
                                   DAQmx_Val_Volts, #unit
                                   None))
        ## initialize timing/sampling of this particular waveform
        self.CHK(nidaq.DAQmxCfgSampClkTiming( self.taskHandle,
                                "", #source. Null means on-board clock
                                float64(self.sampling_rate), #sampling rate
                                DAQmx_Val_Rising,
                                DAQmx_Val_FiniteSamps, #sample mode:DAQmx_Val_ContSamps, DAQmx_Val_FiniteSamps
                                uInt64(self.number_of_sample))); #number of sample to generate per channel
        #triggering test 
        #self.CHK(nidaq.DAQmxCfgDigEdgeStartTrig(self.taskHandle, "PFI0", DAQmx_Val_Rising)) ##somehow having
        #PXI1Slot6/PFI0 doesn't work. Only PFI0 works. Probably the device is
        #already known, so we don't have to re-specify the device in the terminal name.
        
        if self.trigger:
            self.CHK(nidaq.DAQmxCfgDigEdgeStartTrig(self.taskHandle, "PFI0", DAQmx_Val_Rising))
        
                                
        #test retriggerable
        #doesn't work
        #self.CHK(nidaq.DAQmxResetStartTrigRetriggerable(self.taskHandle))
        
        self.CHK(nidaq.DAQmxWriteAnalogF64( self.taskHandle,
                              int32(self.number_of_sample), #number of sample per channel
                              0,
                              float64(-1), #time out -1 is infinite
                              DAQmx_Val_GroupByChannel, #how to arrange the data for channels
                              self.data_1d.ctypes.data, #data
                              None,
                              None))
        threading.Thread.__init__( self )
    def CHK( self, err ):
        """a simple error checking routine"""
        if err < 0:
            buf_size = 200
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))
        if err > 0:
            buf_size = 200
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq generated warning %d: %s'%(err,repr(buf.value)))
    def run( self ):
        self.CHK(nidaq.DAQmxStartTask( self.taskHandle ))
        #self.CHK(nidaq.DAQmxWaitUntilTaskDone( self.taskHandle,float64(10)))
    
    def wait(self):
        self.CHK(nidaq.DAQmxWaitUntilTaskDone( self.taskHandle,float64(20)))
    
    def stop( self ):
        self.running = False
        nidaq.DAQmxStopTask( self.taskHandle )
        nidaq.DAQmxClearTask( self.taskHandle )

class api_dac():
    def __init__(self):
        pass
        
    def setVoltage(self, voltage_array, trigger):
        '''
        Set the voltage pattern according to the input voltage array. We use this to do a quick write for the 
        static voltage value.
        '''
        #print "set Voltage"
        #data1 = np.load('test_ao_sequence1.npy')
        data1 = voltage_array
        mythread = WaveformThread(data1, trigger)
        mythread.run()
        mythread.wait()
        mythread.stop()
        
#     def setVoltagePattern(self, time_vertex_array, v_vertex_array, trigger, sampling_rate):
#         t = time_vertex_array
#         v = v_vertex_array
#         duration = t[-1] ## get the last value of the time array. This is the duration of the pulse sequence.
#         sample_size = sampling_rate*duration
#         ## make sample size an even number
#         sample_size = (sample_size//2)*2
#         time_array = np.linspace(0,duration, sample_size)
#         volt_array = np.ones_like(time_array)
#         volt_array[0] = v[0] #initialize first point
#         
#         for i in range(t.size-1):
#             #i = 0
#             #print i
#             time_location = np.where((time_array>t[i])*(time_array<=t[i+1])) ### look for the location of the time span we are interested in
#             slope = (v[i+1]-v[i])/(t[i+1]-t[i]) ### calculate the voltage slope in this region
#             #print "v is ", v[i]
#             #print "slope is ", slope
#             volt_array[time_location] = v[i]+slope*(time_array[time_location]-t[i]) ## compute the voltage value
#             
#         data = time_array
#         channel_0 = volt_array
#         data = np.vstack((data,channel_0))
#         
#         ## write to NI analog ##
#         mythread = WaveformThread(data, True)
#         mythread.run()
#         print "waiting for the sequence to be done"
#         mythread.wait()
#         print "done waiting"
#         mythread.stop()


    def setVoltagePattern(self, vertex_array, trigger, sampling_rate):
        '''
        Set the voltage pattern according to the input vertex_array. Also the trigger indicated if the pattern will wait for
        the trigger or just go when ready. The sampling_rate is the resolution in time for the voltage pattern.
        '''
        t = vertex_array[0]                 ## first row of the vertex array is the time array
        channel = vertex_array.shape[0]-1   ## the rest is the channel information
        duration = t[-1]                    ## get the last value of the time array. This is the duration of the pulse sequence.
        sample_size = sampling_rate*duration
                                            ## make sample size an even number. This is required by the hardware
        sample_size = (sample_size//2)*2
        time_array = np.linspace(0,duration, sample_size) ## create time array
        
        volt_array = np.ones((channel,np.size(time_array))) ## create voltage array which in the end will get sent to the NI card
        volt_array[:,0] = vertex_array[:,0][1:]             # initialize first points
        #print volt_array[:,0]
        
        ### create time array for low pass convolution
        
        band = 0.0003
        time_filter = np.arange(-3*band,3*band,1/sampling_rate) ##plus-minus time
        conv = np.exp(-0.5*time_filter**2/band**2) ## gaussian
        #conv = np.delete(conv,np.where(conv<0.10))
        conv = conv/np.sum(conv) ## normalization
        ###
        
        for j in range(channel):               # loop through all the channels
            v = vertex_array[j+1]              # v extract the voltage information for the current channel
            for i in range(t.size-1):          # loop through the vertex
                time_location = np.where((time_array>t[i])*(time_array<=t[i+1]))### look for the location of the time span we are interested in
                slope = (v[i+1]-v[i])/(t[i+1]-t[i])  # calculate the voltage slope in this region
                volt_array[j][time_location] = v[i]+slope*(time_array[time_location]-t[i])  # simply a linear equation to calculate the voltage at each time stamp
            if j == 0:
                volt_array[j] = np.convolve(volt_array[j], conv, 'same') ### perform low-pass by convolution
            #print volt_array[j]
        
        data = np.vstack((time_array,volt_array)) # stack the time array and voltage array together
        mythread = WaveformThread(data, trigger)  #
        return mythread
    
#         print "run waveform"
#         mythread.run()
#         print "waiting for the sequence to be done"
#         mythread.wait()
#         print "done waiting"
#         mythread.stop()
        
        
        
        
