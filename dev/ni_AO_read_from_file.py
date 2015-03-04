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
    def __init__( self, waveform):
        self.running = True
        self.taskHandle = TaskHandle( 0 )

        self.data = waveform
        ## calculate the number of channels
        self.channel = self.data.shape[0]-1
        ## extract time array
        self.time_array = self.data[0]
        self.number_of_sample = np.size(self.time_array)
        self.duration = self.time_array[-1]
        self.sampling_rate = (self.number_of_sample-1)/self.duration
        
        print self.duration
        print self.sampling_rate
        print self.channel
        print self.number_of_sample ##per channel
        
        ## generate channel name
        if self.channel == 1:
            self.channel_name = "PXI1Slot6/ao0"
        else:
            self.channel_name = "PXI1Slot6/ao0" + ":" + str(self.channel-1)
            
        print self.channel_name
        
        ### parse data array into single array
        
        self.data_1d = self.data[1]
        self.data_1d = np.concatenate((self.data_1d,self.data[2])) 
        print self.data_1d
        
        #sys.exit()

        self.CHK(nidaq.DAQmxCreateTask("",ctypes.byref( self.taskHandle )))
        self.CHK(nidaq.DAQmxCreateAOVoltageChan( self.taskHandle,
                                   self.channel_name, #change to the correct channel name. Check with MAX software
                                   "", #name assignment
                                   float64(-10.0), #min value
                                   float64(10.0), #max value 
                                   DAQmx_Val_Volts, #unit
                                   None))
        
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
        counter = 0
        self.CHK(nidaq.DAQmxStartTask( self.taskHandle ))
        #self.CHK(nidaq.DAQmxWaitUntilTaskDone( self.taskHandle,float64(10)))
    
    ## create wait
    
    def wait(self):
        self.CHK(nidaq.DAQmxWaitUntilTaskDone( self.taskHandle,float64(20)))
    
    def stop( self ):
        self.running = False
        nidaq.DAQmxStopTask( self.taskHandle )
        nidaq.DAQmxClearTask( self.taskHandle )
if __name__ == '__main__':
    import time
    #data1 = np.load('test_ao_sequence1.npy')
    #data2 = np.load('test_ao_sequence2.npy')
    data1 = np.load('ramp.npy')
    mythread = WaveformThread(data1)
    mythread.run()
    mythread.wait()
    mythread.stop()
    
#     mythread = WaveformThread(data2)
#     mythread.run()
#     mythread.wait()
#     mythread.stop()
    
    print "program finished"