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
                           ('MOT_loading', 'test_lattice'),
                           ('MOT_loading', 'wait_time'),
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
        

        
        self.end = WithUnit(10,'us')
        
        #trigger analog out
        self.addTTL('AO1',WithUnit(10,'us'),WithUnit(1,'ms'))
        self.addTTL('AO2',WithUnit(10,'us'),WithUnit(1,'ms'))
        
        loading_time = p.MOT_loading.loading_time
        
        wait_time = p.MOT_loading.wait_time

        
#         if p.MOT_loading.test_lattice:
#             self.addTTL('BIG_MOT_AO',self.end,loading_time-WithUnit(60.0,'ms'))
#             self.addTTL('BIG_MOT_AO',loading_time,WithUnit(40,'ms'))    
#         else:
#             self.addTTL('BIG_MOT_AO',self.end,loading_time+WithUnit(40.0,'ms'))

#       ### MOT loading period  

        self.addTTL('BIG_MOT_AO',self.end,                                  loading_time-WithUnit(0.1,'us'))
        self.addTTL('BIG_MOT_SH',self.end,loading_time+wait_time+WithUnit(150,'ms'))
        
        
        self.addTTL('BIG_MOT_AO',loading_time+wait_time,                    WithUnit(40,'ms'))
        self.addTTL('BIG_MOT_AO',loading_time+wait_time+WithUnit(50,'ms'),  WithUnit(40,'ms'))
        self.addTTL('BIG_MOT_AO',loading_time+wait_time+WithUnit(100,'ms'), WithUnit(40,'ms'))
        
        
        
#         self.addTTL('sMOT_AO',WithUnit(1005,'ms'),WithUnit(40,'ms'))
#         self.addTTL('sMOT_AO',WithUnit(1055,'ms'),WithUnit(40,'ms'))
#         self.addTTL('sMOT_AO',WithUnit(1105,'ms'),WithUnit(40,'ms'))
        
#         self.addTTL('sMOT_PROBE',WithUnit(1000,'ms'),WithUnit(500,'ms'))
#         self.addTTL('sMOT_PROBE_SPIN',WithUnit(1000,'ms'),WithUnit(500,'ms'))
        
        self.addTTL('CAMERA',loading_time+wait_time,WithUnit(3,'ms'))
        self.addTTL('CAMERA',loading_time+wait_time+WithUnit(50,'ms'),WithUnit(3,'ms'))
        self.addTTL('CAMERA',loading_time+wait_time+WithUnit(100,'ms'),WithUnit(3,'ms'))
        


