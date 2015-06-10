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
    
#     required_parameters = [ 
#                            ('Heating', 'background_heating_time'),
#                            ('OpticalPumping','optical_pumping_enable'), 
#                            ('SidebandCooling','sideband_cooling_enable'),
#                            ]
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
        no_freq_ramp = WithUnit(0,'MHz')
        no_phase = WithUnit(0.0,'deg')
        #('DDS_0', offset, duration, WithUnit(100.0, 'MHz'), WithUnit(-63,'dBm'), WithUnit(0.0,'deg'),WithUnit(0.0, 'MHz'),no_amp_ramp),
        self.addDDS('DDS_0',WithUnit(10,'us'),WithUnit(1.0,'s'),WithUnit(100.0,'MHz'),WithUnit(-20,'dBm'))
        self.addDDS('DDS_0',WithUnit(1.01,'s'),WithUnit(700.0,'ms'),WithUnit(60.0,'MHz'),WithUnit(-20,'dBm'))
        
        #trigger analog out
        self.addTTL('AO1',WithUnit(10,'us'),WithUnit(100,'ms'))
        self.addTTL('AO1',WithUnit(200,'ms'),WithUnit(100,'ms'))
        self.addTTL('AO2',WithUnit(10,'us'),WithUnit(100,'ms'))
        self.addTTL('AO2',WithUnit(200,'ms'),WithUnit(100,'ms'))
        
        #trigger camera
        self.addTTL('ttl_0',WithUnit(1000,'ms'),WithUnit(3,'ms'))
        self.addTTL('ttl_0',WithUnit(1050,'ms'),WithUnit(3,'ms'))
        self.addTTL('ttl_0',WithUnit(1100,'ms'),WithUnit(3,'ms'))
        
        self.addTTL('ttl_1',WithUnit(10,'ms'),WithUnit(250,'ms'))
        self.addTTL('ttl_1',WithUnit(500,'ms'),WithUnit(250,'ms'))
        self.addTTL('ttl_1',WithUnit(1000,'ms'),WithUnit(500,'ms'))
