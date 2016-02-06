
##### a gui to display NI AO data

from analog_sequences_config import analog_name_dictionary
import matplotlib.gridspec as gridspec
from matplotlib import pyplot

class AO_plotter():
    def __init__(self, data):
        self.plot = pyplot
        self.load_plot_data(data)
        self.create_plot_layout()
        self.plot_ao_channel()
    
    def create_plot_layout(self):
        self.fig = self.plot.figure()
        self.analog_plot = []
        
        ## create a grid according to the number of channels
        gs = gridspec.GridSpec(self.channel, 1, wspace=0.15, left = 0.05, right = 0.95)
        
        ## loop and create all channel plots
        for i in range(self.channel):
            #print "channel ",i
            #plot = self.fig.add_subplot(gs[i,0])
            
            if i == 0:
                plot = self.fig.add_subplot(gs[i,0])
            else:
                plot = self.fig.add_subplot(gs[i,0],sharex=plot) ## scale the x-axis to be the same as the first plot for subsequent plots
                
            plot.set_ylabel('V')
            plot.grid(True)
            ## show x label only for the lowest channel
            plot.tick_params(axis='x',which='both',labelbottom='off')
            if i == (self.channel-1):
                plot.set_xlabel('Time (s)')
                plot.tick_params(axis='x',which='both',labelbottom='on')
            #plot.set_title("Analog "+str(i))
            
            ## look for the name of the analog channel with the corresponding channel number
            for name in analog_name_dictionary:
                if analog_name_dictionary[name] == i:
                    plot.set_title(name)
            #plot.set_title()
            ## add plot to the analog_plot list
            self.analog_plot.append(plot)
            
    def plot_ao_channel(self):
        for p in range(self.channel):
            self.analog_plot[p].plot(self.plot_data[0], self.plot_data[p+1], '-r')
        self.plot.show()
        
    def load_plot_data(self, data):
        #self.plot_data = numpy.load("ramp.npy")
        self.plot_data = data
        self.channel = self.plot_data.shape[0]-1 ## get the number of channel from the file

if __name__=="__main__":
    AO = AO_plotter()