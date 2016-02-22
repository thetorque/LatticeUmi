
'''
test frequency modulation of a single DDS channel to try to create a rectangle frequency window.
'''

from servers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit
from treedict import TreeDict
from servers.pulser.pulse_sequences.plot_sequence import SequencePlotter
import labrad
import time
import numpy as np

### main code
cxn = labrad.connect() ##make labrad connection
p = cxn.pulser ## get the pulser server

p.new_sequence() ## initialize a new sequence

## add some ttl switching
#p.add_ttl_pulse('ttl_0',WithUnit(0,'ms'),WithUnit(100,'ms'))
#p.add_ttl_pulse('ttl_0',WithUnit(200,'ms'),WithUnit(100,'ms'))
#p.add_ttl_pulse('ttl_0',WithUnit(400,'ms'),WithUnit(100,'ms'))

## add a list of DDS

amp1 = WithUnit(0, 'dBm')
no_amp_ramp = WithUnit(0.0,'dB')
no_freq_ramp = WithUnit(0.0, 'MHz')
no_phase = WithUnit(0.0,'deg')

time_step = 250.0
total_time = 100.0 #in ms

DDS = [('DDS_0', WithUnit(0.001, 'ms'), WithUnit(0.001, 'ms'), WithUnit(60.0, 'MHz'), amp1, no_phase,no_freq_ramp,no_amp_ramp)]

for j in range(int(time_step)):
    i = j+1
    freq = 60.0+10.0*np.random.rand()
    print freq
    local_DDS = ('DDS_0', WithUnit(float(i)*total_time/time_step, 'ms'), WithUnit(total_time/time_step, 'ms'), WithUnit(freq, 'MHz'), amp1, no_phase,no_freq_ramp,no_amp_ramp)
    DDS.append(local_DDS)
    print i

## program DDS
p.add_dds_pulses(DDS)

##program sequence
p.program_sequence()


##start once
#p.start_number(5000)
p.start_infinite()
time.sleep(60)
p.start_number(1)

# ##wait until sequence is done
p.wait_sequence_done()
print "sequence is done."
# 
# ## stop sequence
p.stop_sequence()