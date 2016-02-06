#!/usr/bin/env python
import labrad
import numpy as np
import time

#connect to LabRAD
try:
    cxn = labrad.connect(name='Node Client')
except:
    print 'Please start LabRAD Manager'
    time.sleep(10)
    raise()

nodeDict = {
            'node ELI':
                ['Data Vault',
                'NI Analog Server',
                'Andor Server',
                'NormalPMTFlow',
                'SD Tracker',
                'ScriptScanner',
                'Line Tracker',
                'ParameterVault',
                'Pulser'],
    }
for node in nodeDict.keys(): #sets the order of opening
    #make sure all node servers are up
    if not node in cxn.servers: print node + ' is not running'
    else:
        print '\n' + 'Working on ' + node + '\n'
        #if node server is up, start all possible servers on it that are not already running
        running_servers = np.array(cxn.servers[node].running_servers().asarray)
        for server in nodeDict[node]:
            if server in running_servers: 
                print server + ' is running'
                try:
                    cxn.servers[node].stop(server)
                    print server, 'is stopped'
                except:
                    print 'ERROR with ' + server
            else:
                print server, 'is not running'



time.sleep(1)
print "Have a good day!"
time.sleep(1)
