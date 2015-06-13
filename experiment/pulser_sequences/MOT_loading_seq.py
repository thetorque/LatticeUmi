from servers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from experiment.pulser_sequences.MOT_detection import MOT_detection
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_loading_seq(pulse_sequence):
    
    required_parameters = [ 
                           ('MOT_loading', 'loading_time'),
                           ('MOT_loading', 'compress_time'),
                           ('MOT_loading', 'big_MOT_loading_power'),
                           ('MOT_loading', 'compress_MOT_power'),
                           ('MOT_loading', 'big_MOT_loading_freq'),
                           ('MOT_loading', 'compress_MOT_freq'),
                           ]
#     
    required_subsequences = [MOT_detection]
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        p = self.parameters
        #self.end = WithUnit(10, 'us')
        no_amp_ramp = WithUnit(0,'dB')
        comb_amp = WithUnit(4.0,'dBm')
        MOT_freq = WithUnit(150.0,'MHz')
        no_freq_ramp = WithUnit(0,'MHz')
        no_phase = WithUnit(0.0,'deg')
        
        #detection_frequency = WithUnit(8.800,'MHz')
        
        MOT_time = p.MOT_loading.loading_time
        compress_time = p.MOT_loading.compress_time
        
        MOT_power = p.MOT_loading.big_MOT_loading_power
        compress_power = p.MOT_loading.compress_MOT_power
        
        MOT_loading_freq = p.MOT_loading.big_MOT_loading_freq
        compress_freq = p.MOT_loading.compress_MOT_freq
        
        self.end = WithUnit(10,'us')
        
        #trigger analog out
        self.addTTL('AO1',WithUnit(10,'us'),WithUnit(1,'ms'))
        self.addTTL('AO2',WithUnit(10,'us'),WithUnit(1,'ms'))
        
        #('DDS_0', offset, duration, WithUnit(100.0, 'MHz'), WithUnit(-63,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        #self.addDDS('DDS_0',WithUnit(10,'us'),WithUnit(1.0,'s'),WithUnit(100.0,'MHz'),WithUnit(-20,'dBm'))
        #self.addDDS('DDS_0',WithUnit(1.01,'s'),WithUnit(200.0,'ms'),WithUnit(60.0,'MHz'),WithUnit(-20,'dBm'))
        
        #Big MOT light on
        
        self.addDDS('SMALL_MOT',WithUnit(10,'us'),MOT_time-WithUnit(10,'us'), MOT_freq,WithUnit(-48,'dBm'))
        self.addTTL('BIG_MOT_SH',WithUnit(10,'us'),MOT_time-WithUnit(10,'us'))
        self.addDDS('BIG_MOT',WithUnit(10,'us'),MOT_time-compress_time-WithUnit(10,'us'),MOT_freq, MOT_power)
        self.addDDS('BIG_MOT',MOT_time-compress_time,compress_time,MOT_freq, compress_power)
        
        #254 comb
        
        self.addDDS('254_COMB', WithUnit(10.0,'us'), MOT_time-compress_time-WithUnit(10,'us'), MOT_loading_freq,comb_amp,no_phase,WithUnit(0.01,'MHz'),no_amp_ramp)
        self.addDDS('254_COMB', MOT_time-compress_time, compress_time, compress_freq, comb_amp, no_phase, WithUnit(0.01,'MHz'),no_amp_ramp)
        
        
        self.end = MOT_time + self.end 
        
        ### add detection ###
        
        self.addSequence(MOT_detection)

        
#         self.addTTL('ttl_1',WithUnit(10,'ms'),WithUnit(250,'ms'))
#         self.addTTL('ttl_1',WithUnit(500,'ms'),WithUnit(250,'ms'))
#         self.addTTL('ttl_1',WithUnit(1000,'ms'),WithUnit(500,'ms'))
