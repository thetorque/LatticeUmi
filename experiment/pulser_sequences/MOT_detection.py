from servers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_detection(pulse_sequence):
    
    required_parameters = [ 
                           ('MOT_loading', 'detection_frequency'),
                           ('MOT_loading', 'blue_detuned_frequency'),
                           ('MOT_loading', 'detection_power'),
                           ]
#     
#     required_subsequences = [doppler_cooling_after_repump_d, empty_sequence, optical_pumping, 
#                              rabi_excitation, tomography_readout, turn_off_all, sideband_cooling]
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        p = self.parameters
        
        no_amp_ramp = WithUnit(0,'dB')
        comb_amp = WithUnit(4.0,'dBm')
        MOT_freq = WithUnit(150.0,'MHz')
        no_freq_ramp = WithUnit(0,'MHz')
        no_phase = WithUnit(0.0,'deg')
        
        ### detection ###
        
        freq_detect = p.MOT_loading.detection_frequency
        freq_blue = p.MOT_loading.blue_detuned_frequency
        detection_power = p.MOT_loading.detection_power
        
        self.end = self.start + WithUnit(225,'ms')
        
        self.addTTL('sMOT_PROBE',      self.start, WithUnit(150,'ms'))
        self.addTTL('sMOT_PROBE_SPIN', self.start, WithUnit(150,'ms'))
        
        self.addDDS('SMALL_MOT',self.start,                    WithUnit(40,'ms'), MOT_freq, detection_power)
        self.addDDS('SMALL_MOT',self.start+WithUnit(50,'ms'),  WithUnit(40,'ms'), MOT_freq, detection_power)
        self.addDDS('SMALL_MOT',self.start+WithUnit(100,'ms'), WithUnit(40,'ms'), MOT_freq, detection_power)
        
        #print self.start
        
        self.addDDS('254_COMB',self.start,                    WithUnit(25,'ms'),  freq_detect, comb_amp)
        self.addDDS('254_COMB',self.start+WithUnit(25,'ms'),  WithUnit(25,'ms'),  freq_blue,   comb_amp, no_phase, WithUnit(0.1,'MHz'),no_amp_ramp)
        self.addDDS('254_COMB',self.start+WithUnit(50,'ms'),  WithUnit(25,'ms'),  freq_detect, comb_amp, no_phase, WithUnit(0.1,'MHz'),no_amp_ramp)
        self.addDDS('254_COMB',self.start+WithUnit(75,'ms'),  WithUnit(25,'ms'),  freq_blue,   comb_amp, no_phase, WithUnit(0.1,'MHz'),no_amp_ramp)
        self.addDDS('254_COMB',self.start+WithUnit(100,'ms'), WithUnit(125,'ms'), freq_detect, comb_amp, no_phase, WithUnit(0.1,'MHz'),no_amp_ramp)
#         self.addDDS('254_COMB',WithUnit(1.025,'s'),WithUnit(25,'ms'),WithUnit(8.0,'MHz'),comb_amp)
#         self.addDDS('254_COMB',WithUnit(1.050,'s'),WithUnit(25,'ms'),WithUnit(9.2,'MHz'),comb_amp)
#         self.addDDS('254_COMB',WithUnit(1.075,'s'),WithUnit(25,'ms'),WithUnit(8.0,'MHz'),comb_amp)
#         self.addDDS('254_COMB',WithUnit(1.100,'s'),WithUnit(345,'ms'),WithUnit(9.2,'MHz'),comb_amp)
        #trigger analog out

        
        #trigger camera
        self.addTTL('CAMERA',self.start,                    WithUnit(3,'ms'))
        self.addTTL('CAMERA',self.start+WithUnit(50,'ms'),  WithUnit(3,'ms'))
        self.addTTL('CAMERA',self.start+WithUnit(100,'ms'), WithUnit(3,'ms'))
        
#         self.addTTL('ttl_1',WithUnit(10,'ms'),WithUnit(250,'ms'))
#         self.addTTL('ttl_1',WithUnit(500,'ms'),WithUnit(250,'ms'))
#         self.addTTL('ttl_1',WithUnit(1000,'ms'),WithUnit(500,'ms'))
