from pulse_sequence import pulse_sequence
from labrad.units import WithUnit
from treedict import TreeDict
from plot_sequence import SequencePlotter

class sampleDDS(pulse_sequence):
    
    def sequence(self):
        start_first = WithUnit(10, 'us')
        on_time = WithUnit(100, 'ms')
        off_time = WithUnit(100, 'ms')
        freq = WithUnit(85.0, 'MHz')
        ampl = WithUnit(-23.0, 'dBm')
#         self.addDDS('DDS_0', start_first, on_time, freq, ampl)
#         self.addDDS('DDS_1', start_second, on_time, freq, ampl)
        self.addDDS('DDS_0', WithUnit(1, 'ms'), WithUnit(500, 'ms'), WithUnit(85.0, 'MHz'), WithUnit(-13.0, 'dBm'))
        self.addDDS('DDS_0', WithUnit(501, 'ms'), WithUnit(500, 'ms'), WithUnit(85.0, 'MHz'), WithUnit(-33.0, 'dBm'))
        self.addDDS('DDS_1', WithUnit(250, 'ms'), WithUnit(100, 'ms'), WithUnit(88.0, 'MHz'), WithUnit(-33.0, 'dBm'))
        #self.addDDS('DDS_0', WithUnit(100, 'ms'), WithUnit(10, 'ms'), freq, ampl)
        #self.addDDS('DDS_1', WithUnit(1000, 'ms'), WithUnit(500, 'ms'), WithUnit(87.0, 'MHz'), WithUnit(-23.0, 'dBm'))
        
#         self.addTTL('channel_0',WithUnit(0,'ms'),WithUnit(100,'ms'))
#         self.addTTL('channel_0',WithUnit(200,'ms'),WithUnit(100,'ms'))
#         self.addTTL('channel_0',WithUnit(400,'ms'),WithUnit(100,'ms'))
        
if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    cs = sampleDDS(TreeDict())
    cs.programSequence(cxn.pulser)
    
    dds = cxn.pulser.human_readable_dds()
    ttl = cxn.pulser.human_readable_ttl()    
    channels = cxn.pulser.get_channels().asarray
    ##print ttl.asarray
    ##print dds.aslist
#     sp = SequencePlotter(ttl.asarray, dds.aslist, channels)
#     sp.makePlot()
    
    cxn.pulser.start_number(5)
    cxn.pulser.wait_sequence_done()
    cxn.pulser.stop_sequence()
    
    #print 'DONE'