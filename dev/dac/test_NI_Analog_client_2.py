from labrad.units import WithUnit
import labrad
import numpy as np
cxn = labrad.connect()
ni = cxn.ni_analog_server

## bias x
channel_0 = np.array([[0.0,1.0,1.009,1.219,1.228,1.50],
                     [3.5,3.5,0.0,0.0,3.5,3.5]])
##bias y

channel_1 = np.array([[0.0,1.0,1.009,1.219,1.228,1.50],
                     [3.0,3.0,0.0,0.0,3.0,3.0]])
## bias z
channel_2 = np.array([[0.0,1.0,1.009,1.219,1.228,1.50],
                     [3.0,3.0,5.5,5.5,3.0,3.0]])

## MOT B
channel_3 = np.array([[0.0,0.85,0.86,1.0,1.01,1.22,1.23,1.50],
                     [3.5,3.5,8.0,8.0,0.0,0.0,8.0,8.0]])

## lattice power

channel_4 = np.array([[0.0,0.82,0.83,1.0,1.01,1.04,1.05,1.50],
                     [-0.8,-0.8,-1.7,-1.7,-1.0,-1.0,-1.3,-1.3]])

## clock power

channel_5 = np.array([[0.0,1.5],
                     [8.0,8.0]])

###
##time = np.union1d(channel_0[0],channel_1[0],channel_2[0],channel_3[0],channel_4[0],channel_5[0])
time = reduce(np.union1d,(channel_0[0],channel_1[0],channel_2[0],channel_3[0],channel_4[0],channel_5[0]))
#print time
total_data = time

for channel, data in [(0, channel_0),
                      (1, channel_1),
                      (2, channel_2),
                      (3, channel_3),
                      (4, channel_4),
                      (5, channel_5),
                       ]:

    voltage_array = data[1]
    time_array = data[0]
    ch = np.ones_like(time)
    ch[0] = voltage_array[0] ## initialize first element
    #print "channel", channel
    #print voltage_array

    index = np.searchsorted(time_array,time, side='left')

    for i in range(np.size(index)-1):
        i = i+1
        #print "step", i
        slope = (voltage_array[index[i]]-voltage_array[index[i]-1])/(time_array[index[i]]-time_array[index[i]-1])
        ch[i] = ch[i-1]+slope*(time[i]-time[i-1])
        
    total_data = np.vstack((total_data,ch))
    
#print total_data

pattern = total_data
ni.set_voltage_pattern(pattern,False,100000)
