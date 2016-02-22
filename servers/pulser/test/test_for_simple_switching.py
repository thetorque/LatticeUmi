from servers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit
from treedict import TreeDict
from servers.pulser.pulse_sequences.plot_sequence import SequencePlotter
import labrad

### main code
cxn = labrad.connect() ##make labrad connection
p = cxn.pulser ## get the pulser server

p.new_sequence() ## initialize a new sequence

## add some ttl switching
#p.add_ttl_pulse('ttl_0',WithUnit(0,'ms'),WithUnit(100,'ms'))
p.add_ttl_pulse('ttl_0',WithUnit(200.00032,'ms'),WithUnit(100,'ms'))
p.add_ttl_pulse('ttl_0',WithUnit(400,'ms'),WithUnit(100,'ms'))

## add a list of DDS ##

amp1 = WithUnit(-30,'dBm')
amp2 = WithUnit(-36,'dBm')
no_amp_ramp = WithUnit(0,'dB')


DDS = [('DDS_0', WithUnit(0.1, 'ms'), WithUnit(199.9, 'ms'), WithUnit(40.0, 'MHz'), WithUnit(-10,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
       ('DDS_0', WithUnit(200.0, 'ms'), WithUnit(1000.0, 'ms'), WithUnit(39.0, 'MHz'), WithUnit(-10,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.005, 'MHz'),no_amp_ramp),
       ('DDS_0', WithUnit(1200.0, 'ms'), WithUnit(500.0, 'ms'), WithUnit(39.0, 'MHz'), WithUnit(-37,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp)
       ]

## program DDS
p.add_dds_pulses(DDS)

##program sequence##
p.program_sequence()

####enable line triggering

p.line_trigger_state(True)


##start once
for i in range(1):
    #print i
    p.start_number(3)
    #p.start_infinite()

####wait until sequence is done
    p.wait_sequence_done()
# 
# ## stop sequence
print "seq is done."
p.stop_sequence()