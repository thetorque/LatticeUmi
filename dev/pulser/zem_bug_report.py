import os
import time
import ok

xem = ok.FrontPanel()
xem.OpenBySerial('')
#xem.ConfigureFPGA('C:\Users\Thaned\Dropbox\Hardware\RIKEN_Hardware\ZEM_bug_test_case\output_files\Pulser.rbf')
xem.ConfigureFPGA('pipetest.rbf')
#xem.ConfigureFPGA('Pulser.rbf')

def padTo16(data):
    size_needed = (16 - len(data)%16)%16
    zero_padding = bytearray(size_needed)
    return data+zero_padding


logic_0 = bytearray.fromhex(u'0000 0000 0000 0011')
 
data = logic_0
data = padTo16(data)

for i in range(100000):
    print "iteration number = ", i
    xem.WriteToBlockPipeIn(0x80,16,data)
    
    xem.SetWireInValue(0x01,0x0000,0xFFFF)
    xem.UpdateWireIns()
    
    xem.UpdateWireOuts()
    a = xem.GetWireOutValue(0x21)
    b = xem.GetWireOutValue(0x22)
    
    print a
    print b
    
    xem.ActivateTriggerIn(0x40,1)
    #time.sleep(0.1)