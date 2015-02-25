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

class NI_Analog_Server(LabradServer):
    name = "NI Analog Server" ## this has to match the instance name
    
    def initServer(self):
        print "hello"
        i = self.initAnalogChannel()
        print i
    
    def initAnalogChannel(self):
        print "initialize analog channel"
        return "return"
        
    
    @setting(1, data='?', returns='b')
    def is_true(self,c,data):
        return bool(data)
    
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

if __name__ == '__main__':
    from labrad import util
    util.runServer(NI_Analog_Server())