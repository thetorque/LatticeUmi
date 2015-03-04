## this program creates a sequence of analog out 
## The idea is to suppl vortices of the ramp and then create an array of voltages


import numpy as np
import time

sampling_rate = 100000 ## set sampling rate
duration = 1.0  ## set duration of the whole sequence
sample_size = sampling_rate*duration ## calculate total number of points

## create time array
time_array = np.linspace(0, duration, sample_size+1)
volt_array = np.ones_like(time_array)

t = np.array([0,0.1,0.3,0.4,0.42,0.45,0.997,1])
v = np.array([0,0,1,2,-1,2,-1,0])

#print volt_array


volt_array[0] = v[0] ### initial points
for i in range(t.size-1):
    #i = 0
    #print i
    time_location = np.where((time_array>t[i])*(time_array<=t[i+1])) ### look for the location of the time span we are interested in
    slope = (v[i+1]-v[i])/(t[i+1]-t[i]) ### calculate the voltage slope in this region
    #print "v is ", v[i]
    #print "slope is ", slope
    volt_array[time_location] = v[i]+slope*(time_array[time_location]-t[i]) ## compute the voltage value


channel_0 = volt_array
channel_1 = -volt_array

data = time_array
data = np.vstack((data,channel_0,channel_1))
# data = np.vstack((data,channel_0,channel_1,channel_2))
 
np.save("ramp",data)



# #print time_array
# 
# channel_0 = 0.2*np.sin(time_array*2*np.pi*4)-0.5
# channel_1 = 0.2*np.sin(time_array*2*np.pi*8)-0.5
# channel_2 = 0.2*np.sin(time_array*2*np.pi*10)
# 
# data = time_array
# data = np.vstack((data,channel_0,channel_1))
# # data = np.vstack((data,channel_0,channel_1,channel_2))
# 
# np.save("test_ao_sequence1",data)
# 
# channel_0 = 0.2*np.sin(time_array*2*np.pi*4)+0.5
# channel_1 = 0.2*np.sin(time_array*2*np.pi*8)+0.5
# channel_2 = 0.2*np.sin(time_array*2*np.pi*10)
# 
# data = time_array
# data = np.vstack((data,channel_0,channel_1))
# # data = np.vstack((data,channel_0,channel_1,channel_2))
# 
# np.save("test_ao_sequence2",data)