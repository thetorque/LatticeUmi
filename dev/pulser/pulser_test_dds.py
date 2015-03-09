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



# set wire in (FPGA reads data). First is the address, second is the value, last is the masking (1 for the bit you want to change)
##xem.SetWireInValue(0x00,0b10101000,0xF8)
# after this you have to update the wire in
##xem.UpdateWireIns()

logic_0 = bytearray.fromhex(u'0000 0000 0000 0002')
logic_1 = bytearray.fromhex(u'0000 0000 0000 0003')
logic_2 = bytearray.fromhex(u'0000 0000 0000 0004')
logic_3 = bytearray.fromhex(u'0000 0000 0000 0005')
logic_4 = bytearray.fromhex(u'0000 0000 0000 0006')
logic_5 = bytearray.fromhex(u'0000 0000 0000 0007')
logic_6 = bytearray.fromhex(u'0000 0000 0000 0008')
logic_7 = bytearray.fromhex(u'0000 0000 0000 0009')

data = logic_0+logic_1+logic_2+logic_3+logic_4+logic_5+logic_6+logic_7
data = padTo16(data)

#data = bytearray(os.urandom(160))

#data = bytearray.fromhex(u'0001 0203 0405 0607 0809 0a0b 0c0d 0e0f')

#bytearray => each one is 8-bit byte
#buf = bytearray(os.urandom(512))



##reset ram position of the DDS
time.sleep(1)
print "reset ram position"
xem.ActivateTriggerIn(0x40,4)
##reset dds fifo on pulser
time.sleep(1)
print "reset fifo"
xem.ActivateTriggerIn(0x40,7)


##set channel
xem.SetWireInValue(0x04,0x00,0xFF)
xem.UpdateWireIns()
### For USB 3.0, data must be a multiple of 16 bytes.
time.sleep(1)
print "write to block pipe"
xem.WriteToBlockPipeIn(0x81,16,data)


##reset ram position of the DDS
#xem.ActivateTriggerIn(0x40,4)
## advanced to next value
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





# set wire in (FPGA reads data). First is the address, second is the value, last is the masking (1 for the bit you want to change)
##xem.SetWireInValue(0x00,0b10101000,0xF8)
# after this you have to update the wire in
##xem.UpdateWireIns()

logic_0 = bytearray.fromhex(u'0000 0000 0000 0004')
logic_1 = bytearray.fromhex(u'0000 0000 0000 0000')
data = logic_0 + logic_1



##reset ram position of the DDS
# time.sleep(1)
# print "reset ram position"
xem.ActivateTriggerIn(0x40,4)
#reset dds fifo on pulser
#time.sleep(2)
#print "reset fifo"
xem.ActivateTriggerIn(0x40,7)


##set channel
xem.SetWireInValue(0x04,0x00,0xFF)
xem.UpdateWireIns()
### For USB 3.0, data must be a multiple of 16 bytes.
#time.sleep(1)
print "write to block pipe"
xem.WriteToBlockPipeIn(0x81,16,data)