from servers.pulser.pulse_sequences.analog_sequence import analog_sequence
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_detection_analog(analog_sequence):
    
    required_parameters = []
#     
    required_subsequences = []
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        #p = self.parameters
        #self.end = WithUnit(10, 'us')

        self.end = self.start + WithUnit(1000,'ms')
        
        #trigger analog out
        self.addAnalog(0, self.start+WithUnit(10.0,'ms'), 3.0)
        self.addAnalog(1, self.start*2+WithUnit(10.0,'ms'), 3.0)
