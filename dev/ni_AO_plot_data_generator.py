## this program creates a sequence of analog out 


import numpy as np
import time

sampling_rate = 1000 ## set sampling rate
duration = 0.2 ## set duration of the whole sequence
sample_size = sampling_rate*duration ## calculate total number of points

## create time array
time_array = np.linspace(0, duration, sample_size+1)

#print time_array

channel_0 = 0.2*np.sin(time_array*2*np.pi*4)-0.5
channel_1 = 0.2*np.sin(time_array*2*np.pi*8)-0.5
channel_2 = 0.2*np.sin(time_array*2*np.pi*10)

data = time_array
data = np.vstack((data,channel_0,channel_1))
# data = np.vstack((data,channel_0,channel_1,channel_2))

np.save("test_ao_sequence1",data)

channel_0 = 0.2*np.sin(time_array*2*np.pi*4)+0.5
channel_1 = 0.2*np.sin(time_array*2*np.pi*8)+0.5
channel_2 = 0.2*np.sin(time_array*2*np.pi*10)

data = time_array
data = np.vstack((data,channel_0,channel_1))
# data = np.vstack((data,channel_0,channel_1,channel_2))

np.save("test_ao_sequence2",data)