from labrad.units import WithUnit
import labrad
cxn = labrad.connect()
ni = cxn.ni_analog_server
ni.get_voltage('comp1')
ni.set_voltage('comp1',WithUnit(2,'V'))