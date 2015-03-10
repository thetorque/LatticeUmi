import os
import time
import ok
import numpy as np

xem = ok.FrontPanel()
xem.OpenBySerial('')
xem.ConfigureFPGA('C:\Users\Thaned\Dropbox\Hardware\RIKEN_Hardware\Pulser_w_line_triggering_2012_12_19\photon\photon.bit')


def numToByteArray(number):
    #a,b = number//65536, number %65536
    b = bytearray(4)
    b[2] = number%256
    b[3] = (number//256)%256
    b[0] = (number//65536)%256
    b[1] = (number//16777216)%256
    print np.array([b[0],b[1],b[2],b[3]])
    return b

def padTo16(data):
    size_needed = (16 - len(data)%16)%16
    zero_padding = bytearray(size_needed)
    return data+zero_padding



# set wire in (FPGA reads data). First is the address, second is the value, last is the masking (1 for the bit you want to change)
##xem.SetWireInValue(0x00,0b10101000,0xF8)
# after this you have to update the wire in
##xem.UpdateWireIns()
#padding = bytearray.fromhex(u'0000') 
time_0 = numToByteArray(0)
time_1 = numToByteArray(25000000) ### unit is 40 ns
time_2 = numToByteArray(50000000)
time_3 = numToByteArray(75000000)
time_4 = numToByteArray(100000000)
time_5 = numToByteArray(125000000)
time_6 = numToByteArray(150000000)
time_7 = numToByteArray(175000000)

logic_0 = bytearray.fromhex(u'0000 0100')  ## logic is [23 to 16][31 to 24][7 to 0][15 to 8]
logic_1 = bytearray.fromhex(u'0000 0200')
logic_2 = bytearray.fromhex(u'0000 0400')
logic_3 = bytearray.fromhex(u'0000 0800')
logic_4 = bytearray.fromhex(u'0000 1000')
logic_5 = bytearray.fromhex(u'0000 2000')
logic_6 = bytearray.fromhex(u'0000 4000')
logic_7 = bytearray.fromhex(u'0000 8000')

data = time_0+logic_0+time_1+logic_1+time_2+logic_2+time_3+logic_3+time_4+logic_4+time_5+logic_5+time_6+logic_6+time_7+logic_7
data = padTo16(data)


#data = bytearray.fromhex(u'0001 0203 0405 0607 0809 0a0b 0c0d 0e0f')

#bytearray => each one is 8-bit byte
#buf = bytearray(os.urandom(512))


### For USB 3.0, data must be a multiple of 16 bytes.
xem.WriteToBlockPipeIn(0x80,16,data)

#time.sleep(1)
print "start"
xem.SetWireInValue(0x00,0x04,0xFF)
xem.UpdateWireIns()