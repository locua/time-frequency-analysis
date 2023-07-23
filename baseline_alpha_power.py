
import os
import re
import mne
import datetime
import numpy as np
import pandas as pd

from load_data import load_data

print('* start')

cleaned_dir = '../data_final/'

eeg_files = []

table = {
    'participant':[],
    'session':[],
    'code':[],
    'filename':[],
}
print('* adding file names to table')
for root, dirs, files in os.walk(cleaned_dir):
    initial_baseline = 0
    for file in files:
        # Actives
        if file.endswith('.h5') and 'baseline' in os.path.join(root, file):
            x = os.path.join(root, file)
            eeg_files.append(x)

            directories = root.split('/')

            # Find the index of 'data_final' in the list
            data_final_index = directories.index('data_final')
            subject_dir = directories[data_final_index + 1]

            nums = re.findall(r'\d+', subject_dir)

            subject = nums[0]
            session = nums[1]

            table['participant'].append(subject)
            table['session'].append(session)
            table['filename'].append(x)
            table['code'].append(subject_dir)

table = pd.DataFrame(table)
table = table.sort_values(by='participant', ascending=True)

# Remove the second baseline
# Regular expression pattern to match the "dd-dd-dd" format
pattern = r'\d{2}-\d{2}-\d{2}'

# Define a function to extract the pattern from each row and return the matches as a list
def extract_time(text):
    return re.findall(pattern, text)[0].replace('-', ':')

table['time'] = table['filename'].apply(extract_time)
table['time'] = pd.to_datetime(table['time'])

# Create a new column indicating whether the datetime is the minimum or the maximum
table['baseline'] = np.where(table['time'] == table.groupby('code')['time'].transform('min'), 1,
                            np.where(table['time'] == table.groupby('code')['time'].transform('max'), 2, None))

baseline1 = table[table['baseline']==1]

print('* looping through and getting alpha power')

def get_psd_power(m_raw):
    spectrum = m_raw.compute_psd('welch', fmin=8, fmax=12)
    return spectrum.to_data_frame()


def get_psd_power_normed(ep):
    spectrum = ep.compute_psd('welch', fmin=8, fmax=12)
    alpha =  spectrum.to_data_frame().drop(columns=['freq']).melt().value
    mean_alpha =  spectrum.to_data_frame().drop(columns=['freq']).melt().value.mean()
    std_alpha = spectrum.to_data_frame().drop(columns=['freq']).melt().value.std()
    centered_alpha_power = alpha - mean_alpha
    normed_alpha_power = centered_alpha_power / std_alpha
    return normed_alpha_power.mean()

def get_avg_power(h5file, subject, session):
    """Return average power for h5 eeg data file.
    """
    regions = {
        'left occipital' : ["O1"],
        'right occipital' : ["O2"],
        'left parietal-occipital':["PO7", "PO3"],
        'right parietal-occipital':["PO8", "PO4"],
        'left parietal' : ["P7", "P5", "P3", "P1"],
        'right parietal' : ["P2", "P4", "P6", "P8"],
        'right O, PO and CP' : ["P2", "P4", "P6", "P8", "PO8", "PO4", "O2", "CP6", "CP4", "CP2"],
        'left O, PO and CP' : ["P7", "P5", "P3", "P1", "PO7", "PO3", "O1", "CP5", "CP3", "CP1"]
    }


    df1, fs, channels, p_names = load_data(h5file)
    df1['sample'] = df1.index

    # get baseline blocks and block numbers
    df1_all_bl = df1.loc[df1['block_name'].str.contains("baseline", case=False)]
    df1_all_bl = df1_all_bl.loc[~df1_all_bl['block_name'].str.contains("start", case=False)]
    baseline_blocks = df1_all_bl['block_number'].unique()

    output = {
        'baseline type':[],
        'ROI':[],
        'participant':[],
        'power':[],
        'session':[]
    }

    for block in baseline_blocks:
        for key, value in regions.items():
            df1_bl = df1_all_bl.loc[df1_all_bl["block_number"] == block]
            baseline_name = df1_bl["block_name"].unique()[0]
            # Drop non eeg data
            eeg_data = df1_bl.drop(
                columns=['signal_left', 'signal_right', 'signal_AAI', 'events', 'reward', 'choice', 'answer', 'probe',
                         'block_name', 'chunk_n', 'cue', 'posner_stim', 'posner_time', 'response_data',
                         'block_number', 'sample'])
            eeg_data = eeg_data[value]

            # create an MNE info
            m_info = mne.create_info(ch_names=list(eeg_data.columns), sfreq=fs, ch_types=['eeg' for ch in list(eeg_data.columns)])

            # Set the montage (THIS IS FROM roi_spatial_filter.py)
            standard_montage = mne.channels.make_standard_montage(kind='standard_1020')
            standard_montage_names = [name.upper() for name in standard_montage.ch_names]
            for j, channel in enumerate(eeg_data.columns):
                try:
                    # make montage names uppercase to match own data
                    standard_montage.ch_names[standard_montage_names.index(channel.upper())] = channel.upper()
                except ValueError as e:
                    print(f"ERROR ENCOUNTERED: {e}")
            m_info.set_montage(standard_montage, on_missing='ignore')

            # Create the mne raw object with eeg data
            m_raw = mne.io.RawArray(eeg_data.T, m_info, first_samp=0, copy='auto', verbose=None)

            power = get_psd_power_normed(m_raw)
            roi_name = key
            output['baseline type'].append(baseline_name)
            output['ROI'].append(roi_name)
            output['participant'].append(subject)
            output['power'].append(power)
            output['session'].append(session)

    return pd.DataFrame(output)

powers = []
count = 0

for index, row in baseline1.iterrows():
    filename = row.filename
    subject = row.participant
    session = row.session
    power = get_avg_power(filename, subject, session)
    powers.append(power)

    # if(count>1):
    #     break
    # count+=1


merged_powers = pd.concat(powers, ignore_index=True, sort=False)

baseline1['session'] = baseline1['session'].astype(float)
baseline1['participant'] = baseline1['participant'].astype(float)
merged_powers['participant'] = merged_powers['participant'].astype(float)
merged_powers['session'] = merged_powers['session'].astype(float)

print(baseline1.dtypes)
print(merged_powers.dtypes)

baselines = pd.merge(baseline1, merged_powers, on=['participant', 'session'])

# print(second_merge.drop(columns=['filename']))

baselines = baselines.drop(columns=['filename'])

baselines.to_csv('baseline_powers.csv', index=False)




