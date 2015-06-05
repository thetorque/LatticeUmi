from servers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit
from treedict import TreeDict
from servers.pulser.pulse_sequences.plot_sequence import SequencePlotter
import labrad
import time
'''This is the code I use to test the various timing of the pulse programming'''
### main code
cxn = labrad.connect() ##make labrad connection
p = cxn.pulser ## get the pulser server

#p.new_sequence() ## initialize a new sequence

## add some ttl switching
#p.add_ttl_pulse('ttl_0',WithUnit(0,'ms'),WithUnit(100,'ms'))
#p.add_ttl_pulse('ttl_0',WithUnit(200,'ms'),WithUnit(100,'ms'))
#p.add_ttl_pulse('ttl_0',WithUnit(400,'ms'),WithUnit(100,'ms'))

## add a list of DDS ##

amp1 = WithUnit(-30,'dBm')
amp2 = WithUnit(-40,'dBm')
no_amp_ramp = WithUnit(0,'dB')


DDS = [('DDS_0', WithUnit(0.001, 'ms'), WithUnit(10.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(5.1, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(10.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(20.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(22.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(50.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(60.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(70.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(80.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(90.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(100.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(110.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(120.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_1', WithUnit(130.0, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(5.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(10.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(20.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(22.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(50.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(60.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(70.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(80.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(90.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(100.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(110.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(120.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_3', WithUnit(130.2, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_2', WithUnit(5.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_2', WithUnit(10.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_2', WithUnit(20.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_2', WithUnit(22.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(50.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(60.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(70.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(80.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(90.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(100.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(110.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(120.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(130.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_2', WithUnit(205.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_2', WithUnit(210.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_2', WithUnit(220.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        ('DDS_2', WithUnit(222.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(250.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(260.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(270.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(280.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(290.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(300.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(310.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(320.3, 'ms'), WithUnit(1.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
         ('DDS_2', WithUnit(330.3, 'ms'), WithUnit(1000.0, 'ms'), WithUnit(0.1, 'MHz'), WithUnit(-20,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
       ]

## program DDS
#p.add_dds_pulses(DDS)
start = time.clock()
##program sequence##
#p.program_sequence()

##start once
for i in range(10):
    #print i
    start_iteration = time.time()
    print i, "start time is ", time.clock()-start
    start = time.clock()
    p.new_sequence()
    print i, "new sequence time is ", time.clock()-start
    start = time.clock()
    p.add_dds_pulses(DDS)
    print i, "add dds pulse time is ", time.clock()-start
    start = time.clock()
    p.program_sequence()
    print i, "program seq time is ", time.clock()-start
    start = time.clock()
    p.start_number(1)
    print i, "start number time is ", time.clock()-start
    start = time.clock()
# ##wait until sequence is done
    #p.wait_sequence_done()
    time.sleep(1.330)
    print i, "seq done time is ", time.clock()-start
    start = time.clock()
    p.stop_sequence()
    print i, "stop seq time is ", time.clock()-start
    print i, "total time is ", time.time()-start_iteration
# 
# ## stop sequence
#p.stop_sequence()