class config_tracker(object):
    
    ID = 99983
    
    update_rate = 2.0 #seconds
    frequency_limit = (-5000.0, 5000.0) #MHz
    #saved_lines_729 = ['729Experiments','saved_lines_729']
    #favorites = {'S+1/2D-3/2':'OP', 'S-1/2D+3/2':'Right OP', 'S-1/2D-5/2':'carrier -1/2-5/2', 'S-1/2D-1/2':'carrier -1/2-1/2'}
    favorites = {'S+1/2P+1/2':'inner SP2', 'S+1/2P-1/2':'outer SP2 (low AO freq)', 'S-1/2P+1/2':'outer SP1', 'S-1/2P-1/2':'inner SP1 (low AO freq)'}