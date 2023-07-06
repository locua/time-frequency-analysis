import mne
import pandas as pd
import pybv

def relabel_events(session_id, pos_id):
    vhdr_file = session_id + '/'+session_id+'_'+pos_id+'.vhdr'
    print('Data file: ', vhdr_file)
    raw = mne.io.read_raw_brainvision(vhdr_file, preload=True)


