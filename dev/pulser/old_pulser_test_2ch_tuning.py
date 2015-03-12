import os
import time
import ok
import numpy as np

def padTo16(data):
    size_needed = (16 - len(data)%16)%16
    zero_padding = bytearray(size_needed)
    return data+zero_padding


def freqToByteArray(freq):
    f_ref = 2000000000.0
    #input freq in Hz
    print "f = ", freq
    f_int = int(freq*(2**32)*(2**32)/f_ref)
    #print "freq is =",f_int
    b = bytearray(8)
    for i in range(8):
        b[i]=(f_int//(2**(i*8)))%256
        #print i, "=", (f_int//(2**(i*8)))%256
    return b

def ampToByteArray(amp):
    ## 0 to 65535 (actually only 14 bits)
    b = bytearray(2)
    b[0] = amp%256
    b[1] = (amp//256)%256
    data = bytearray.fromhex(u'0000') + b + bytearray.fromhex(u'0000 0000') ### zeros stuff are unused for now
    return data 

def DDSdata(amp,freq):
    c = ampToByteArray(amp) + freqToByteArray(freq)
    return c

xem = ok.FrontPanel()
xem.OpenBySerial('')
#xem.ConfigureFPGA('C:\Users\Thaned\Dropbox\Hardware\RIKEN_Hardware\Pulser_Altera\output_files\Pulser.rbf')
#xem.ConfigureFPGA('C:\Users\Thaned\Dropbox\Hardware\RIKEN_Hardware\Pulser_w_line_triggering_2015_03_10\photon\photon.bit')
delay = 0.1
 
padding = bytearray.fromhex(u'0000') 



##set channel 0
xem.SetWireInValue(0x04,0x00,0xFF)
xem.UpdateWireIns()
xem.ActivateTriggerIn(0x40,4)

data = padding + DDSdata(0,88888888.888)

data = padTo16(data)
xem.WriteToBlockPipeIn(0x81,16,data)
# 
#set channel 1
xem.SetWireInValue(0x04,0x01,0xFF)
xem.UpdateWireIns()
xem.ActivateTriggerIn(0x40,4)
data = padding + DDSdata(0,80000000)
data = padTo16(data)
xem.WriteToBlockPipeIn(0x81,16,data)

# for i in range(10000):
#     time.sleep(0.05)
#     print i
#     xem.ActivateTriggerIn(0x40,4)
#     #data = padding + DDSdata(40000,80000000+1000000*np.sin(2*np.pi*i/20)+np.random.random(1)[0]*1000000)
#     data = padding + DDSdata(40000,80000000)
#     data = padTo16(data)
#     xem.SetWireInValue(0x04,0x01,0xFF)
#     xem.UpdateWireIns()
#     xem.WriteToBlockPipeIn(0x81,16,data)
# 
#     xem.ActivateTriggerIn(0x40,4)
#     data = padding + DDSdata(40000,80000000)
#     data = padTo16(data)
#     xem.SetWireInValue(0x04,0x00,0xFF)
#     xem.UpdateWireIns()
#     xem.WriteToBlockPipeIn(0x81,16,data)
