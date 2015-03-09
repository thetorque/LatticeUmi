import os
import time
import ok

xem = ok.FrontPanel()
xem.OpenBySerial('')
xem.ConfigureFPGA('C:\Users\Thaned\Desktop\Hardware\RIKEN_Hardware\Pulser_Altera\output_files\Pulser.rbf')

#xem.SetWireInValue(0x04,0b00000000,0xFF)
#xem.UpdateWireIns()

def numToByteArray(number):
    #a,b = number//65536, number %65536
    b = bytearray(4)
    b[0] = number%256
    b[1] = (number//256)%256
    b[2] = (number//65536)%256
    b[3] = (number//16777216)%256
    return b

def padTo16(data):
    size_needed = (16 - len(data)%16)%16
    zero_padding = bytearray(size_needed)
    return data+zero_padding


logic_0 = bytearray.fromhex(u'0000 0000 0000 0002')
logic_1 = bytearray.fromhex(u'0000 0000 0000 0003')
logic_2 = bytearray.fromhex(u'0000 0000 0000 0004')
logic_3 = bytearray.fromhex(u'0000 0000 0000 0005')
logic_4 = bytearray.fromhex(u'0000 0000 0000 0006')
logic_5 = bytearray.fromhex(u'0000 0000 0000 0007')
logic_6 = bytearray.fromhex(u'0000 0000 0000 0008')
logic_7 = bytearray.fromhex(u'0000 0000 0000 0009')
 
data = logic_0+logic_1+logic_2+logic_3+logic_4+logic_5+logic_6+logic_7
#data = padTo16(data)


##reset ram position of the DDS

xem.ActivateTriggerIn(0x40,4)
##reset dds fifo on pulser
xem.ActivateTriggerIn(0x40,7)


##set channel
xem.SetWireInValue(0x04,0x00,0xFF)
xem.UpdateWireIns()
### For USB 3.0, data must be a multiple of 16 bytes.
print '1'
xem.WriteToBlockPipeIn(0x81,16,data)

time.sleep(0.5)
xem.ActivateTriggerIn(0x40,5)
time.sleep(0.5)
xem.ActivateTriggerIn(0x40,5)
time.sleep(0.5)
xem.ActivateTriggerIn(0x40,5)
time.sleep(0.5)
xem.ActivateTriggerIn(0x40,5)
time.sleep(0.5)
xem.ActivateTriggerIn(0x40,5)

for i in range(4000):
    #xem.ConfigureFPGA('C:\Users\Thaned\Desktop\Hardware\RIKEN_Hardware\Pulser_Altera\output_files\Pulser.rbf')
    logic_0 = bytearray.fromhex(u'0000 0000 0000 0004 0000 0000 0000 0000')
    logic_1 = bytearray.fromhex(u'0000 0000 0000 0000 0000 0000 0000 0000')
    data = logic_0 + logic_1
    xem.ActivateTriggerIn(0x40,4)
    xem.WriteToBlockPipeIn(0x81,16,data)
    #time.sleep(0.1)
    logic_0 = bytearray.fromhex(u'0000 0000 0000 0002 0000 0000 0000 0000')
    logic_1 = bytearray.fromhex(u'0000 0000 0000 0000 0000 0000 0000 0000')
    data = logic_0 + logic_1
    xem.ActivateTriggerIn(0x40,4)
    xem.WriteToBlockPipeIn(0x81,16,data)
    #time.sleep(0.1)


