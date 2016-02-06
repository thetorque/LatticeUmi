from servers.script_scanner.scan_methods import experiment
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
Experiment for drift tracker of the cavity
'''    
       
class Clock_stabilization(experiment):
    ##name of the experiment to be shown in the scriptscanner
    name = 'Clock stabilization'  
    ## list required parameters for this experiment
    experiment_required_parameters = [('Clock_stab','Half_linewidth'),
                                      ('Clock_stab','Tracker_number'),
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
        self.sd = cxn.sd_tracker ### drifttracker
        self.tracker = cxn.line_tracker

        self.readout_save_context = cxn.context() ## context for saving data
        self.ident = ident
        self.setup_data_vault() ## call data vault setup
        self.initialize_camera(cxn) 
        
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
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H", localtime)]
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
            self.dv.new('MOT {}'.format(self.datasetNameAppend),[('Time', 'Sec')],[('Excitation','Excitation','Excitation'),
                                                                                   ('Error Sig.','Error Sig.','Error Sig.'),
                                                                                   ('Drift rate','Drift rate','Hz/s'),
                                                                                   ('line freq','line freq','kHz'),
                                                                                   ('lock','lock','lock')], context = self.readout_save_context)   
            self.dv.add_parameter('Window', ['Stabilization'], context = self.readout_save_context)     
            ## open the graph once the data set is created
            self.dv.add_parameter('plotLive', True, context = self.readout_save_context)     
        
    def run(self, cxn, context):
        '''
        main experiment running method
        '''
        now = datetime.now()
        self.start_time = (now-now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
        
        tracker_channel = int(self.parameters['Clock_stab.Tracker_number'])
        
        ###
        freq_step = self.parameters['Clock_stab.Half_linewidth']
        
        ###freq_step = 0.89/self.parameters['Clock.clock_duration'] ## calculate frequency setp directly from the clock_duration
        
        ## do the first side of the first line
        #freq_line_1 = self.sd.get_current_line('S+1/2P+1/2') + freq_step
        freq_line_1 = self.tracker.get_current_line(tracker_channel) + freq_step
        print freq_line_1
        
        self.parameters['Clock.Clock_freq'] = freq_line_1
        self.sub_experiment.set_parameters(self.parameters)
        result_1 = self.sub_experiment.run(cxn,context)

        ## do the second side of the first line
        #freq_line_2 = self.sd.get_current_line('S+1/2P+1/2') - freq_step
        
        freq_line_2 = self.tracker.get_current_line(tracker_channel) - freq_step
        print freq_line_2
        
        self.parameters['Clock.Clock_freq'] = freq_line_2
        self.sub_experiment.set_parameters(self.parameters)
        result_2 = self.sub_experiment.run(cxn,context)
        
        #result_1 = (0.32, 500.0)
        #result_2 = (0.29, 500.0)
        
        ## calculate correction
        gain = 1.4
        error_signal = freq_step*gain*(result_1[0] - result_2[0])
        #error_signal = error_signal['Hz']
        average_excitation = (result_1[0] + result_2[0])/2.0
        print error_signal
        
        ## calculate new frequency
        new_freq_1 = (freq_line_1 + freq_line_2)/2.0 + error_signal
        
        ## get drift rate
        drift_rate_1 = self.tracker.get_fit_parameters(tracker_channel)[-2]*1000.0 ## the returning fit parameter is a*x + b
        
        #print drift_rate_1
        
        ## check if anything bad happened
        if ((result_1[0] < 0.0) or (result_1[0]>1.0) or (result_2[0] < 0.0) or (result_2[0]>1.0)):
            is_locked = 0.0
        elif ((result_1[1] < 200.0) or (result_2 < 200.0)):
            is_locked = 0.0
        else:
            is_locked = 1.0
        
        submission = [self.start_time, average_excitation, error_signal['Hz'], drift_rate_1, new_freq_1['kHz'], is_locked]

        self.dv.add(submission, context =self.readout_save_context)
        
        if is_locked > 0.5: ## if no problem, feed it back to sd_tracker
            #print "submit to tracker"
#             freq_submission = [
#                                ('S+1/2P+1/2', new_freq_1),
#                                ('S-1/2P-1/2',WithUnit(0.0,'Hz'))]
            freq_submission = new_freq_1
            print "submit ", freq_submission
            self.tracker.set_measurement(freq_submission, tracker_channel)
        else:
            print "condition not met"

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
    exprt = Clock_stabilization(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)