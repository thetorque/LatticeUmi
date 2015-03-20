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
        print "hello"
        self.api_dac  = api_dac()
        self.inCommunication = DeferredLock()
        self.d = yield self.initAnalogChannel()
        self.chan_number = len(self.d)
        self.listeners = set() 
        
        
    @inlineCallbacks
    def initAnalogChannel(self):
        '''creates dictionary for information storage''' 
        d = {}
        for name,channel_number in [
                             ('comp1', 0),
                             ('comp2', 1),
                             ('endcap1', 2),
                             ('endcap2', 3),
                             ]:
            chan = dac_channel(name, channel_number)
            chan.voltage = yield self.getRegValue(name)
            d[name] = chan
            
        voltage_array = self.genStaticVoltageArray(d)
        yield self.do_set_voltage(voltage_array, trigger = False)
        returnValue( d )
        
    def genStaticVoltageArray(self,d):
        
        '''this method generate an array of time and voltage to be written to the NI card with the
        input of dictionay of voltage channel
        '''
        
        time_array = np.linspace(0, 0.001, 2)
        voltage_array = np.zeros(shape=(len(d)+1,2))
        voltage_array[0]= time_array
        for key, chan in d.iteritems():
            voltage = chan.voltage
            channel = chan.channel_number
            voltage_array[channel+1] = voltage*np.ones_like(time_array)
        return voltage_array
        
            
    @inlineCallbacks
    def getRegValue(self, name):
        yield self.client.registry.cd(['','Servers', 'DAC'], True)
        try:
            voltage = yield self.client.registry.get(name)
        except Exception:
            print '{} not found in registry'.format(name)
            voltage = 0
        returnValue(voltage)
        
    @setting(0, "Set Voltage",channel = 's', voltage = 'v[V]', returns = '')
    def setVoltage(self, c, channel, voltage):
        try:
            ### check of the name of channel is correct or not
            chan = self.d[channel]
            channel_number = chan.channel_number
        except KeyError:
            raise Exception ("Channel {} not found".format(channel))
        
        self.d[channel].voltage = voltage['V'] ## cast from voltage unit to normal float
        voltage_array = self.genStaticVoltageArray(self.d)
        yield self.do_set_voltage(voltage_array, False)
        self.notifyOtherListeners(c, (channel, voltage), self.onNewVoltage)
        
    @setting(1, "Get Voltage", channel = 's', returns = 'v[V]')
    def getVoltage(self, c, channel):
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