import os
import time
import ok

def padTo16(data):
    size_needed = (16 - len(data)%16)%16
    zero_padding = bytearray(size_needed)
    return data+zero_padding

xem = ok.FrontPanel()
xem.OpenBySerial('')
#xem.ConfigureFPGA('C:\Users\Thaned\Dropbox\Hardware\RIKEN_Hardware\Pulser_Altera\output_files\Pulser.rbf')
xem.ConfigureFPGA('C:\Users\Thaned\Dropbox\Hardware\RIKEN_Hardware\Pulser_w_line_triggering_2012_12_19\photon\photon.bit')
delay = 0.1

padding = bytearray.fromhex(u'0000') 
setting_0 = bytearray.fromhex(u'0000 0080 0000 0001')
setting_1 = bytearray.fromhex(u'0000 0000 0000 0002')
setting_2 = bytearray.fromhex(u'0000 0080 0000 0003')
setting_3 = bytearray.fromhex(u'0000 0000 0000 0004')
data = padding + setting_0+setting_1+setting_2+setting_3
data = padTo16(data)


xem.ActivateTriggerIn(0x40,4)

xem.SetWireInValue(0x04,0x00,0xFF)
xem.UpdateWireIns()

xem.WriteToBlockPipeIn(0x81,16,data)
time.sleep(delay)
xem.ActivateTriggerIn(0x40,5)
time.sleep(delay)
xem.ActivateTriggerIn(0x40,5)
time.sleep(delay)
xem.ActivateTriggerIn(0x40,5)

for i in range(1000):
    xem.ActivateTriggerIn(0x40,4)
    print i
    ##set channel
    xem.SetWireInValue(0x04,0x00,0xFF)
    xem.UpdateWireIns()
       
    #xem.WriteToBlockPipeIn(0x81,16,data)
    xem.WriteToBlockPipeIn(0x81,16,data)
    time.sleep(delay)
    xem.ActivateTriggerIn(0x40,5)
    time.sleep(delay)
    xem.ActivateTriggerIn(0x40,5)
    time.sleep(delay)
    xem.ActivateTriggerIn(0x40,5)
    time.sleep(delay)