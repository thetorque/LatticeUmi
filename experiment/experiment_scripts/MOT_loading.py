from servers.script_scanner.scan_methods import experiment
#from experiment.pulser_sequences.MOT_loading_seq import MOT_loading_seq
from experiment.pulser_sequences.MOT_loading_w_LV import MOT_loading_seq
from experiment.analog_sequences.MOT_loading_analog import MOT_loading_analog

from labrad.units import WithUnit
import labrad
import numpy
import time
from datetime import datetime

'''
Template for the experiment. By Hong.
'''

       
class MOT_loading(experiment):
    ##name of the experiment to be shown in the scriptscanner
    name = 'MOT loading'  
    ## list required parameters for this experiment
    experiment_required_parameters = [('CCD_settings','exposure_time'),
                                      ('CCD_settings','EMCCD_gain'),
                                      ]
    ## define which pulse sequence to use
    pulse_sequence = MOT_loading_seq
    ## define which analog sequence to use
    analog_sequence = MOT_loading_analog

    
    @classmethod
    def all_required_parameters(cls):
        '''
        take the required parameters for both pulse sequence and analog sequence and union into a total list of require parameters for this experiment
        '''
        params = set(cls.experiment_required_parameters)
        params = params.union(set(cls.pulse_sequence.all_required_parameters()))
        params = params.union(set(cls.analog_sequence.all_required_parameters()))
        params = list(params)
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

        self.setup_data_vault() ## call data vault setup
        
        self.initialize_camera(cxn) 
            
    def initialize_camera(self, cxn):
        self.camera = cxn.andor_server ## connect to andor camera server

        self.camera_initially_live_display = self.camera.is_live_display_running()
        self.camera.abort_acquisition()
        self.camera.set_exposure_time(self.parameters['CCD_settings.exposure_time'])
        self.camera.set_emccd_gain(int(self.parameters['CCD_settings.EMCCD_gain']))
        self.image_region = [
                             4, ## binning
                             4, ## binning
                             316, ### vertical ##up
                             343, ### vertical ## down
                             225, ### hor left
                             252, ### hor right
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
            print "yes"
            self.dv.open_appendable(names[0], context=self.readout_save_context)
        ### if there's no matched name, then create the data set
        else:
            ## this line defines the structure of the data. "name", horizontal axis, vertical axis (this case, there are multiple lines)
            self.dv.new('MOT {}'.format(self.datasetNameAppend),[('Time', 'Sec')],[('S_state','S_state.','No.'),('P_state','P_state.','No.'),('BG','BG','No.')], context = self.readout_save_context)   
            self.dv.add_parameter('Window', ['MOT population'], context = self.readout_save_context)     
            ## open the graph once the data set is created
            self.dv.add_parameter('plotLive', True, context = self.readout_save_context)     
        
    
        
    def run(self, cxn, context):
        '''
        main experiment running method
        '''
        
        ## setup pulse sequence and program
        pulse_sequence = self.pulse_sequence(self.parameters)
        pulse_sequence.programSequence(self.pulser)
        
        ### setup analog sequence and program
        analog_sequence = self.analog_sequence(self.parameters)
        analog_sequence.programAnalog(self.NI_analog)
        
        ## setup camera and get ready
        self.camera.set_number_kinetics(3)
        self.camera.start_acquisition()
        
        ### get no. of second of today
        now = datetime.now()
        start_time = (now-now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
        
        #### configure TTL switching from manual to auto ###
        self.pulser.switch_auto('BIG_MOT_SH', False)
        self.pulser.switch_auto('BIG_MOT_AO', False)
        
        #### start pulse sequence
        
        self.pulser.start_number(1)
        self.pulser.wait_sequence_done()
        self.pulser.stop_sequence()
        
        #### configure TTL switching back to manual###
        self.pulser.switch_manual('BIG_MOT_SH', True)
        self.pulser.switch_manual('BIG_MOT_AO', True)
        
        #### stop analog pattern
        self.NI_analog.stop_voltage_pattern()
        
        
        ### wait to see if the camera is missing some pictures
        proceed = self.camera.wait_for_kinetic()
        if not proceed:
            self.camera.abort_acquisition()
            self.finalize(cxn, context)
            raise Exception ("Did not get all kinetic images from camera")
        ### read all three picture
        images = self.camera.get_acquired_data(3).asarray
        ### stop camera
        self.camera.abort_acquisition()
        
        ### create number of pixel in x and y direction for array of data
        x_pixels = int( (self.image_region[3] - self.image_region[2] + 1.) / (self.image_region[0]) )
        y_pixels = int(self.image_region[5] - self.image_region[4] + 1.) / (self.image_region[1])
        
        ### reshape array into three x-y images
        images = numpy.reshape(images, (3, y_pixels, x_pixels))

        ### send data to the camera server for displaying the picture
        self.camera.set_ccd_images(images)
        
        ### calculate the no. of atoms
        
        expose_time_ms = self.parameters['CCD_settings.exposure_time']['ms']
        ccd_gain = self.parameters['CCD_settings.EMCCD_gain']
        
        S_state = (numpy.sum(images[0]-images[2]))/(0.11547*expose_time_ms*ccd_gain)
        P_state = (numpy.sum(images[1]-images[2]))/(0.11547*expose_time_ms*ccd_gain)
        
        ### create array of data 
        Atom_number_data = numpy.array([start_time,S_state,P_state,S_state+P_state])
        ##print Atom_number_data
        
        ## save to DV
        self.dv.add(Atom_number_data, context = self.readout_save_context)

        ### return value for this experiment. Used for scanning this script.
        return S_state+P_state

    def finalize(self, cxn, context):

        self.pv.save_parameters_to_registry()
        #self.camera.start_live_display()


if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = MOT_loading(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)