class config(object):
    
    double_pass_passes = 2
    double_pass_direction = -1 #1 means add frequencies, -1 subtracts
    
    fit_order = 1 #order of polynomial for fitting
    
    keep_line_measurements = 120
    
    #data vault saving configuration
    save_folder = ['', 'Line_Tracking']
    dataset_name = 'Line Drift'
    #signaling
    signal_id = 9898991