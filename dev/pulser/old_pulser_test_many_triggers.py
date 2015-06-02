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
delay = 0.001

xem.ActivateTriggerIn(0x40,4)
time.sleep(delay)
xem.ActivateTriggerIn(0x40,5)
time.sleep(delay)
xem.ActivateTriggerIn(0x40,5)
time.sleep(delay)
xem.ActivateTriggerIn(0x40,5)

for i in range(1000):
    print i
 
    xem.ActivateTriggerIn(0x40,5)
    time.sleep(delay)
    xem.ActivateTriggerIn(0x40,5)
    time.sleep(delay)
    xem.ActivateTriggerIn(0x40,5)
    time.sleep(delay)
    xem.ActivateTriggerIn(0x40,5)
    time.sleep(delay)