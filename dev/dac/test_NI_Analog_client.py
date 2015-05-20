from labrad.units import WithUnit
import labrad
import numpy as np
cxn = labrad.connect()
ni = cxn.ni_analog_server

#ni.get_voltage('comp1')
#ni.set_voltage('comp1',WithUnit(2,'V'))

pattern = np.array([[0,0.1,0.3,0.4,0.42,0.45,0.997,3],
                    [0,0,1,2,2,2,-1,0],
                    [0,0,1,2,2,2,-1,0],
                    [0,0,1,2,2,2,-1,0],
                    [1,1,2,3,3,3,0,1]])

ni.set_voltage_pattern(pattern,False,100000)

#ni.set_voltage('comp1',WithUnit(2,'V'))