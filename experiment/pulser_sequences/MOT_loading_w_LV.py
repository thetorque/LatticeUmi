from servers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
#from experiment.pulser_sequences.MOT_detection import MOT_detection
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_loading_seq(pulse_sequence):
    
    required_parameters = [ 
                           ('MOT_loading', 'loading_time'),
                           ('MOT_loading', 'compress_time'),
                           ('MOT_loading', 'big_MOT_loading_power'),
                           ('MOT_loading', 'compress_MOT_power'),
                           ('MOT_loading', 'detection_power'),
                           ('MOT_loading', 'wait_time'),
                           ('MOT_loading', 'detect_bigMOT')
                           ]
#     
    required_subsequences = []
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        p = self.parameters
        #self.end = WithUnit(10, 'us')
        no_amp_ramp = WithUnit(0,'dB')
        comb_amp = WithUnit(4.0,'dBm')
        off_power = WithUnit(-48.0,'dBm')
        MOT_freq = WithUnit(150.0,'MHz')
        no_freq_ramp = WithUnit(0,'MHz')
        no_phase = WithUnit(0.0,'deg')
        

        
        self.end = WithUnit(10,'us')
        
        #trigger analog out
        self.addTTL('AO1',WithUnit(10,'us'),WithUnit(1,'ms'))
        self.addTTL('AO2',WithUnit(10,'us'),WithUnit(1,'ms'))
        
        loading_time = p.MOT_loading.loading_time
        
        wait_time = p.MOT_loading.wait_time
        
        MOT_power = p.MOT_loading.big_MOT_loading_power
        detection_power = p.MOT_loading.detection_power
        compress_power = p.MOT_loading.compress_MOT_power

        self.addDDS('BIG_MOT',   self.end, loading_time-self.end-WithUnit(60,'ms'), MOT_freq, MOT_power)
        self.addDDS('BIG_MOT',   loading_time-WithUnit(60,'ms'), WithUnit(60,'ms'), MOT_freq, compress_power)
        
        detect_w_big = p.MOT_loading.detect_bigMOT
        
        if detect_w_big:
            #self.addTTL('BIG_MOT_SH',self.end,loading_time+wait_time+WithUnit(150,'ms'))
            self.addDDS('BIG_MOT',   loading_time+wait_time,                    WithUnit(40,'ms'), MOT_freq, MOT_power)
            self.addDDS('BIG_MOT',   loading_time+wait_time+WithUnit(50,'ms'),  WithUnit(40,'ms'), MOT_freq, MOT_power)
            self.addDDS('BIG_MOT',   loading_time+wait_time+WithUnit(100,'ms'), WithUnit(40,'ms'), MOT_freq, MOT_power)
        else:
            #self.addTTL('BIG_MOT_SH',self.end,loading_time-self.end)
            self.addTTL('BIG_MOT_SH',loading_time,wait_time + WithUnit(150,'ms'))
            self.addDDS('BIG_MOT',   loading_time, WithUnit(150,'ms')+wait_time, MOT_freq, off_power)
            self.addTTL('sMOT_PROBE', loading_time+wait_time-WithUnit(5,'ms'), WithUnit(150,'ms'))
            self.addTTL('sMOT_PROBE_SPIN', loading_time+wait_time-WithUnit(5,'ms'), WithUnit(150,'ms'))
            self.addDDS('SMALL_MOT',   loading_time+wait_time,                    WithUnit(40,'ms'), MOT_freq, detection_power)
            self.addDDS('SMALL_MOT',   loading_time+wait_time+WithUnit(50,'ms'),  WithUnit(40,'ms'), MOT_freq, detection_power)
            self.addDDS('SMALL_MOT',   loading_time+wait_time+WithUnit(100,'ms'), WithUnit(40,'ms'), MOT_freq, detection_power)
        
        
        

        camera_offset = WithUnit(2,'ms')
        self.addTTL('CAMERA',loading_time+wait_time+camera_offset,WithUnit(3,'ms'))
        self.addTTL('CAMERA',loading_time+wait_time+WithUnit(50,'ms')+camera_offset,WithUnit(3,'ms'))
        self.addTTL('CAMERA',loading_time+wait_time+WithUnit(100,'ms')+camera_offset,WithUnit(3,'ms'))
        


