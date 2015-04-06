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

amp1 = WithUnit(-20, 'dBm')
amp2 = WithUnit(-30, 'dBm')

# DDS = [('DDS_0', WithUnit(0.1, 'ms'), WithUnit(199.9, 'ms'), WithUnit(85.0, 'MHz'), amp, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
#        ('DDS_0', WithUnit(200.0, 'ms'), WithUnit(2300.0, 'ms'), WithUnit(88.0, 'MHz'), amp, WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz')),
#        ('DDS_0', WithUnit(2.5, 's'), WithUnit(0.5, 's'), WithUnit(88.0, 'MHz'), amp, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
#        ('DDS_0', WithUnit(3.0, 's'), WithUnit(2, 's'), WithUnit(83.0, 'MHz'), amp, WithUnit(0.0,'deg'),WithUnit(0.005, 'MHz')),
#        ('DDS_0', WithUnit(5.0, 's'), WithUnit(0.5, 's'), WithUnit(85.0, 'MHz'), amp, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
#        ('DDS_0', WithUnit(5.5, 's'), WithUnit(500, 'ms'), WithUnit(82.0, 'MHz'), amp, WithUnit(0.0,'deg'),WithUnit(0.02, 'MHz')),
#        ('DDS_0', WithUnit(6.0, 's'), WithUnit(500, 'ms'), WithUnit(82.0, 'MHz'), amp, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'))
#        ]

DDS = [('DDS_0', WithUnit(0.1, 'ms'), WithUnit(199.9, 'ms'), WithUnit(85.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
       ('DDS_0', WithUnit(200.0, 'ms'), WithUnit(2300.0, 'ms'), WithUnit(88.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz')),
       ('DDS_0', WithUnit(2.5, 's'), WithUnit(0.5, 's'), WithUnit(88.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
       ('DDS_0', WithUnit(3.0, 's'), WithUnit(2, 's'), WithUnit(83.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.005, 'MHz')),
       ('DDS_0', WithUnit(5.0, 's'), WithUnit(0.5, 's'), WithUnit(85.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
       ('DDS_0', WithUnit(5.5, 's'), WithUnit(500, 'ms'), WithUnit(82.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.02, 'MHz')),
       ('DDS_0', WithUnit(6.0, 's'), WithUnit(500, 'ms'), WithUnit(82.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
       
       ('DDS_1', WithUnit(0.1, 'ms'), WithUnit(499.9, 'ms'), WithUnit(85.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
       ('DDS_1', WithUnit(500.0, 'ms'), WithUnit(2500.0, 'ms'), WithUnit(83.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz')),
       ('DDS_1', WithUnit(3.0, 's'), WithUnit(1.5, 's'), WithUnit(83.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
       ('DDS_1', WithUnit(4.5, 's'), WithUnit(1.3, 's'), WithUnit(84.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.005, 'MHz')),
       ('DDS_1', WithUnit(5.8, 's'), WithUnit(0.2, 's'), WithUnit(80.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz')),
       ('DDS_1', WithUnit(6.0, 's'), WithUnit(500, 'ms'), WithUnit(82.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.02, 'MHz')),
       ('DDS_1', WithUnit(6.5, 's'), WithUnit(500, 'ms'), WithUnit(85.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'))
       ]

# DDS = [('DDS_0', WithUnit(0.1, 'ms'), WithUnit(250, 'ms'), WithUnit(85.0, 'MHz'), WithUnit(-23.0, 'dBm'), WithUnit(0.0,'deg'),ramp_rate),
#        ('DDS_0', WithUnit(500, 'ms'), WithUnit(250, 'ms'), WithUnit(85.0, 'MHz'), WithUnit(-23.0, 'dBm'), WithUnit(0.0,'deg'),ramp_rate),
#        ('DDS_1', WithUnit(1000, 'ms'), WithUnit(100, 'ms'), WithUnit(88.0, 'MHz'), WithUnit(-40.0, 'dBm'), WithUnit(0.0,'deg'),ramp_rate),
#        ('DDS_1', WithUnit(2000, 'ms'), WithUnit(2000, 'ms'), WithUnit(87.0, 'MHz'), WithUnit(-40.0, 'dBm'), WithUnit(0.0,'deg'),ramp_rate)
#        ]

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