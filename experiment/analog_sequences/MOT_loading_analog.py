from servers.pulser.pulse_sequences.analog_sequence import analog_sequence
from experiment.analog_sequences.MOT_detection_analog import MOT_detection_analog
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_loading_seq(analog_sequence):
    
    required_parameters = []
#     
    required_subsequences = [MOT_detection_analog]
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        #p = self.parameters
        #self.end = WithUnit(10, 'us')
        
        '''
        
        sequence rule 
        1.) start and stop voltage for each channel must be the same
        2.) start and stop time for each channel must be the same and defines the sequence length
        3.) cleverly initiate points with loading configuration. Look up in parameter vault
        
        '''

        self.end = WithUnit(3.2,'ms')
        
        #trigger analog out
        self.addAnalog(0, WithUnit(0.0,'ms'), 1.0)
        self.addAnalog(1, WithUnit(0.0,'ms'), 2.0)
        self.addAnalog(2, WithUnit(0.0,'ms'), 2.0)
        self.addAnalog(3, WithUnit(0.0,'ms'), 2.0)
        self.addAnalog(4, WithUnit(0.0,'ms'), 2.0)
        self.addAnalog(5, WithUnit(0.0,'ms'), 2.0)
        self.addAnalog(6, WithUnit(0.0,'ms'), 2.0)
        self.addAnalog(7, WithUnit(0.0,'ms'), 2.0)
        
        self.addAnalog(0, WithUnit(0.5,'s'), 1.5)
        
        #self.addSequence(MOT_detection_analog)
        
        self.addAnalog(0, WithUnit(1.5,'s'), 2.0)
        self.addAnalog(1, WithUnit(1.5,'s'), 2.0)
        self.addAnalog(1, WithUnit(1.5,'s'), 2.0)
        self.addAnalog(2, WithUnit(1.5,'s'), 2.0)
        self.addAnalog(3, WithUnit(1.5,'s'), 2.0)
        self.addAnalog(4, WithUnit(1.5,'s'), 2.0)
        self.addAnalog(5, WithUnit(1.5,'s'), 2.0)
        self.addAnalog(6, WithUnit(1.5,'s'), 2.0)
        self.addAnalog(7, WithUnit(1.5,'s'), 2.0)
        

if __name__ == '__main__':
    print "hey world"
    import labrad
    cxn = labrad.connect()
    ni = cxn.ni_analog_server
    M = MOT_loading_seq(TreeDict())
    #M.sequence()
    #M.convert_sequence()
    M.programAnalog(ni)
