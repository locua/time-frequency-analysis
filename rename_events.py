import os
import mne
import pybv
import pandas as pd

def recursive_search(directory, target_string):
    # Iterate over all files and directories in the given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv') and target_string in file:
                file_path = os.path.join(root, file)
                return file_path

    # If the target string is not found in any CSV file
    return None

event_dict_map = {
    1: '1',
    10: '10',
    101: '101',
    109: '109',
    11: '11',
    117: '117',
    20: '20',
    30: '30',
    40: '40',
    5: '5',
    50: '50',
    51: '51',
    52: '52',
    60: '60',
    70: '70',
    80: '80',
    99999: '99999'
}

def relabel_events(session_id, pos_id):
    """Relabel events with cueing data from posner task csv file.

    Args:
        session_id (string): Of the form 'm_01_02' (participant 1, session 2)
        pos_id (string): Of the form 'pos2a' (session 2, posner task a)

    Returns:
        raw (mne.Raw): relabelled data file
    """
    vhdr_file = session_id + '/'+session_id+'_'+pos_id+'.vhdr'
    print('Data file: ', vhdr_file)
    raw = mne.io.read_raw_brainvision(vhdr_file, preload=True, verbose=0)

    #raw.set_eeg_reference(ref_channels='average', projection=True) # remove micro vault error?

    events, events_id = mne.events_from_annotations(raw)

    # Define the target strings
    target_strings = ['1a', '1b', '2a', '2b']
    
    # Specify the directory to search
    directory_path = session_id+'/'
    
    # Perform the search for each target string
    csv_files = {}
    for target_string in target_strings:
        result = recursive_search(directory_path, target_string)
        if result is not None:
            print(f"Found '{target_string}' in file: {result}")
            csv_files[target_string]=result
    
    pos_task = pos_id.strip('pos')
    print("**********", pos_task)

    posner_csv_file = csv_files[pos_task] 
    #print(posner_csv) 

    posner_csv = pd.read_csv(posner_csv_file)
    cols = ["block_name", "cue_dir", "stim_pos", "session", "valid_cue"]
    posner_csv = posner_csv[cols]
    validity = posner_csv[posner_csv["block_name"]=="trials"]["valid_cue"].to_numpy()
    
    # get events
    events, event_id = mne.events_from_annotations(raw) # get events
    idx = 0 # stim even idx increment
    
    for i, e in enumerate(events):
        code=e[2]
        # If stim
        if(code==51):
            # Change code 51 (end of stim) to 52
            events[i][2]=52
        if(code==50):
            if validity[idx]==True:
                # Give code 51 if valid
                events[i][2]=51
            idx+=1

    s_freq = raw.info['sfreq']

    anno_from_events=mne.annotations_from_events(events,
            sfreq=s_freq,
            orig_time=raw.info['meas_date'], 
            event_desc=event_dict_map)

    raw = raw.set_annotations(anno_from_events, verbose=1) 

    return raw
