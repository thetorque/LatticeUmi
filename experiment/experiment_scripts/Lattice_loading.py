from servers.script_scanner.scan_methods import experiment
#from experiment.pulser_sequences.MOT_loading_seq import MOT_loading_seq
from experiment.pulser_sequences.MOT_loading import MOT_loading_seq
from experiment.analog_sequences.MOT_clock_analog import MOT_clock_analog

from labrad.units import WithUnit
import labrad
import numpy
import time
from datetime import datetime

'''
Template for the experiment. By Hong.
'''
'''
Experiment to check the loading of the lattice
'''    
       
class Lattice_loading(experiment):
    ##name of the experiment to be shown in the scriptscanner
    name = 'Lattice loading'  
    ## list required parameters for this experiment
    experiment_required_parameters = [('CCD_settings','exposure_time'),
                                      ('CCD_settings','EMCCD_gain'),
                                      ('CCD_settings','binning'),
                                      ('CCD_settings','x_min'),
                                      ('CCD_settings','x_max'),
                                      ('CCD_settings','y_min'),
                                      ('CCD_settings','y_max'),
                                      ('CCD_settings','x_min_cropped'),
                                      ('CCD_settings','x_max_cropped'),
                                      ('CCD_settings','y_min_cropped'),
                                      ('CCD_settings','y_max_cropped'),
                                      ]
    ## define which pulse sequence to use
    pulse_sequence = MOT_loading_seq
    ## define which analog sequence to use
    #analog_sequence = MOT_loading_analog
    analog_sequence = MOT_clock_analog

    
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
        self.save_directory.extend(['MOT loading'])
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
            self.dv.new('MOT {}'.format(self.datasetNameAppend),[('Time', 'Sec')],[('S_state','S_state.','No.'),('P_state','P_state.','No.'),('Total','Total','No.')], context = self.readout_save_context)   
            self.dv.add_parameter('Window', ['MOT population'], context = self.readout_save_context)     
            ## open the graph once the data set is created
            self.dv.add_parameter('plotLive', True, context = self.readout_save_context)     
        
    def plot_current_sequence(self, cxn):
        from servers.pulser.pulse_sequences.plot_sequence import SequencePlotter
        dds = cxn.pulser.human_readable_dds()
        ttl = cxn.pulser.human_readable_ttl()
        channels = cxn.pulser.get_channels().asarray
        sp = SequencePlotter(ttl.asarray, dds.aslist, channels)
        sp.makePlot()    
        
    def initSequence(self, cxn):
        ## setup pulse sequence and program
        pulse_sequence = self.pulse_sequence(self.parameters)
        pulse_sequence.programSequence(self.pulser)
        
        ##plot sequence to see check visually
        #self.plot_current_sequence(cxn)
        
        ### setup analog sequence and program
        analog_sequence = self.analog_sequence(self.parameters)
        
        #analog_sequence.plotPatternArray(self.NI_analog)
        
        analog_sequence.programAnalog(self.NI_analog)
        
        ## setup camera and get ready
        self.camera.set_number_kinetics(3)
        self.camera.start_acquisition()
        
        ### get no. of second of today
        now = datetime.now()
        self.start_time = (now-now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
        
    def execSequence(self):
        self.pulser.start_number(1)
        self.pulser.wait_sequence_done()
        self.pulser.stop_sequence()
        self.NI_analog.stop_voltage_pattern()
        
        
    def run(self, cxn, context):
        '''
        main experiment running method
        '''
        
        self.initSequence(cxn)
        
        #### configure TTL switching from manual to auto ###
        self.pulser.switch_auto('BIG_MOT_SH', True)
        self.pulser.switch_auto('BIG_MOT_AO', True)
        
        #### start pulse sequence
        self.execSequence()
 
        #### configure TTL switching back to manual###
        self.pulser.switch_manual('BIG_MOT_SH', False)
        self.pulser.switch_manual('BIG_MOT_AO', False)
        
        #### stop analog pattern
        
        
        Atom_number_data = self.perform_readout(cxn, context)
        ### wait to see if the camera is missing some pictures
        
        
        ## save to DV
        self.dv.add(Atom_number_data, context = self.readout_save_context)

        ### return value for this experiment. Used for scanning this script.
        return Atom_number_data[3]
    
    def perform_readout(self, cxn, context):
        '''
        Take picture from the CCD camera. Send picture to the server for displaying. Calculate and return the atom number data.
        '''
        
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
        self.y_pixels = int( (self.image_region[3] - self.image_region[2] + 1.) / (self.image_region[0]) )
        self.x_pixels = int(self.image_region[5] - self.image_region[4] + 1.) / (self.image_region[1])
        
        ### reshape array into three x-y images
        images = numpy.reshape(images, (3, self.x_pixels, self.y_pixels))

        images_cropped = self.cropImage(images)
        ### set the main camera display
        image_offset = numpy.array([self.parameters['CCD_settings.x_min'],self.parameters['CCD_settings.y_min']])
        
        ### send data to the camera server for displaying the picture
        self.camera.set_ccd_images(images_cropped,images[0]-images[2],image_offset, self.parameters['CCD_settings.binning'])
        
        ### calculate the no. of atoms
        
        expose_time_ms = self.parameters['CCD_settings.exposure_time']['ms']
        ccd_gain = self.parameters['CCD_settings.EMCCD_gain']
        
        S_state = (numpy.sum(images_cropped[0]-images_cropped[2]))/(0.11547*expose_time_ms*ccd_gain)
        P_state = (numpy.sum(images_cropped[1]-images_cropped[2]))/(0.11547*expose_time_ms*ccd_gain)
        P_state = P_state/0.45
        
        return numpy.array([self.start_time,S_state,P_state,S_state+P_state])
        
    
    def cropImage(self, images):
        '''
        crop image according to the parameter crop. This will reduce noise from the region of the camera picture without meaningful data.
        '''
        ### crop image
        
        x_min_index = numpy.floor((self.parameters['CCD_settings.x_min_cropped'] - self.parameters['CCD_settings.x_min'])/self.parameters['CCD_settings.binning'])
        x_max_index = numpy.floor((self.parameters['CCD_settings.x_max_cropped'] - self.parameters['CCD_settings.x_min'])/self.parameters['CCD_settings.binning'])
        y_min_index = numpy.floor((self.parameters['CCD_settings.y_min_cropped'] - self.parameters['CCD_settings.y_min'])/self.parameters['CCD_settings.binning'])
        y_max_index = numpy.floor((self.parameters['CCD_settings.y_max_cropped'] - self.parameters['CCD_settings.y_min'])/self.parameters['CCD_settings.binning'])
        
        if (x_min_index < 0) or (y_min_index < 0) or (x_max_index > (self.x_pixels-1)) or (y_max_index > (self.y_pixels-1)):
            '''
            if the cropping region is not good (too big), then just do not do any cropping
            '''
            x_min_index = 0
            y_min_index = 0
            x_max_index = self.x_pixels-1
            y_max_index = self.y_pixels-1
        
        return images[:,x_min_index:x_max_index,y_min_index:y_max_index]
    
    def finalize(self, cxn, context):

        self.pv.save_parameters_to_registry()
        ### save parameter to also datavault data set
        d = dict(self.parameters)
        for name in d.keys():
            self.dv.add_parameter_over_write(name,d[name], context = self.readout_save_context)



if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = Lattice_loading(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)