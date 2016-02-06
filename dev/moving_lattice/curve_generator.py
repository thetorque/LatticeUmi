from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import time


total_time = 0.05 #100 ms
time_step = 0.00001 # 10 us

max_f_range = 122070.3125
max_f = 100000.0
f_resolution = max_f_range/2**32

def curve(time):
    last_index = np.size(time)

    voltage=np.ones_like(time)
    ## first half
    t = time[0:last_index/2]
    voltage[0:last_index/2]= (9.0/20.0) * ((-1760.0/9.0)*(t**4)+(320.0/3.0)*(t**3))
    ## second half
    t = time[last_index/2:last_index]
    voltage[last_index/2:last_index] = (9.0/20.0) * ((800.0/9.0)*(t**4)-(1600.0/9.0)*(t**3)+(320.0/3.0)*(t**2)-(160.0/9.0)*t+10.0/9.0)

    return voltage

## define time array

data_depth = 4096

time_array = np.linspace(0,0.5,data_depth) ###which is 2**12
time_integer = np.arange(0,data_depth,1)

voltage = curve(time_array)

freq_array = max_f*voltage/f_resolution

### save to text file
f = open("data.mif",'w')

initial_text = np.array(["WIDTH=32;\n\
DEPTH="+str(data_depth)+";\n\
\n\
ADDRESS_RADIX=UNS;\n\
DATA_RADIX=UNS;\n\
\n\
CONTENT BEGIN\n\
"])

np.savetxt(f,initial_text,fmt="%s")

for i in range(np.size(time_array)):
    str_to_save = np.array([str(time_integer[i]) + "   :   " + str(int(freq_array[i])) + ";" ])
    np.savetxt(f,str_to_save,fmt="%s")
    #print i

initial_text = np.array(["\n\n\
END;\
"])

np.savetxt(f,initial_text,fmt="%s")

f.close()

plt.plot(time_array, freq_array)
plt.show()


