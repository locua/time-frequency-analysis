#!/usr/bin/env python

import os
import re
import mne
import numpy as np

print('>>>')

my_dir = './ica_notebooks/cleaned'

def find_files(folder_path, extension):
    matching_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(extension):
                matching_files.append(os.path.join(root, file))
    return matching_files

extension = ".vhdr"

matching_files = find_files(my_dir, extension)

event_map = {'Comment/101':101, 
             'Comment/109':109,
             'Comment/30':30,
             'Comment/40':40,
             'Comment/50':50,
             'Comment/51':51,
             'Comment/52':52,
             'Comment/60':60,
             'Comment/70':70,
             'Comment/80':80,
             'New Segment/':99999}


def epoch_loop():
    for file_path in matching_files:

        m1 = re.search(r'[^/]*(?=.vhdr)', file_path)
        save_name = m1.group()
    
        #### SOME mne loading and EPOCH REMOVAL CODE ####
        raw = mne.io.read_raw(file_path, preload=True)
        events = mne.events_from_annotations(raw, event_map)
    
        tmin=0
        tmax=6
    
        event_id = {'Comment/40': 40}
    
        epochs = mne.Epochs(raw, events[0], event_id, tmin, tmax, preload=True, baseline=(0,0))
    
        epochs.plot()

        input('Continue?')
        epochs.plot_drop_log()

        #### END BLOCK ####
        
        # Clean up memory
        del raw
        del events
        del epochs

        # pause for input
        print('\n'+m1+' done >>>\n')
        input('>>> Press enter to continue...')
        

def main():
    epoch_loop()
        
if __name__=='__main__':
    main()
