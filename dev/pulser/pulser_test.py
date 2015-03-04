import ok
xem = ok.FrontPanel()
xem.OpenBySerial('')
#xem.ConfigureFPGA('C:\Users\Thaned\Desktop\Hardware\RIKEN_Hardware\Pulser_Altera\output_files\Pulser.rbf')

# set wire in (FPGA reads data). First is the address, second is the value, last is the masking (1 for the bit you want to change)
xem.SetWireInValue(0x00,0b10101000,0xF8)
# after this you have to update the wire in
xem.UpdateWireIns()