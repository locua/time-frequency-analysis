import mne
import pandas as pd
import pybv

def test():
    print('Hello!')

def relabel_events(session_id, pos_id):
    print('Data file: ', session_id + '/'+session_id+'_'+pos_id+'.vhdr')
    raw = mne.io.read_raw_brainvision(session_id + '/'+session_id+'_'+pos_id+'.vhdr', preload=True)   

    pass
