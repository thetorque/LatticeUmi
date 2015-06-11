class channelConfiguration(object):
    """
    Stores complete configuration for each of the channels
    """
    def __init__(self, channelNumber, ismanual, manualstate,  manualinversion, autoinversion):
        self.channelnumber = channelNumber
        self.ismanual = ismanual
        self.manualstate = manualstate
        self.manualinv = manualinversion
        self.autoinv = autoinversion
        
class ddsConfiguration(object):
    """
    Stores complete configuration of each DDS board
    """
    def __init__(self, address, allowedfreqrange, allowedamplrange, frequency, amplitude, **args):
        self.channelnumber = address
        self.allowedfreqrange = allowedfreqrange
        self.allowedamplrange = allowedamplrange
        self.frequency = frequency
        self.amplitude = amplitude
        self.state = True
        self.boardfreqrange = args.get('boardfreqrange', (0.0, 2000.0))
        self.boardramprange = args.get('boardramprange', (0.000113687, 7.4505806))
        self.board_amp_ramp_range = args.get('board_amp_ramp_range', (0.00174623, 22.8896))
        self.boardamplrange = args.get('boardamplrange', (-48.0, 6.0))
        self.boardphaserange = args.get('boardphaserange', (0.0, 360.0))
        self.off_parameters = args.get('off_parameters', (0.0, -63.0))
        self.phase_coherent_model = args.get('phase_coherent_model', True)        
        self.remote = args.get('remote', False)
        self.name = None #will get assigned automatically

class remoteChannel(object):
    def __init__(self, ip, server, **args):
        self.ip = ip
        self.server = server
        self.reset = args.get('reset', 'reset_dds')
        self.program = args.get('program', 'program_dds')
        
class hardwareConfiguration(object):
    channelTotal = 32
    timeResolution = '40.0e-9' #seconds
    timeResolvedResolution = 10.0e-9
    maxSwitches = 1022
    resetstepDuration = 3 #duration of advanceDDS and resetDDS TTL pulses in units of timesteps
    collectionTimeRange = (0.010, 5.0) #range for normal pmt counting
    sequenceTimeRange = (0.0, 85.0) #range for duration of pulse sequence    
    isProgrammed = False
    sequenceType = None #none for not programmed, can be 'one' or 'infinite'
    collectionMode = 'Normal' #default PMT mode
    collectionTime = {'Normal':0.100,'Differential':0.100} #default counting rates
    okDeviceID = 'Pulser2'
    okDeviceFile = 'photon_2015_06_10.bit'
    lineTriggerLimits = (0, 15000)#values in microseconds 
    secondPMT = False
    DAC = False
    
    #name: (channelNumber, ismanual, manualstate,  manualinversion, autoinversion)
    channelDict = {
                   'CAMERA':channelConfiguration(0, False, False, False, False), ## camera
                   'ttl_1':channelConfiguration(1, False, False, False, False),
                   'ttl_2':channelConfiguration(2, False, False, False, False),
                   'BIG_MOT_SH':channelConfiguration(3, False, False, False, False),
                   'ttl_4':channelConfiguration(4, False, False, False, False),
                   'AdvanceDDS':channelConfiguration(18, False, False, False, False),
                   'ResetDDS':channelConfiguration(19, False, False, False, False),
                   'AO1':channelConfiguration(20, False, False, False, False), ### triggering for analog board
                   'AO2':channelConfiguration(21, False, False, False, False), ### triggering for analog board
                   
                }
    #address, allowedfreqrange, allowedamplrange, frequency, amplitude, **args):
    ddsDict =   {
                'DDS_0':ddsConfiguration(    0,  (0.0,800.0),   (-48.0,6.0),  70.0,   -48.0),
                'BIG_MOT':ddsConfiguration(    1,  (145.0,155.0),   (-48.0,-5.0),  150.0,   -48.0),
                '254_COMB':ddsConfiguration(    2,  (6.5,11.0),   (-48.0,5.0),  9.0,   4.5),
                'SMALL_MOT':ddsConfiguration(    3,  (145.0,155.0),   (-48.0,6.0),  150.0,   -48.0),
#                 'DDS_4':ddsConfiguration(    4,  (0.0,800.0),   (-63.0,-3.0),  90.0,   -63.0),
#                 'DDS_5':ddsConfiguration(    5,  (0.0,800.0),   (-63.0,-3.0),  95.0,   -63.0),
#                 'DDS_6':ddsConfiguration(    6,  (0.0,800.0),   (-63.0,-3.0), 100.0,   -63.0),
#                 'DDS_7':ddsConfiguration(    7,  (0.0,800.0),   (-63.0,-3.0), 105.0,   -63.0),
                }
    remoteChannels = {
                    }