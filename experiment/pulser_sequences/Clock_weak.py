from servers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
#from experiment.pulser_sequences.MOT_detection import MOT_detection
from labrad.units import WithUnit
from treedict import TreeDict

class Clock_weak(pulse_sequence):
    
    required_parameters = [ 
                           ('MOT_loading', 'loading_time'),
                           ('MOT_loading', 'big_MOT_loading_power'),
                           ('MOT_loading', 'compress_MOT_power'),
                           ('MOT_loading', 'detection_power'),
                           ('MOT_loading', 'wait_time'),
                           ('Clock', 'Clock_freq'),
                           ('Clock', 'SP1_duration'),
                           ('Clock', 'SP2_duration'),
                           ('Clock', 'time_before_clock'),
                           ('Clock', 'clock_duration'),
                           
                           
                           ]
#     
    required_subsequences = []
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        p = self.parameters
        
        off_power = WithUnit(-48.0,'dBm')
        MOT_freq = WithUnit(150.0,'MHz')
        

        
        self.start = WithUnit(10,'us')
        
        
        #trigger analog out
        self.addTTL('AO1',WithUnit(10,'us'),WithUnit(1,'ms'))
        self.addTTL('AO2',WithUnit(10,'us'),WithUnit(1,'ms'))
        
        loading_time = p.MOT_loading.loading_time
        wait_time = p.MOT_loading.wait_time
        
        MOT_power = p.MOT_loading.big_MOT_loading_power
        detection_power = p.MOT_loading.detection_power
        compress_power = p.MOT_loading.compress_MOT_power

        self.addDDS('BIG_MOT',   self.start, loading_time-self.start-WithUnit(60,'ms'), MOT_freq, MOT_power)
        self.addDDS('BIG_MOT',   loading_time-WithUnit(60,'ms'), WithUnit(60,'ms'), MOT_freq, compress_power)
        
        self.end = loading_time+wait_time + WithUnit(160, 'ms')
        
        ##clock laser
        
        clock_freq = p.Clock.Clock_freq
        clock_duration = p.Clock.clock_duration
        time_before_clock = p.Clock.time_before_clock
        ## add the clock interrogation pulse
        self.addDDS('Clock', loading_time+time_before_clock,  clock_duration, clock_freq, WithUnit(-5.0, 'dBm'))
        self.addTTL('dummy_clock', loading_time+time_before_clock,  clock_duration)
        ## have to fill the rest of the time for the DNC to stay locked
        clock_filling_start_time = loading_time+time_before_clock+clock_duration
        self.addDDS('Clock', clock_filling_start_time, self.end - clock_filling_start_time, WithUnit(198.0, 'MHz'), WithUnit(-5.0, 'dBm'))
        
        ## ADD sp1 and sp2
        SP1 = p.Clock.SP1_duration
        SP2 = p.Clock.SP2_duration
        if SP1 > WithUnit(0.1,'us'):
            print SP1
            self.addTTL('SP1', loading_time, time_before_clock)
            self.addDDS('SMALL_MOT',   loading_time + time_before_clock/2.0, SP1, MOT_freq, detection_power)
        if SP2 > WithUnit(0.1,'us'):
            print SP2
            self.addTTL('SP2', loading_time, time_before_clock)
            self.addDDS('SMALL_MOT',   loading_time + time_before_clock/2.0, SP2, MOT_freq, detection_power)
        self.addTTL('sMOT_PROBE_SPIN', loading_time, time_before_clock)
        
        
        ### detection
            
        self.addTTL('BIG_MOT_SH',loading_time,wait_time + WithUnit(150,'ms'))
        self.addDDS('BIG_MOT',   loading_time, WithUnit(150,'ms')+wait_time, MOT_freq, off_power)
        self.addTTL('sMOT_PROBE', loading_time+wait_time-WithUnit(5,'ms'), WithUnit(150,'ms'))
        self.addTTL('sMOT_PROBE_SPIN', loading_time+wait_time-WithUnit(5,'ms'), WithUnit(150,'ms'))
        self.addDDS('SMALL_MOT',   loading_time+wait_time, WithUnit(40,'ms'), MOT_freq, detection_power)
        self.addTTL('405_ECDL', loading_time+wait_time+WithUnit(40,'ms'),WithUnit(10,'ms'))
        self.addDDS('SMALL_MOT',   loading_time+wait_time+WithUnit(50,'ms'),  WithUnit(40,'ms'), MOT_freq, detection_power)
        self.addDDS('SMALL_MOT',   loading_time+wait_time+WithUnit(100,'ms'), WithUnit(40,'ms'), MOT_freq, detection_power)
        
        
        

        camera_offset = WithUnit(1,'ms')
        self.addTTL('CAMERA',loading_time+wait_time+camera_offset,WithUnit(3,'ms'))
        self.addTTL('CAMERA',loading_time+wait_time+WithUnit(50,'ms')+camera_offset,WithUnit(3,'ms'))
        self.addTTL('CAMERA',loading_time+wait_time+WithUnit(100,'ms')+camera_offset,WithUnit(3,'ms'))
        


