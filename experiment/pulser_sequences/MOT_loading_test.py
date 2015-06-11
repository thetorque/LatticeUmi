from servers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from subsequences.RepumpDwithDoppler import doppler_cooling_after_repump_d
from subsequences.EmptySequence import empty_sequence
from subsequences.OpticalPumping import optical_pumping
from subsequences.RabiExcitation import rabi_excitation
from subsequences.Tomography import tomography_readout
from subsequences.TurnOffAll import turn_off_all
from subsequences.SidebandCooling import sideband_cooling
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_loading(pulse_sequence):
    
    required_parameters = [ 
                           ('MOT_loading', 'loading_time'),
                           ]
#     
#     required_subsequences = [doppler_cooling_after_repump_d, empty_sequence, optical_pumping, 
#                              rabi_excitation, tomography_readout, turn_off_all, sideband_cooling]
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
        #('DDS_0', offset, duration, WithUnit(100.0, 'MHz'), WithUnit(-63,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        #self.addDDS('DDS_0',WithUnit(10,'us'),WithUnit(1.0,'s'),WithUnit(100.0,'MHz'),WithUnit(-20,'dBm'))
        #self.addDDS('DDS_0',WithUnit(1.01,'s'),WithUnit(200.0,'ms'),WithUnit(60.0,'MHz'),WithUnit(-20,'dBm'))
        
        #Big MOT light on
        self.addTTL('BIG_MOT_SH',WithUnit(10,'us'),WithUnit(1.5,'s'))
        self.addDDS('BIG_MOT',WithUnit(10,'us'),WithUnit(1.5,'s'),MOT_freq,WithUnit(-5,'dBm'))
        
        #254 comb
        
        far_red_detuned_time = p.MOT_loading.loading_time-WithUnit(300.0,'ms')-WithUnit(10.0,'us')
        
        self.addDDS('254_COMB',WithUnit(10.0,'us'),far_red_detuned_time, WithUnit(10.5,'MHz'),comb_amp,no_phase,WithUnit(0.01,'MHz'),no_amp_ramp)
        self.addDDS('254_COMB',WithUnit(700.0,'ms'),WithUnit(300.0,'ms'),WithUnit(9.0,'MHz'),comb_amp,no_phase,WithUnit(0.01,'MHz'),no_amp_ramp)
        ### detection ###
        self.addDDS('254_COMB',WithUnit(1.000,'s'),WithUnit(25,'ms'),WithUnit(9.0,'MHz'),comb_amp)
        self.addDDS('254_COMB',WithUnit(1.025,'s'),WithUnit(25,'ms'),WithUnit(8.0,'MHz'),comb_amp,no_phase,WithUnit(0.1,'MHz'),no_amp_ramp)
        self.addDDS('254_COMB',WithUnit(1.050,'s'),WithUnit(25,'ms'),WithUnit(9.0,'MHz'),comb_amp,no_phase,WithUnit(0.1,'MHz'),no_amp_ramp)
        self.addDDS('254_COMB',WithUnit(1.075,'s'),WithUnit(25,'ms'),WithUnit(8.0,'MHz'),comb_amp,no_phase,WithUnit(0.1,'MHz'),no_amp_ramp)
        self.addDDS('254_COMB',WithUnit(1.100,'s'),WithUnit(345,'ms'),WithUnit(9.0,'MHz'),comb_amp,no_phase,WithUnit(0.1,'MHz'),no_amp_ramp)
#         self.addDDS('254_COMB',WithUnit(1.025,'s'),WithUnit(25,'ms'),WithUnit(8.0,'MHz'),comb_amp)
#         self.addDDS('254_COMB',WithUnit(1.050,'s'),WithUnit(25,'ms'),WithUnit(9.2,'MHz'),comb_amp)
#         self.addDDS('254_COMB',WithUnit(1.075,'s'),WithUnit(25,'ms'),WithUnit(8.0,'MHz'),comb_amp)
#         self.addDDS('254_COMB',WithUnit(1.100,'s'),WithUnit(345,'ms'),WithUnit(9.2,'MHz'),comb_amp)
        #trigger analog out
        self.addTTL('AO1',WithUnit(10,'us'),WithUnit(1,'ms'))
        self.addTTL('AO2',WithUnit(10,'us'),WithUnit(1,'ms'))
        
        #trigger camera
        self.addTTL('CAMERA',WithUnit(1000,'ms'),WithUnit(3,'ms'))
        self.addTTL('CAMERA',WithUnit(1050,'ms'),WithUnit(3,'ms'))
        self.addTTL('CAMERA',WithUnit(1100,'ms'),WithUnit(3,'ms'))
        
#         self.addTTL('ttl_1',WithUnit(10,'ms'),WithUnit(250,'ms'))
#         self.addTTL('ttl_1',WithUnit(500,'ms'),WithUnit(250,'ms'))
#         self.addTTL('ttl_1',WithUnit(1000,'ms'),WithUnit(500,'ms'))
