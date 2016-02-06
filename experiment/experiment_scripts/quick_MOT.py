from servers.script_scanner.scan_methods import experiment
#from experiment.pulser_sequences.MOT_loading_seq import MOT_loading_seq
from experiment.experiment_scripts.MOT_loading import MOT_loading

from labrad.units import WithUnit
import labrad
import numpy
import time
from datetime import datetime

'''
Template for the experiment. By Hong.
'''
'''
This experiment implement a quick MOT setting that we always use to monitor the MOT population
'''    
       
class quick_MOT(experiment):
    ##name of the experiment to be shown in the scriptscanner
    name = 'quick_MOT'  
    experiment_required_parameters = []

    
    @classmethod
    def all_required_parameters(cls):
        '''
        take the required parameters for both pulse sequence and analog sequence and union into a total list of require parameters for this experiment
        '''
        params = set(cls.experiment_required_parameters)
        params = params.union(set(MOT_loading.all_required_parameters()))
        #params = params.union(set(cls.analog_sequence.all_required_parameters()))
        params = list(params)
        
        ### remove parameter that we are scanning
        params.remove(('CCD_settings','binning'))
        params.remove(('CCD_settings','EMCCD_gain'))
        params.remove(('CCD_settings','exposure_time'))
        params.remove(('MOT_loading','loading_time'))
        
        return params
    
    def initialize(self, cxn, context, ident):
        '''
        initialization: list all the servers we need to talk to
        '''
        self.pulser = cxn.pulser ## pulse sequence server
        self.NI_analog = cxn.ni_analog_server ## analog sequence server
        self.dv = cxn.data_vault ## data vault server for saving data
        self.pv = cxn.parametervault ## parameter vault server for loading/saving parameters of the experiment

        self.ident = ident
        #self.setup_data_vault() ## call data vault setup
        self.initialize_camera(cxn) 
        #self.readout_save_context = cxn.context()
        
        ## declare sub experiment
        self.sub_experiment = self.make_experiment(MOT_loading)
        self.sub_experiment.initialize(cxn, context, ident)
            
    def initialize_camera(self, cxn):
        self.camera = cxn.andor_server ## connect to andor camera server

        #self.camera_initially_live_display = self.camera.is_live_display_running()
        self.camera.abort_acquisition()
        self.camera.set_exposure_time(WithUnit(10.0,'ms'))
        self.camera.set_emccd_gain(1)
        
        self.binning = int(4.0)
        self.image_region = [
                             self.binning, ## binning
                             self.binning, ## binning
                             int(self.parameters['CCD_settings.y_min']), ### vertical ##down
                             int(self.parameters['CCD_settings.y_max']), ### vertical ## up
                             int(self.parameters['CCD_settings.x_min']), ### hor left
                             int(self.parameters['CCD_settings.x_max']), ### hor right
                             ]


        self.camera.set_image_region(*self.image_region)
        self.camera.set_acquisition_mode('Kinetics')
        self.initial_trigger_mode = self.camera.get_trigger_mode()
        self.camera.set_trigger_mode('External')    
            

        
    def run(self, cxn, context):
        '''
        main experiment running method
        '''
        self.parameters['MOT_loading.loading_time'] = WithUnit(300.0,'ms')
        self.sub_experiment.set_parameters(self.parameters)
        self.sub_experiment.run(cxn,context)
#         for i, freq in enumerate(self.scan):
#             ## for pausing
#             should_stop = self.pause_or_stop()
#             if should_stop: break
#             ## replace parameter that we are scanning
#             self.parameters['Clock.Clock_freq'] = freq
#             ## set parameters of the sub experiment and run
#             self.sub_experiment.set_parameters(self.parameters)
#             excitation = self.sub_experiment.run(cxn, context)
#             ## make data to be saved to DV
#             submission = [freq['kHz']]
#             submission.extend([excitation])
#             self.dv.add(submission, context = self.readout_save_context)
#             self.update_progress(i)
    
#     def update_progress(self, iteration):
#         progress = self.min_progress + (self.max_progress - self.min_progress)*float(iteration + 1.0)/len(self.scan)
#         self.sc.script_set_progress(self.ident, progress)
    
#     def finalize(self, cxn, context):
# 
#         self.pv.save_parameters_to_registry()
#         ### save parameter to also datavault data set
#         d = dict(self.parameters)
#         for name in d.keys():
#             #print name, d[name]
#             self.dv.add_parameter_over_write(name,d[name], context = self.readout_save_context)
#         #self.camera.start_live_display()


if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = quick_MOT(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)