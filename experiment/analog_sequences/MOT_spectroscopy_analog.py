from servers.pulser.pulse_sequences.analog_sequence import analog_sequence
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_spectroscopy_analog(analog_sequence):
    
    required_parameters = [('MOT_loading', 'loading_time'),
                           ('MOT_loading', 'B_x'),
                           ('MOT_loading', 'B_y'),
                           ('MOT_loading', 'B_z'),
                           ('MOT_loading', 'B_x_det'),
                           ('MOT_loading', 'B_y_det'),
                           ('MOT_loading', 'B_z_det'),
                           ('MOT_loading', 'wait_time'),
                           ('MOT_loading', 'MOT_current_compress'),
                           ('Clock', 'B_x_clock'),
                           ('Clock', 'B_y_clock'),
                           ('Clock', 'B_z_clock'),
                           ('Clock', 'SP1_freq'),
                           ]
#     
    required_subsequences = []
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        p = self.parameters
        #self.end = WithUnit(10, 'us')

        self.end = self.start+p.MOT_loading.wait_time
        #print self.end
        #print self.start
        
        detect_freq = -0.2
        blue_freq = -0.9
        MOT_intensity = 1.2
        
        B_x_clock = p.Clock.B_x_clock
        B_y_clock = p.Clock.B_y_clock
        B_z_clock = p.Clock.B_z_clock
        
        B_x_det = p.MOT_loading.B_x_det
        B_y_det = p.MOT_loading.B_y_det
        B_z_det = p.MOT_loading.B_z_det
        
        ## MOT AO frequency is channel 0
        
        SP1_freq = p.Clock.SP1_freq
        
        self.addAnalog(0, self.start+WithUnit(2,'ms'), SP1_freq)
        self.addAnalog(0, self.end-WithUnit(2,'ms'), SP1_freq)
        
        ### B field
        
        time_before_detect = WithUnit(32, 'ms')
        
        self.addAnalog(2, self.start+WithUnit(2,'ms'), B_x_clock)
        self.addAnalog(2, self.end-time_before_detect, B_x_clock)
        self.addAnalog(2, self.end-time_before_detect + WithUnit(2,'ms'), B_x_det)
        self.addAnalog(3, self.start+WithUnit(2,'ms'), B_y_clock)
        self.addAnalog(3, self.end-time_before_detect, B_y_clock)
        self.addAnalog(3, self.end-time_before_detect + WithUnit(2,'ms'), B_y_det)
        self.addAnalog(4, self.start+WithUnit(2,'ms'), B_z_clock)
        self.addAnalog(4, self.end-time_before_detect, B_z_clock)
        self.addAnalog(4, self.end-time_before_detect + WithUnit(2,'ms'), B_z_det)
        
        ### MOT_AO intensity
        
        self.addAnalog(1, self.start+WithUnit(2,'ms'), MOT_intensity)
        self.addAnalog(1, self.end-WithUnit(2,'ms'), MOT_intensity)
        
        ## MOT coil
        self.addAnalog(5, self.start+WithUnit(2,'ms'), 0.0)
        self.addAnalog(5, self.end-time_before_detect, 0.0)
        self.addAnalog(5, self.end-time_before_detect + WithUnit(2,'ms'), p.MOT_loading.MOT_current_compress)
        
        ### Lattice
        self.addAnalog(6, self.start+WithUnit(2,'ms'), -1.0)
        self.addAnalog(6, self.start+WithUnit(12,'ms'), -1.0)
        self.addAnalog(6, self.start+WithUnit(15,'ms'), -1.3)
        self.addAnalog(6, self.end-WithUnit(3,'ms'), -1.3)
        
        ### clock
        self.addAnalog(7, self.start+WithUnit(2,'ms'), 10.0)
        self.addAnalog(7, self.end-WithUnit(2,'ms'), 10.0)
        

if __name__ == '__main__':
    print "hey world"
    import labrad
    cxn = labrad.connect()
    ni = cxn.ni_analog_server
    M = MOT_spectroscopy_analog(TreeDict())
    #M.sequence()
    #M.convert_sequence()
    M.programAnalog(ni)
