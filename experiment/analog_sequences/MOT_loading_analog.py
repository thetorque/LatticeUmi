from servers.pulser.pulse_sequences.analog_sequence import analog_sequence
from experiment.analog_sequences.MOT_detection_analog import MOT_detection_analog
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_loading_analog(analog_sequence):
    
    required_parameters = [('MOT_loading', 'loading_time'),
                           ('MOT_loading', 'compress_time'),
                           ('MOT_loading', 'B_x'),
                           ('MOT_loading', 'B_y'),
                           ('MOT_loading', 'B_z'),
                           ('MOT_loading', 'MOT_intensity'),
                           ]
#     
    required_subsequences = [MOT_detection_analog]
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        p = self.parameters
        #self.end = WithUnit(10, 'us')
        
        '''
        
        sequence rule 
        1.) start and stop voltage for each channel must be the same
        2.) start and stop time for each channel must be the same and defines the sequence length
        3.) cleverly initiate points with loading configuration. Look up in parameter vault
        
        '''
        
        print p.MOT_loading.loading_time
        
        ###B_field###
        B_x = p.MOT_loading.B_x
        B_y = p.MOT_loading.B_y
        B_z = p.MOT_loading.B_z
        
        
        
        self.addAnalog(2, WithUnit(0.0,'ms'), B_x)
        self.addAnalog(2, p.MOT_loading.loading_time-WithUnit(0.1,'ms'), B_x)
        self.addAnalog(3, WithUnit(0.0,'ms'), B_y)
        self.addAnalog(3, p.MOT_loading.loading_time-WithUnit(0.1,'ms'), B_y)
        self.addAnalog(4, WithUnit(0.0,'ms'), B_z)
        self.addAnalog(4, p.MOT_loading.loading_time-WithUnit(0.1,'ms'), B_z)
        
        #### MOT intensity
        
        MOT_intensity = p.MOT_loading.MOT_intensity
        
        self.addAnalog(1, WithUnit(0.0,'ms'), MOT_intensity)
        self.addAnalog(1, p.MOT_loading.loading_time-WithUnit(0.1,'ms'), MOT_intensity)
        

        

        self.addAnalog(5, WithUnit(0.0,'ms'), 0.0)
        self.addAnalog(6, WithUnit(0.0,'ms'), 0.0)
        self.addAnalog(7, WithUnit(0.0,'ms'), 0.0)
        
        
        ### MOT frequency
        
        self.addAnalog(0, WithUnit(0.0,'ms'), -0.2)
        self.addAnalog(0, WithUnit(3.0,'ms'), -0.2)
        self.addAnalog(0, WithUnit(4.0,'ms'), 0.8)
        self.addAnalog(0, p.MOT_loading.loading_time-WithUnit(60.0,'ms'), 0.8)
        self.addAnalog(0, p.MOT_loading.loading_time-WithUnit(60.0,'ms')+WithUnit(3.0,'ms'), -0.2)
        self.addAnalog(0, p.MOT_loading.loading_time-WithUnit(0.1,'ms'), -0.2)
        
        self.end = p.MOT_loading.loading_time
        
        self.addSequence(MOT_detection_analog)
        

if __name__ == '__main__':
    print "hey world"
    import labrad
    cxn = labrad.connect()
    ni = cxn.ni_analog_server
    M = MOT_loading_analog(TreeDict())
    #M.sequence()
    #M.convert_sequence()
    M.programAnalog(ni)