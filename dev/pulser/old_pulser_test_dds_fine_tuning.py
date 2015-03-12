import os
import time
import ok

def padTo16(data):
    size_needed = (16 - len(data)%16)%16
    zero_padding = bytearray(size_needed)
    return data+zero_padding


def freqToByteArray(freq):
    f_ref = 2000000000.0
    #input freq in Hz
    f_int = int(freq*(2**32)*(2**32)/f_ref)
    print "freq is =",f_int
    b = bytearray(8)
    for i in range(8):
        b[i]=(f_int//(2**(i*8)))%256
        print i, "=", (f_int//(2**(i*8)))%256
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
xem.ConfigureFPGA('C:\Users\Thaned\Dropbox\Hardware\RIKEN_Hardware\Pulser_w_line_triggering_2015_03_10\photon\photon.bit')
delay = 0.1
 
padding = bytearray.fromhex(u'0000') 
# # #amp_0 = bytearray.fromhex(u'0000 00b0 0000 0000') ## []frequency[7 to 0][15 to 8][23 to 16][31 to 24] ## this goes to lower chuck
# # amp_0 = ampToByteArray(50000)
# # #setting_1 = bytearray.fromhex(u'0000 0000 0000 0008') ## lower:frequency[7 to 0][15 to 8][23 to 16][31 to 24] higher:[7 to 0][15 to 8][23 to 16][31 to 24]
# # freq_0 = freqToByteArray(80000000.1)
# # amp_1 = bytearray.fromhex(u'0000 00b0 0000 0000')
# # freq_1 = freqToByteArray(80000000.2)
# data = padding + DDSdata(40000,80000000) + DDSdata(40000,80000001)
# data = padTo16(data)
#  
# xem.ActivateTriggerIn(0x40,4)
#  
# xem.SetWireInValue(0x04,0x00,0xFF)
# xem.UpdateWireIns()
#  
# xem.WriteToBlockPipeIn(0x81,16,data)

for i in range(1000):
    time.sleep(2)
    print i
    xem.ActivateTriggerIn(0x40,4)
    data = padding + DDSdata(40000,80000000+i/10000.0)
    data = padTo16(data)
    xem.WriteToBlockPipeIn(0x81,16,data)