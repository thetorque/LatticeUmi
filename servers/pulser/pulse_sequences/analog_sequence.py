from analog_sequences_config import analog_name_dictionary as analog_config
from labrad.units import WithUnit
from treedict import TreeDict
import numpy as np

class analog_sequence(object):
	
	'''
	Base class for analog sequence
	idea: when adding analog sequence, it should have this format: [channel,time,voltage] where
	we only put in the vertex of the V-T curve. Then in the end, there is a method to sort out
	and then generat an appropriate array to pass to the analog server
	Version 0.1
	'''
	required_parameters = []
	required_subsequences = []
	replaced_parameters = {}
	
	def __init__(self, parameter_dict, start = WithUnit(0, 's')):
		if not type(parameter_dict) == TreeDict: raise Exception ("replacement_dict must be a TreeDict in sequence {0}".format(self.__class__.__name__))
		self.start = start
		self.end = start
		self._analog_pulses = []
		self.replace = parameter_dict
		self.parameters = self.fill_parameters(self.required_parameters , self.replace)
		self.sequence()
	
	@classmethod
	def all_required_parameters(cls):
		'''
		returns a list of all required variables for the current sequence and all used subsequences
		'''
		required = set(cls.required_parameters)
		for subsequence in cls.required_subsequences:
			replaced = set(cls.replaced_parameters.get(subsequence, []))
			additional = set(subsequence.all_required_parameters())
			additional.difference_update(replaced)
			required = required.union(additional)
		required = list(required)
		return required
	
	def sequence(self):
		'''
		implemented by subclass
		'''
	
	def fill_parameters(self, params, replace):
		if not len(params) == len(set(params)):
			raise Exception ("Duplicate required parameters found in {0}".format(self.__class__.__name__))
		new_dict = TreeDict()
		for collection,parameter_name in params:
			treedict_key = '{0}.{1}'.format(collection,parameter_name)
			try:
				new_dict[treedict_key] = replace[treedict_key]
			except KeyError:
				raise Exception('{0} {1} value not provided for the {2} Pulse Sequence'.format(collection, parameter_name, self.__class__.__name__))
		return new_dict
	
	def addAnalog(self, channel, time, voltage):
		"""
		add an analog time-voltage point to the pulse sequence
		"""

		self._analog_pulses.append((channel, time, voltage))
	
	def addSequence(self, sequence, replacement_dict = TreeDict(), position = None):
		'''insert a subsequence, position is either time or None to insert at the end'''
		if sequence not in self.required_subsequences: raise Exception ("Adding subsequence {0} that is not listed in the required subequences".format(sequence.__class__.__name__))
		if not type(replacement_dict) == TreeDict: raise Exception ("replacement_dict must be a TreeDict")
		for replacement_key in replacement_dict.keys():
			parsed = tuple(replacement_key.split('.'))
			key_list = self.replaced_parameters.get(sequence, [])
			if not parsed in key_list:
				raise Exception("Error in {0}: replacing the key {1} in the sequence {2} that is not listed among the replacement parameters".format(self, replacement_key, sequence))
		if position is None:
			position = self.end
		#replacement conists of global replacement and keyword arguments
		replacement = TreeDict()
		replacement.update(self.replace)
		replacement.update(replacement_dict)
		seq = sequence(replacement, start = position)
		self._analog_pulses.extend( seq._analog_pulses )
		self.end = max(self.end, seq.end)
	
	def programAnalog(self, analog_server):
		pattern = self.convert_sequence(self._analog_pulses)
		print "program Analog"
		waveform = analog_server.set_voltage_pattern(pattern,True,100000)
		return waveform
		
	def convert_sequence(self, sequence_data):
		'''
		Take a list of analog sequence and create channel-wise array of v-t vertices.
		'''
		## initialize array
		channel_0 = np.array([[0],[0]])
		channel_1 = np.array([[0],[0]])
		channel_2 = np.array([[0],[0]])
		channel_3 = np.array([[0],[0]])
		channel_4 = np.array([[0],[0]])
		channel_5 = np.array([[0],[0]])
		channel_6 = np.array([[0],[0]])
		channel_7 = np.array([[0],[0]])
		
		## dump data into array
		for value in sequence_data:
			chan, time, voltage = value
			time_voltage = np.array([[time['s']],[voltage]])
			if chan == 0:
				channel_0 = np.hstack((channel_0,time_voltage))
			elif chan == 1:
				channel_1 = np.hstack((channel_1,time_voltage))
			elif chan == 2:
				channel_2 = np.hstack((channel_2,time_voltage))
			elif chan == 3:
				channel_3 = np.hstack((channel_3,time_voltage))
			elif chan == 4:
				channel_4 = np.hstack((channel_4,time_voltage))
			elif chan == 5:
				channel_5 = np.hstack((channel_5,time_voltage))	
			elif chan == 6:
				channel_6 = np.hstack((channel_6,time_voltage))	
			elif chan == 7:
				channel_7 = np.hstack((channel_7,time_voltage))	
					
		channel_0 = np.delete(channel_0,0,1)
		channel_1 = np.delete(channel_1,0,1)
		channel_2 = np.delete(channel_2,0,1)
		channel_3 = np.delete(channel_3,0,1)
		channel_4 = np.delete(channel_4,0,1)
		channel_5 = np.delete(channel_5,0,1)
		channel_6 = np.delete(channel_6,0,1)
		channel_7 = np.delete(channel_7,0,1)
		
		print channel_0
		
		
		time = reduce(np.union1d,(channel_0[0],channel_1[0],channel_2[0],channel_3[0],channel_4[0],channel_5[0],channel_6[0],channel_7[0]))
		#print time
		total_data = time
		
		#print channel_0
		
 		for channel, data in [(0, channel_0),
 		                      (1, channel_1),
 		                      (2, channel_2),
 		                      (3, channel_3),
 		                      (4, channel_4),
 		                      (5, channel_5),
 		                      (6, channel_6),
 		                      (7, channel_7),
 		                       ]:
 			voltage_array = data[1]
 			time_array = data[0]
 			ch = np.ones_like(time)
 			ch[0] = voltage_array[0] ## initialize first element
 
 			index = np.searchsorted(time_array,time, side='left')
 			for i in range(np.size(index)-1):
 				i = i+1
 				slope = (voltage_array[index[i]]-voltage_array[index[i]-1])/(time_array[index[i]]-time_array[index[i]-1])
 				ch[i] = ch[i-1]+slope*(time[i]-time[i-1])
 			total_data = np.vstack((total_data,ch))
 
 		pattern = total_data
 		return pattern
		
		### create common-time array
		
		
		
		
		
		
		#print self._analog_pulses
		
# 		pulser.new_sequence()
# 		pulser.add_ttl_pulses(self._ttl_pulses)
# 		pulser.add_dds_pulses(self._dds_pulses)
# 		pulser.program_sequence()