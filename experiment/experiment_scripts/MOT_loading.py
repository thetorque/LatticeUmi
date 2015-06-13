from servers.script_scanner.scan_methods import experiment
from experiment.pulser_sequences.MOT_loading_seq import MOT_loading_seq
from experiment.pulser_sequences.TTL_test import TTL_test
from labrad.units import WithUnit
import labrad
import numpy
import time
from datetime import datetime
import matplotlib.pyplot as plt
       
class MOT_loading(experiment):
    name = 'MOT loading'  
    experiment_required_parameters = [('CCD_setting','exposure_time'),]
    pulse_sequence = MOT_loading_seq
    #pulse_sequence = TTL_test
    
    @classmethod
    def all_required_parameters(cls):
        params = set(cls.experiment_required_parameters)
        params = params.union(set(cls.pulse_sequence.all_required_parameters()))
        params = list(params)
        return params
    
    def initialize(self, cxn, context, ident):
        self.pulser = cxn.pulser
        self.dv = cxn.data_vault
        self.pv = cxn.parametervault

        self.readout_save_context = cxn.context()

        self.setup_data_vault()
        self.initialize_camera(cxn)
            
    def initialize_camera(self, cxn):
        self.camera = cxn.andor_server

        self.camera_initially_live_display = self.camera.is_live_display_running()
        self.camera.abort_acquisition()

        self.image_region = [
                             4,
                             4,
                             302,
                             369,
                             236,
                             295,
                             ]


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
        
    
        
    def run(self, cxn, context):

        print "running"
        repetitions = 3;
        
        pulse_sequence = self.pulse_sequence(self.parameters)
        pulse_sequence.programSequence(self.pulser)

        self.camera.set_number_kinetics(3)
        self.camera.start_acquisition()
        
        ### get no. of second of today
        now = datetime.now()
        start_time = (now-now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
        
        self.pulser.start_number(1)
        self.pulser.wait_sequence_done()
        self.pulser.stop_sequence()

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
        S_image = images[0]/(0.11547*20)
        #print S_image
#         plt.imshow(S_image)
#         plt.show()
        S_state = (numpy.sum(images[0])-numpy.sum(images[2]))/(0.11547*20)
        P_state = (numpy.sum(images[1])-numpy.sum(images[2]))/(0.11547*20)
        
         
        Atom_number_data = numpy.array([start_time,S_state,P_state,S_state+P_state])
        #print Atom_number_data
         
        self.dv.add(Atom_number_data, context = self.readout_save_context)
        
        return S_state+P_state

    def finalize(self, cxn, context):
        #pass
        self.pv.save_parameters_to_registry()
        self.camera.start_live_display()

if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = MOT_loading(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)