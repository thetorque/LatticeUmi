import labrad
from labrad.units import WithUnit
cxn = labrad.connect()
tracker = cxn.line_tracker
tracker.set_measurement(WithUnit(0.1, 'kHz'))
#print tracker