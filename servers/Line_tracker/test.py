import labrad
from labrad.units import WithUnit
import time
cxn = labrad.connect()
tracker = cxn.line_tracker
#tracker.add_tracker()
tracker.add_tracker()
time.sleep(1)
tracker.set_measurement(WithUnit(1.3, 'kHz'), 2)
time.sleep(1)
tracker.set_measurement(WithUnit(1.4, 'kHz'), 2)
time.sleep(1)
tracker.set_measurement(WithUnit(1.2, 'kHz'), 2)
time.sleep(1)
tracker.set_measurement(WithUnit(1.3, 'kHz'), 2)
# time.sleep(1)
# tracker.set_measurement(WithUnit(2.0, 'kHz'), 1)
# tracker.set_measurement(WithUnit(-2.0, 'kHz'), 2)
# time.sleep(1)
# tracker.set_measurement(WithUnit(3.0, 'kHz'), 1)
# tracker.set_measurement(WithUnit(-3.0, 'kHz'), 2)
# print tracker.get_fit_parameters(1)
# print tracker.get_fit_parameters(2)
# time.sleep(1)
# print tracker.get_current_line(1)
# print tracker.get_current_line(2)
# print tracker.get_fit_history(1)
# print tracker.get_fit_history(2)
#print tracker