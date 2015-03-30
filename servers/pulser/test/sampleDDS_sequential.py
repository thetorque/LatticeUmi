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
p.add_ttl_pulse('ttl_0',WithUnit(0,'ms'),WithUnit(100,'ms'))
p.add_ttl_pulse('ttl_0',WithUnit(200,'ms'),WithUnit(100,'ms'))
p.add_ttl_pulse('ttl_0',WithUnit(400,'ms'),WithUnit(100,'ms'))

## add a list of DDS

DDS = [('DDS_0', WithUnit(0.1, 'ms'), WithUnit(250, 'ms'), WithUnit(85.0, 'MHz'), WithUnit(-23.0, 'dBm'), WithUnit(0.0,'deg')),
       ('DDS_0', WithUnit(500, 'ms'), WithUnit(250, 'ms'), WithUnit(85.0, 'MHz'), WithUnit(-23.0, 'dBm'), WithUnit(0.0,'deg')),
       ('DDS_1', WithUnit(1000, 'ms'), WithUnit(100, 'ms'), WithUnit(88.0, 'MHz'), WithUnit(-40.0, 'dBm'), WithUnit(0.0,'deg')),
       ('DDS_1', WithUnit(2000, 'ms'), WithUnit(2000, 'ms'), WithUnit(87.0, 'MHz'), WithUnit(-40.0, 'dBm'), WithUnit(0.0,'deg'))
       ]

## program DDS
p.add_dds_pulses(DDS)

##program sequence
p.program_sequence()

##start once
p.start_number(2)

# ##wait until sequence is done
p.wait_sequence_done()
# 
# ## stop sequence
p.stop_sequence()