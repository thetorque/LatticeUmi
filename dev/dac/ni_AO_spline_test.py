from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import time



start_time = time.time()

## sample vertices array
t = np.array([0,0.1,0.2,0.4,0.5,0.6,1.5])
v = np.array([5,2,4,4,2,0,5])

sampling_rate = 10000 ## set sampling rate
duration = t[-1]  ## set duration of the whole sequence
sample_size = sampling_rate*duration ## calculate total number of points

## create time array
time_array = np.linspace(0, duration, sample_size+1)
volt_array = np.ones_like(time_array)

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


now = time.time()-start_time
print now

### low pass

# conv = np.zeros_like(volt_array)
# conv[np.size(conv)/2]=1
# conv[np.size(conv)/2+1]=0.75
# conv[np.size(conv)/2-1]=0.75
# conv[np.size(conv)/2+2]=0.50
# conv[np.size(conv)/2-2]=0.50
# conv[np.size(conv)/2+3]=0.25
# conv[np.size(conv)/2-3]=0.25


time_filter = time_array - time_array[-1]/2
band = 0.0005
conv = np.exp(-0.5*time_filter**2/band**2)

conv = np.delete(conv,np.where(conv<0.05))

#print conv
now = time.time()-start_time
print now

conv = conv/np.sum(conv)


## there is a problem is the start voltage is not zero then there is a slow response
volt_smooth = np.convolve(volt_array-volt_array[0], conv, 'same')+volt_array[0]

now = time.time()-start_time
print now
 
#### spline
 
# x=time_array
# y=volt_smooth
#  
# tck = interpolate.splrep(x,y,s=0)
#   
# x_new = np.arange(x[0],x[-1],0.00001)
# y_new = interpolate.splev(x_new,tck,der=0)
 
 
plt.plot(time_array,volt_smooth,'o')
plt.plot(time_array,volt_array,'o')
plt.plot(t,v,'o')
# plt.plot(time_array,volt_array,'o')
#plt.plot(x_new,y_new)
# #print tck
plt.show(block=False)

now = time.time()-start_time
print now
plt.show()

