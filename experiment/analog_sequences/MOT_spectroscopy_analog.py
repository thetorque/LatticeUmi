from servers.pulser.pulse_sequences.analog_sequence import analog_sequence
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_spectroscopy_analog(analog_sequence):
    
    required_parameters = [('MOT_loading', 'loading_time'),
                           ('MOT_loading', 'compress_time'),
                           ('MOT_loading', 'B_x'),
                           ('MOT_loading', 'B_y'),
                           ('MOT_loading', 'B_z'),
                           ('MOT_loading', 'wait_time'),
                           ('Clock', 'B_x_clock'),
                           ('Clock', 'B_y_clock'),
                           ('Clock', 'B_z_clock'),
                           ]
#     
    required_subsequences = []
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        p = self.parameters
        #self.end = WithUnit(10, 'us')

        self.end = self.start +p.MOT_loading.wait_time
        
        detect_freq = -0.2
        blue_freq = -0.9
        MOT_intensity = 1.2
        
        B_x_clock = p.Clock.B_x_clock
        B_y_clock = p.Clock.B_y_clock
        B_z_clock = p.Clock.B_z_clock
        
        ## MOT AO frequency is channel 0
        
        self.addAnalog(0, self.start+WithUnit(0.1,'ms'), detect_freq)
        self.addAnalog(0, self.end-WithUnit(0.1,'ms'), detect_freq)
        
        ### B field
        
        self.addAnalog(2, self.start+WithUnit(0.1,'ms'), B_x_clock)
        self.addAnalog(2, self.end-WithUnit(0.1,'ms'), B_x_clock)
        self.addAnalog(3, self.start+WithUnit(0.1,'ms'), B_y_clock)
        self.addAnalog(3, self.end-WithUnit(0.1,'ms'), B_y_clock)
        self.addAnalog(4, self.start+WithUnit(0.1,'ms'), B_z_clock)
        self.addAnalog(4, self.end-WithUnit(0.1,'ms'), B_z_clock)
        
        ### MOT_AO intensity
        
        self.addAnalog(1, self.start+WithUnit(0.1,'ms'), MOT_intensity)
        self.addAnalog(1, self.end-WithUnit(0.1,'ms'), MOT_intensity)
        
        ## MOT coil
        self.addAnalog(0, self.start+WithUnit(0.1,'ms'), 0.0)
        self.addAnalog(0, self.end-WithUnit(0.1,'ms'), 0.0)
        
        ### Lattice
        self.addAnalog(6, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), 0.0)
        
        ### clock
        self.addAnalog(7, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), 10.0)
        

if __name__ == '__main__':
    print "hey world"
    import labrad
    cxn = labrad.connect()
    ni = cxn.ni_analog_server
    M = MOT_spectroscopy_analog(TreeDict())
    #M.sequence()
    #M.convert_sequence()
    M.programAnalog(ni)
