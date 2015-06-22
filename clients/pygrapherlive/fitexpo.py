"""

This class defines a line curve to fit and its parameters

"""
import numpy as np
from fitcurve import CurveFit

class FitExpo(CurveFit):

    def __init__(self, parent):
        self.parent = parent
        self.curveName = 'Expo'
        self.parameterNames = ['Decay_time', 'Amplitude','Offset']
        self.parameterValues = [1.0, 1.0,0.0]
        self.parameterFit = [True,True, True]

    # idk, something like this?
    def fitFunc(self, x, p):
        """ 
            Line
            p = [Decay_time, Amplitude,Offset]
        
        """   
        curve = fitFunc = p[1]*np.exp(-x/p[0]) + p[2] #line
        return curve    