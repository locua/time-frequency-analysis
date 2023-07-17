#!/usr/bin/env python

import os
import re
import sys
import mne
import numpy as np


def find_files(folder_path, extension):
    matching_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(extension):
                matching_files.append(os.path.join(root, file))
    return matching_files

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

    extension = ".vhdr"
    my_dir = './ica_notebooks/cleaned'
    matching_files = find_files(my_dir, extension)

    for file_path in matching_files:

        m1 = re.search(r'[^/]*(?=.vhdr)', file_path)
        save_name = m1.group()

        #### SOME mne loading and EPOCH REMOVAL CODE ####
        raw = mne.io.read_raw(file_path, preload=True)
        events = mne.events_from_annotations(raw, event_map)
    
        event_id = {'Comment/60': 60,
                'Comment/70':70,
                'Comment/80':80}
        tmin=0
        tmax=6
    
        epochs = mne.Epochs(raw, 
                events[0], 
                event_id, 
                tmin, 
                tmax, 
                preload=True, 
                baseline=(0,0))
    
        epochs.plot()
        input('Continue?')
        epochs.plot_drop_log()
        save_name = str(save_name)
        save_name+='-epo.fif'
        save_name = os.path.join('./saved_epochs',save_name) 
        epochs.save(save_name, overwrite=False)
        #### END ####
        
        # Clean up memory
        del raw
        del events
        del epochs

        # pause for input
        print('\n'+save_name+' done >>>\n')
        input('>>> Press enter to continue...')
        
def test():
    print('TEST')
    #raw = mne.io.read_raw('./ica_notebooks/cleaned/m_01_01/m_01_01_pos1a.vhdr')
    epochs = mne.read_epochs('./saved_epochs/m_01_01_pos1a-epo.fif')
    
    epochs=epochs.pick_types(eeg=True)
    epochs.plot()
    input('Running test...')
    del epochs
    del raw

def main():
    if sys.argv[1]=='test':
        test()
    else:
        epoch_loop()
        
if __name__=='__main__':
    main()
