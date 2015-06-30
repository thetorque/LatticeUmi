from servers.pulser.pulse_sequences.analog_sequence import analog_sequence
from labrad.units import WithUnit
from treedict import TreeDict

class MOT_detection_analog(analog_sequence):
    
    required_parameters = [('MOT_loading', 'B_x_det'),
                           ('MOT_loading', 'B_x'),
                           ('MOT_loading', 'B_y_det'),
                           ('MOT_loading', 'B_y'),
                           ('MOT_loading', 'B_z_det'),
                           ('MOT_loading', 'B_z'),
                           ('MOT_loading', 'MOT_current_load'),
                           ('MOT_loading', 'MOT_current_compress'),
                           ]
#     
    required_subsequences = []
#     
#     replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration')]
#                            }

    def sequence(self):
        p = self.parameters
        #self.end = WithUnit(10, 'us')

        self.end = self.start + WithUnit(139,'ms') + WithUnit(0.1,'ms')
        
        detect_freq = -0.2
        blue_freq = -0.9
        MOT_intensity = 1.2
        B_x_det = p.MOT_loading.B_x_det
        B_y_det = p.MOT_loading.B_y_det
        B_z_det = p.MOT_loading.B_z_det
        
        B_x = p.MOT_loading.B_x
        B_y = p.MOT_loading.B_y
        B_z = p.MOT_loading.B_z
        
        ## MOT AO frequency is channel 0
        
        self.addAnalog(0, self.start+WithUnit(0.1,'ms'), detect_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(30,'ms'), detect_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(33,'ms'), blue_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(36,'ms'), blue_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(39,'ms'), detect_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(80,'ms'), detect_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(83,'ms'), blue_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(86,'ms'), blue_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(89,'ms'), detect_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(130,'ms'), detect_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(133,'ms'), blue_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(136,'ms'), blue_freq)
        self.addAnalog(0, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), detect_freq)
        
        ### B field
        
        self.addAnalog(2, self.start+WithUnit(0.1,'ms'), B_x_det)
        self.addAnalog(2, self.start+WithUnit(0.1,'ms')+WithUnit(133,'ms'), B_x_det)
        self.addAnalog(2, self.start+WithUnit(0.1,'ms')+WithUnit(136,'ms'), B_x)
        self.addAnalog(2, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), B_x)
        self.addAnalog(3, self.start+WithUnit(0.1,'ms'), B_y_det)
        self.addAnalog(3, self.start+WithUnit(0.1,'ms')+WithUnit(133,'ms'), B_y_det)
        self.addAnalog(3, self.start+WithUnit(0.1,'ms')+WithUnit(136,'ms'), B_y)
        self.addAnalog(3, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), B_y)
        self.addAnalog(4, self.start+WithUnit(0.1,'ms'), B_z_det)
        self.addAnalog(4, self.start+WithUnit(0.1,'ms')+WithUnit(133,'ms'), B_z_det)
        self.addAnalog(4, self.start+WithUnit(0.1,'ms')+WithUnit(136,'ms'), B_z)
        self.addAnalog(4, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), B_z)
        
        ### MOT_AO intensity
        
        self.addAnalog(1, self.start+WithUnit(0.1,'ms'), MOT_intensity)
        self.addAnalog(1, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), MOT_intensity)
        
        ## MOT coil
        
        load_current = p.MOT_loading.MOT_current_load
        compress_current = p.MOT_loading.MOT_current_compress
        
        self.addAnalog(5, self.start+WithUnit(0.1,'ms'), compress_current)
        self.addAnalog(5, self.start+WithUnit(0.1,'ms')+WithUnit(130,'ms'), compress_current) #8.0
        self.addAnalog(5, self.start+WithUnit(0.1,'ms')+WithUnit(133,'ms'), load_current)
        self.addAnalog(5, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), load_current) #4.5
        
        
        
        self.addAnalog(6, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), 0.0)
        self.addAnalog(7, self.start+WithUnit(0.1,'ms')+WithUnit(139,'ms'), 10.0)
        
