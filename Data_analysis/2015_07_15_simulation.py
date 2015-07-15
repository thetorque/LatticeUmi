from __future__ import division
import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit
import time

drift_rate = 0.1 ## drift rate in Hz/s 
start_time = time.time()

def current_real_frequency(time):
    duration = time - start_time
    freq = duration*drift_rate + np.sin(duration*1)
    #freq = np.sin(duration*1)
    return freq
    
current_clock_freq = 0.0

#integrator = np.zeros(20)
integrator = []

center_f_array = []
error_array = []

# hl, = pyplot.plot([1],[1],'o')
# pyplot.show()

for i in range(1000):
    #print i
    time.sleep(0.1)
    error_signal = current_real_frequency(time.time()) - current_clock_freq
    #integrator = np.roll(integrator,1)
    #integrator[0] = error_signal
    integrator.append(error_signal)
    current_clock_freq = current_clock_freq + error_signal + 0.1*np.sum(integrator)#/(np.size(integrator)+1)
    center_f_array.append(current_clock_freq)
    error_array.append(error_signal)
#     hl.set_xdata(center_f_array)
#     hl.set_ydata(center_f_array)
    #pyplot.draw()
#    line.set_ydata(center_f_array)
#     line.set_xdata(np.ones_like(center_f_array))
#     fig.canvas.draw()
    #fig.show()
    print "err is ", error_signal, "freq is ", current_clock_freq, "int is ", np.sum(integrator)
    #print "int is ", integrator
print "average is ", np.sum(error_array), " pm ", np.std(error_array)/(np.size(error_array)+1)
pyplot.plot(error_array, 'o')
pyplot.show()