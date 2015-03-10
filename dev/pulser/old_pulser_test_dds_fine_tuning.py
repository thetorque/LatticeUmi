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
xem.ConfigureFPGA('C:\Users\Thaned\Dropbox\Hardware\RIKEN_Hardware\Pulser_w_line_triggering_2015_03_10\photon\photon.bit')
delay = 0.1

padding = bytearray.fromhex(u'0000') 
setting_0 = bytearray.fromhex(u'0000 00b0 0000 0009') ## []frequency[7 to 0][15 to 8][23 to 16][31 to 24]
setting_1 = bytearray.fromhex(u'0000 00b0 0000 0008')
setting_2 = bytearray.fromhex(u'0000 00b0 0000 0007')
setting_3 = bytearray.fromhex(u'0000 00c0 0000 0006')
data = padding + setting_0+setting_1+setting_2+setting_3
data = padTo16(data)


xem.ActivateTriggerIn(0x40,4)

xem.SetWireInValue(0x04,0x00,0xFF)
xem.UpdateWireIns()

xem.WriteToBlockPipeIn(0x81,16,data)

time.sleep(1)
xem.ActivateTriggerIn(0x40,5)
time.sleep(1)
xem.ActivateTriggerIn(0x40,5)
time.sleep(1)
xem.ActivateTriggerIn(0x40,5)
