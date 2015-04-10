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

amp1 = WithUnit(-30,'dBm')
amp2 = WithUnit(-40,'dBm')
no_amp_ramp = WithUnit(0,'dB')


# DDS = [('DDS_0', WithUnit(0.1, 'ms'), WithUnit(199.9, 'ms'), WithUnit(85.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
#        ('DDS_0', WithUnit(200.0, 'ms'), WithUnit(2300.0, 'ms'), WithUnit(88.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz'),no_amp_ramp),
#        ('DDS_0', WithUnit(2.5, 's'), WithUnit(0.5, 's'), WithUnit(88.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
#        ('DDS_0', WithUnit(3.0, 's'), WithUnit(2, 's'), WithUnit(83.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.005, 'MHz'),no_amp_ramp),
#        ('DDS_0', WithUnit(5.0, 's'), WithUnit(0.5, 's'), WithUnit(85.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
#        ('DDS_0', WithUnit(5.5, 's'), WithUnit(500, 'ms'), WithUnit(82.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.02, 'MHz'),no_amp_ramp),
#        ('DDS_0', WithUnit(6.0, 's'), WithUnit(500, 'ms'), WithUnit(82.0, 'MHz'), amp1, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
#        
#        ('DDS_1', WithUnit(0.1, 'ms'), WithUnit(699.9, 'ms'), WithUnit(85.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
#        ('DDS_1', WithUnit(700.0, 'ms'), WithUnit(2300.0, 'ms'), WithUnit(88.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz'),no_amp_ramp),
#        ('DDS_1', WithUnit(3.0, 's'), WithUnit(0.5, 's'), WithUnit(88.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
#        ('DDS_1', WithUnit(3.5, 's'), WithUnit(2, 's'), WithUnit(83.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.005, 'MHz'),no_amp_ramp),
#        ('DDS_1', WithUnit(5.5, 's'), WithUnit(0.5, 's'), WithUnit(85.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
#        ('DDS_1', WithUnit(6.0, 's'), WithUnit(500, 'ms'), WithUnit(82.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.02, 'MHz'),no_amp_ramp),
#        ('DDS_1', WithUnit(6.5, 's'), WithUnit(500, 'ms'), WithUnit(82.5, 'MHz'), amp2, WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp)
#        ]

DDS = [('DDS_0', WithUnit(0.1, 'ms'), WithUnit(199.9, 'ms'), WithUnit(85.0, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
       ('DDS_0', WithUnit(200.0, 'ms'), WithUnit(2300.0, 'ms'), WithUnit(88.0, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz'),no_amp_ramp),
       ('DDS_0', WithUnit(2.5, 's'), WithUnit(4000.0, 'ms'), WithUnit(88.0, 'MHz'), WithUnit(-60,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz'),WithUnit(22.0,'dB')),
       ('DDS_0', WithUnit(6.5, 's'), WithUnit(0.5, 's'), WithUnit(88.0, 'MHz'), WithUnit(-60,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
       ('DDS_1', WithUnit(0.1, 'ms'), WithUnit(199.9, 'ms'), WithUnit(85.0, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
       ('DDS_1', WithUnit(200.0, 'ms'), WithUnit(2300.0, 'ms'), WithUnit(88.0, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz'),no_amp_ramp),
       ('DDS_1', WithUnit(2.5, 's'), WithUnit(4000.0, 'ms'), WithUnit(88.0, 'MHz'), WithUnit(-60,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.003, 'MHz'),WithUnit(0.0,'dB')),
       ('DDS_1', WithUnit(6.5, 's'), WithUnit(0.5, 's'), WithUnit(88.0, 'MHz'), WithUnit(-60,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp)
       ]

## program DDS
p.add_dds_pulses(DDS)

##program sequence
p.program_sequence()

##start once
for i in range(1):
    #print i
    p.start_number(2)

# ##wait until sequence is done
    p.wait_sequence_done()
# 
# ## stop sequence
p.stop_sequence()