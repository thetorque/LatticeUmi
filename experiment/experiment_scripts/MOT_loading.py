from servers.script_scanner.scan_methods import experiment
from experiment.pulser_sequences.MOT_loading_test import MOT_loading
from labrad.units import WithUnit
import labrad
import numpy
import time
from datetime import datetime
import matplotlib.pyplot as plt
       
class MOT_loading(experiment):
    name = 'MOT loading'  
    excitation_required_parameters = []
    pulse_sequence = MOT_loading
    
    @classmethod
    def all_required_parameters(cls):
        params = set(cls.excitation_required_parameters)
        params = params.union(set(cls.pulse_sequence.all_required_parameters()))
        params = list(params)
        return params
    
    def initialize(self, cxn, context, ident):
        self.pulser = cxn.pulser
#         self.drift_tracker = cxn.sd_tracker
        self.dv = cxn.data_vault
#        self.total_readouts = []
        self.readout_save_context = cxn.context()
#        self.histogram_save_context = cxn.context()
#        self.readout_save_iteration = 0
#         self.setup_sequence_parameters()
#         self.setup_initial_switches()
        self.setup_data_vault()
#         self.use_camera = self.parameters.StateReadout.use_camera_for_readout
#        self.use_camera = True
#        if self.use_camera:
        self.initialize_camera(cxn)
            
    def initialize_camera(self, cxn):
        self.total_camera_confidences = []
#        p = self.parameters.IonsOnCamera
#        from lmfit import Parameters as lmfit_Parameters
        self.camera = cxn.andor_server
#         self.fitter = ion_state_detector(int(p.ion_number))
        self.camera_initially_live_display = self.camera.is_live_display_running()
        self.camera.abort_acquisition()
#         self.initial_exposure = self.camera.get_exposure_time()
#         exposure = self.parameters.StateReadout.state_readout_duration
#         self.camera.set_exposure_time(exposure)
#         self.initial_region = self.camera.get_image_region()
#         self.image_region = [
#                              int(p.horizontal_bin),
#                              int(p.vertical_bin),
#                              int(p.horizontal_min),
#                              int(p.horizontal_max),
#                              int(p.vertical_min),
#                              int(p.vertical_max),
#                              ]
        self.image_region = [
                             2,
                             2,
                             326,
                             359,
                             240,
                             271,
                             ]

#         self.fit_parameters = lmfit_Parameters()
#         self.fit_parameters.add('ion_number', value = int(p.ion_number))
#         self.fit_parameters.add('background_level', value = p.fit_background_level)
#         self.fit_parameters.add('amplitude', value = p.fit_amplitude)
#         self.fit_parameters.add('rotation_angle', p.fit_rotation_angle)
#         self.fit_parameters.add('center_x', value = p.fit_center_horizontal)
#         self.fit_parameters.add('center_y', value = p.fit_center_vertical)
#         self.fit_parameters.add('spacing', value = p.fit_spacing)
#         self.fit_parameters.add('sigma', value = p.fit_sigma)
#         x_axis = numpy.arange(self.image_region[2], self.image_region[3] + 1, self.image_region[0])
#         y_axis = numpy.arange(self.image_region[4], self.image_region[5] + 1, self.image_region[1])
#         xx,yy = numpy.meshgrid(x_axis, y_axis)
#         self.fitter.set_fitted_parameters(self.fit_parameters, xx, yy)
        self.camera.set_image_region(*self.image_region)
        self.camera.set_acquisition_mode('Kinetics')
        self.initial_trigger_mode = self.camera.get_trigger_mode()
        self.camera.set_trigger_mode('External')
        
    def setup_data_vault(self):
        localtime = time.localtime()
        self.datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        self.save_directory = ['','Experiments']
        self.save_directory.extend([self.name])
        self.save_directory.extend(dirappend)
        self.dv.cd(self.save_directory ,True, context = self.readout_save_context)
        self.dv.new('MOT {}'.format(self.datasetNameAppend),[('Time', 'Sec')],[('S_state','S_state.','No.'),('P_state','P_state.','No.'),('BG','BG','No.')], context = self.readout_save_context)   
        self.dv.add_parameter('Window', ['MOT population'], context = self.readout_save_context)     
        self.dv.add_parameter('plotLive', True, context = self.readout_save_context)     
        
    
#     def setup_sequence_parameters(self):
#         op = self.parameters.OpticalPumping
#         optical_pumping_frequency = cm.frequency_from_line_selection(op.frequency_selection, op.manual_frequency_729, op.line_selection, self.drift_tracker, op.optical_pumping_enable)
#         self.parameters['OpticalPumping.optical_pumping_frequency_729'] = optical_pumping_frequency
#         aux = self.parameters.OpticalPumpingAux
#         aux_optical_pumping_frequency = cm.frequency_from_line_selection('auto', WithUnit(0,'MHz'),  aux.aux_op_line_selection, self.drift_tracker, aux.aux_op_enable)
#         self.parameters['OpticalPumpingAux.aux_optical_frequency_729'] = aux_optical_pumping_frequency
#         sc = self.parameters.SidebandCooling
#         sideband_cooling_frequency = cm.frequency_from_line_selection(sc.frequency_selection, sc.manual_frequency_729, sc.line_selection, self.drift_tracker, sc.sideband_cooling_enable)
#         if sc.frequency_selection == 'auto': 
#             trap = self.parameters.TrapFrequencies
#             sideband_cooling_frequency = cm.add_sidebands(sideband_cooling_frequency, sc.sideband_selection, trap)
#         self.parameters['SidebandCooling.sideband_cooling_frequency_729'] = sideband_cooling_frequency
    
