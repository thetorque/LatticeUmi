from servers.script_scanner.scan_methods import experiment
#from experiment.pulser_sequences.MOT_loading_seq import MOT_loading_seq
from experiment.experiment_scripts.Clock_weak import Clock_weak

from labrad.units import WithUnit
import labrad
import numpy
import time
from datetime import datetime

'''
Template for the experiment. By Hong.
'''
'''
This experiment implement scan of the Clock_weak_scan experiment
'''    
       
class Clock_weak_scan(experiment):
    ##name of the experiment to be shown in the scriptscanner
    name = 'Clock weak_scan'  
    ## list required parameters for this experiment
    experiment_required_parameters = [('Clock_scan','manual_scan'),
                                      ]
    ## define which pulse sequence to use
    #pulse_sequence = Clock_weak
    ## define which analog sequence to use
    #analog_sequence = MOT_clock_analog

    
    @classmethod
    def all_required_parameters(cls):
        '''
        take the required parameters for both pulse sequence and analog sequence and union into a total list of require parameters for this experiment
        '''
        params = set(cls.experiment_required_parameters)
        params = params.union(set(Clock_weak.all_required_parameters()))
        #params = params.union(set(cls.analog_sequence.all_required_parameters()))
        params = list(params)
        
        ### remove parameter that we are scanning
        params.remove(('Clock','Clock_freq'))
        
        return params
    
    def initialize(self, cxn, context, ident):
        '''
        initialization: list all the servers we need to talk to
        '''
        self.pulser = cxn.pulser ## pulse sequence server
        self.NI_analog = cxn.ni_analog_server ## analog sequence server
        self.dv = cxn.data_vault ## data vault server for saving data
        self.pv = cxn.parametervault ## parameter vault server for loading/saving parameters of the experiment

        self.readout_save_context = cxn.context() ## context for saving data
        self.ident = ident
        self.setup_data_vault() ## call data vault setup
        self.initialize_camera(cxn) 
        
        self.setup_scan_parameter()
        
        ## declare sub experiment
        self.sub_experiment = self.make_experiment(Clock_weak)
        self.sub_experiment.initialize(cxn, context, ident)
            
    def initialize_camera(self, cxn):
        self.camera = cxn.andor_server ## connect to andor camera server

        #self.camera_initially_live_display = self.camera.is_live_display_running()
        self.camera.abort_acquisition()
        self.camera.set_exposure_time(self.parameters['CCD_settings.exposure_time'])
        self.camera.set_emccd_gain(int(self.parameters['CCD_settings.EMCCD_gain']))
        
        self.binning = int(self.parameters['CCD_settings.binning'])
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
        
    def setup_data_vault(self):
        localtime = time.localtime()
        self.datasetNameAppend = time.strftime("%Y%b%d_%H",localtime)
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        self.save_directory = ['','Experiments']
        self.save_directory.extend([self.name])
        self.save_directory.extend(dirappend)
        self.dv.cd(self.save_directory ,True, context = self.readout_save_context)
        
        data_in_folder = self.dv.dir(context=self.readout_save_context)[1]
        
        ## look for dataset in the folder
        names = sorted([name for name in data_in_folder if self.datasetNameAppend in name])
        
        ### if there's matched name, then don't create a new data set. Simply append to it
        if names:
            self.dv.open_appendable(names[0], context=self.readout_save_context)
        ### if there's no matched name, then create the data set
        else:
            ## this line defines the structure of the data. "name", horizontal axis, vertical axis (this case, there are multiple lines)
            self.dv.new('MOT {}'.format(self.datasetNameAppend),[('Frequency', 'MHz')],[('Excitation','Excitation','Excitation')], context = self.readout_save_context)   
            self.dv.add_parameter('Window', ['Excitation'], context = self.readout_save_context)     
            ## open the graph once the data set is created
            self.dv.add_parameter('plotLive', True, context = self.readout_save_context)     
            
    def setup_scan_parameter(self):
        sp = self.parameters.Clock_scan
        minim, maxim, steps = sp.manual_scan
        self.scan = numpy.linspace(minim, maxim, steps)
        self.scan = [WithUnit(pt,'kHz') for pt in self.scan]

        
    def run(self, cxn, context):
        '''
        main experiment running method
        '''
        for i, freq in enumerate(self.scan):
            ## for pausing
            should_stop = self.pause_or_stop()
            if should_stop: break
            ## replace parameter that we are scanning
            self.parameters['Clock.Clock_freq'] = freq
            ## set parameters of the sub experiment and run
            self.sub_experiment.set_parameters(self.parameters)
            result = self.sub_experiment.run(cxn, context)
            excitation = result[0]
            ## make data to be saved to DV
            submission = [freq['kHz']]
            submission.extend([excitation])
            self.dv.add(submission, context = self.readout_save_context)
            self.update_progress(i)
    
    def update_progress(self, iteration):
        progress = self.min_progress + (self.max_progress - self.min_progress)*float(iteration + 1.0)/len(self.scan)
        self.sc.script_set_progress(self.ident, progress)
    
    def finalize(self, cxn, context):

        self.pv.save_parameters_to_registry()
        ### save parameter to also datavault data set
        d = dict(self.parameters)
        for name in d.keys():
            #print name, d[name]
            self.dv.add_parameter_over_write(name,d[name], context = self.readout_save_context)
        #self.camera.start_live_display()


if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = Clock_weak_scan(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)