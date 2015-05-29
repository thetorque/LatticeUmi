"""
### BEGIN NODE INFO
[info]
name = NI Analog Server
version = 0.1
description = 
instancename = NI Analog Server

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""

from labrad.server import LabradServer, setting, Signal
from labrad.units import WithUnit
from twisted.internet.defer import inlineCallbacks, returnValue, DeferredLock
from twisted.internet.threads import deferToThread
from api_dac import api_dac
import numpy as np

class dac_channel(object):
    def __init__(self, name, channel_number,voltage = None):
        '''min voltage is used to calibrate the offset of the channel'''
        self.name = name
        self.channel_number = channel_number
        self.voltage = voltage
    
    def is_in_range(self, voltage):
        return (self.min_voltage  <= voltage <= self.max_voltage)
    
    def get_range(self):
        return (self.min_voltage, self.max_voltage)

class NI_Analog_Server(LabradServer):
    name = "NI Analog Server" ## this has to match the instance name
    onNewVoltage = Signal(123556, 'signal: new voltage', '(sv)')
    
    @inlineCallbacks
    def initServer(self):
        '''
        Initialize the server
        '''
        print "NI Analog says hello to you."
        self.api_dac  = api_dac()    # import api for DAC
        self.inCommunication = DeferredLock()   # twisted function
        self.d = yield self.initAnalogChannel() 
        self.chan_number = len(self.d) # channel number is how many elements in self.d
        self.listeners = set() 
        
        ##
        #vertex_array = ([[0,1,2],[0,1,0], [-1,-2,-1]])
        #self.setVoltagePattern(-1, vertex_array, False, 1000)
        
        
    @inlineCallbacks
    def initAnalogChannel(self):
        '''creates dictionary for information storage''' 
        d = {}
        for name,channel_number in [        # make a dictionary of the channel name and ID. Should be somewhere less obscure.
                             ('B_x', 0),
                             ('B_y', 1),
                             ('B_z', 2),
                             ('MOT', 3),
                             ('lattice',4),
                             ('clock',5),
                             ]: 
            chan = dac_channel(name, channel_number)
            chan.voltage = yield self.getRegValue(name)   # get value of each channel from the registry
            d[name] = chan
            
        voltage_array = self.genStaticVoltageArray(d)     # generate initial value according to the values in the registry
        yield self.do_set_voltage(voltage_array, trigger = False)
        returnValue( d )
        
    def genStaticVoltageArray(self,d):
        
        '''this method generate an array of time and voltage to be written to the NI card with the
        input of dictionay of voltage channel
        '''
        
        time_array = np.linspace(0, 0.001, 2)   # kind of arbitrary time array. We want to write to the current static voltage so should be relativel fast
        voltage_array = np.zeros(shape=(len(d)+1,2))  # initialize voltage array according to the number of channels
        voltage_array[0]= time_array
        for key, chan in d.iteritems():
            voltage = chan.voltage
            channel = chan.channel_number
            voltage_array[channel+1] = voltage*np.ones_like(time_array)
        return voltage_array
        
            
    @inlineCallbacks
    def getRegValue(self, name):
        '''
        Get the values of the voltage from the registry
        '''
        yield self.client.registry.cd(['','Servers', 'DAC'], True)
        try:
            voltage = yield self.client.registry.get(name)
        except Exception:
            print '{} not found in registry'.format(name)
            voltage = 0
        returnValue(voltage)
        
    @setting(0, "Set Voltage",channel = 's', voltage = 'v[V]', returns = '')
    def setVoltage(self, c, channel, voltage):
        '''
        Set voltage for a given channel name
        '''
        try:
            ### check of the name of channel is correct or not
            chan = self.d[channel]
            #channel_number = chan.channel_number
        except KeyError:
            raise Exception ("Channel {} not found".format(channel))
        
        self.d[channel].voltage = voltage['V'] ## cast from voltage unit to normal float
        voltage_array = self.genStaticVoltageArray(self.d)
        yield self.do_set_voltage(voltage_array, False)
        self.notifyOtherListeners(c, (channel, voltage), self.onNewVoltage)  ## tell other listeners that the voltage is updated
        
    @setting(1, "Get Voltage", channel = 's', returns = 'v[V]')
    def getVoltage(self, c, channel):
        '''
        Get the voltage value for the given channel.
        '''
        try:
            voltage = self.d[channel].voltage
        except KeyError:
            raise Exception ("Channel {} not found".format(channel))
        return WithUnit(voltage, 'V')
        
    @inlineCallbacks
    def do_set_voltage(self, voltage_array, trigger):
        '''
        This method takes the input voltage array and program the NI analog card via the api calling
        '''
        yield self.inCommunication.acquire()
        try:
            yield deferToThread(self.api_dac.setVoltage, voltage_array, trigger)
        except Exception as e:
            raise e
        finally:
            self.inCommunication.release()
            
    @setting(2, "Set Voltage Pattern", vertex_array = '*2v', trigger = 'b', sampling = 'v', returns = '')
    def setVoltagePattern(self, c, vertex_array, trigger, sampling):
        '''
        Generate the voltage pattern given the vertex of the time (first row) and voltages (subsequent rows). Trigger
        indiciate if the voltage pattern will wait for a trigger or not. Sampling is the sample rate of this voltage pattern.
        '''
        #print "array is", vertex_array
        vertex_array = np.asarray(vertex_array)
        yield self.do_set_voltagePattern(vertex_array, trigger, sampling)
        #self.notifyOtherListeners(c, (channel, voltage), self.onNewVoltage)
            
    @inlineCallbacks
    def do_set_voltagePattern(self, vertex_array, trigger, sampling):
        '''
        This method takes the input voltage array and program the NI analog card via the api calling
        '''
        yield self.inCommunication.acquire()
        try:
            yield deferToThread(self.api_dac.setVoltagePattern, vertex_array, trigger,sampling)
        except Exception as e:
            raise e
        finally:
            self.inCommunication.release()
    
    def notifyOtherListeners(self, context, message, f):
        """
        Notifies all listeners except the one in the given context, executing function f
        """
        notified = self.listeners.copy()
        notified.remove(context.ID)
        f(message,notified)
    
    def initContext(self, c):
        """Initialize a new context object."""
        self.listeners.add(c.ID)
    
    def expireContext(self, c):
        self.listeners.remove(c.ID)
        
    @inlineCallbacks
    def stopServer(self):
        '''save the latest voltage information into registry'''
        try:
            yield self.client.registry.cd(['','Servers', 'DAC'], True)
            for name,channel in self.d.iteritems():
                yield self.client.registry.set(name, channel.voltage)
        except AttributeError:
            #if dictionary doesn't exist yet (i.e bad identification error), do nothing
            pass

if __name__ == '__main__':
    from labrad import util
    util.runServer(NI_Analog_Server())