#     def setup_initial_switches(self):
#         self.pulser.switch_manual('crystallization',  False)
#         #switch off 729 at the beginning
#         self.pulser.output('729DP', False)
    
#     def plot_current_sequence(self, cxn):
#         from common.okfpgaservers.pulser.pulse_sequences.plot_sequence import SequencePlotter
#         dds = cxn.pulser.human_readable_dds()
#         ttl = cxn.pulser.human_readable_ttl()
#         channels = cxn.pulser.get_channels().asarray
#         sp = SequencePlotter(ttl.asarray, dds.aslist, channels)
#         sp.makePlot()
        
    def run(self, cxn, context):
#         threshold = int(self.parameters.StateReadout.state_readout_threshold)
#         repetitions = int(self.parameters.StateReadout.repeat_each_measurement)
        print "running"
        repetitions = 3;
        
        pulse_sequence = self.pulse_sequence(self.parameters)
        pulse_sequence.programSequence(self.pulser)
#         self.plot_current_sequence(cxn)
        #if self.use_camera:
            #print 'starting acquisition'
        self.camera.set_number_kinetics(3)
        self.camera.start_acquisition()
        
        
        ### get no. of second of today
        now = datetime.now()
        start_time = (now-now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
        
        self.pulser.start_number(1)
        self.pulser.wait_sequence_done()
        self.pulser.stop_sequence()
#        if not self.use_camera:
            #get percentage of the excitation using the PMT threshold
#             readouts = self.pulser.get_readout_counts().asarray
#             self.save_data(readouts)            
#             if len(readouts):
#                 perc_excited = numpy.count_nonzero(readouts <= threshold) / float(len(readouts))
#             else:
#                 #got no readouts
#                 perc_excited = -1.0
#             ion_state = [perc_excited]
# #             print readouts
#            pass
#        else:
            #get the percentage of excitation using the camera state readout
        proceed = self.camera.wait_for_kinetic()
        if not proceed:
            self.camera.abort_acquisition()
            self.finalize(cxn, context)
            raise Exception ("Did not get all kinetic images from camera")
        images = self.camera.get_acquired_data(repetitions).asarray
        #print images
        self.camera.abort_acquisition()
        x_pixels = int( (self.image_region[3] - self.image_region[2] + 1.) / (self.image_region[0]) )
        y_pixels = int(self.image_region[5] - self.image_region[4] + 1.) / (self.image_region[1])
        images = numpy.reshape(images, (repetitions, y_pixels, x_pixels))
        
        S_state = numpy.sum(images[0])
        P_state = numpy.sum(images[1])
        Background = numpy.sum(images[2])
        
        Atom_number_data = numpy.array([start_time,S_state,P_state,Background])
        print Atom_number_data
        
        self.dv.add(Atom_number_data, context = self.readout_save_context)
#         print images
#         plt.imshow(images[2])
#         plt.show()
#             readouts, confidences = self.fitter.state_detection(images)
            #ion_state = 1 - readouts.mean(axis = 0)
            #useful for debugging, saving the images
#             numpy.save('readout {}'.format(int(time.time())), images)
#             self.save_confidences(confidences)
        #return ion_state, readouts
    
#     @property
#     def output_size(self):
#         if self.use_camera:
#             return int(self.parameters.IonsOnCamera.ion_number)
#         else:
#             return 1
    
    def finalize(self, cxn, context):
        self.camera.start_live_display()
#         if self.use_camera:
#             #if used the camera, return it to the original settings
#             #self.camera.set_trigger_mode(self.initial_trigger_mode)
#             #self.camera.set_exposure_time(self.initial_exposure)
#             #self.camera.set_image_region(self.initial_region)
#             if self.camera_initially_live_display:
#                 self.camera.start_live_display()
#                
#     def save_data(self, readouts):
#         #save the current readouts
#         iters = numpy.ones_like(readouts) * self.readout_save_iteration
#         self.dv.add(numpy.vstack((iters, readouts)).transpose(), context = self.readout_save_context)
#         self.readout_save_iteration += 1
#         self.total_readouts.extend(readouts)
#         if (len(self.total_readouts) >= 500):
#             hist, bins = numpy.histogram(self.total_readouts, 50)
#             self.dv.cd(self.save_directory ,True, context = self.histogram_save_context)
#             self.dv.new('Histogram {}'.format(self.datasetNameAppend),[('Counts', 'Arb')],[('Occurence','Arb','Arb')], context = self.histogram_save_context )
#             self.dv.add(numpy.vstack((bins[0:-1],hist)).transpose(), context = self.histogram_save_context )
#             self.dv.add_parameter('Histogram729', True, context = self.histogram_save_context )
#             self.total_readouts = []
    
#     def save_confidences(self, confidences):
#         '''
#         saves confidences readings for the camera state detection
#         '''
#         self.total_camera_confidences.extend(confidences)
#         if (len(self.total_camera_confidences) >= 300):
#             hist, bins = numpy.histogram(self.total_camera_confidences, 30)
#             self.dv.cd(self.save_directory ,True, context = self.histogram_save_context)
#             self.dv.new('Histogram Camera {}'.format(self.datasetNameAppend),[('Counts', 'Arb')],[('Occurence','Arb','Arb')], context = self.histogram_save_context )
#             self.dv.add(numpy.vstack((bins[0:-1],hist)).transpose(), context = self.histogram_save_context )
#             self.dv.add_parameter('HistogramCameraConfidence', True, context = self.histogram_save_context )
#             self.total_camera_confidences = []

if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = MOT_loading(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)