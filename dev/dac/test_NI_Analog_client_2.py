from labrad.units import WithUnit
import labrad
import numpy as np
cxn = labrad.connect()
ni = cxn.ni_analog_server


channel_0 = np.array([[0,0.1,0.3,0.4,0.42,0.45,2,3],
                     [0,0,1,2,2,2,-1,0]])

channel_1 = np.array([[0,0.1,0.2,0.5,0.9,3],
                     [1,-2,2,-3,-4,1]])

time = np.union1d(channel_0[0],channel_1[0])

total_data = time

for channel, data in [(0, channel_0),
                      (1, channel_1),
                       ]:

    voltage_array = data[1]
    time_array = data[0]
    ch = np.ones_like(time)
    ch[0] = voltage_array[0] ## initialize first element

    index = np.searchsorted(time_array,time, side='left')

    for i in range(np.size(index)-1):
        i = i+1
        slope = (voltage_array[index[i]]-voltage_array[index[i]-1])/(time_array[index[i]]-time_array[index[i]-1])
        ch[i] = ch[i-1]+slope*(time[i]-time[i-1])
        
    total_data = np.vstack((total_data,ch))
    
#print total_data

pattern = total_data
ni.set_voltage_pattern(pattern,False,100000)
