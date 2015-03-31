import labrad
cxn = labrad.connect()
l = cxn.labview_server
print l.say_name('A')
print l.return_message('B')