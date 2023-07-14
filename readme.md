
# Ica notes

- `m_01_01`, ica's to remove less obvious (?), 0, 1, 2 removed only
- `m_02_01`, first few ica's are strange...? see screenshots
- `m_02_02`, pos2a 103 stim (50) events in the raw eeg events **NOW CORRECTED!**
  - ALSO: why don't the timestamps for the stim and other events in the raw data match with the csv ones??? :/
  - `m_06_02` has the same issue, 102 stim events (code 50) but 100 in the posner csv... **NOW CORRECTED!**
- `m_04_01`, raw data for posner a and b looks very noisey 
- `m_06_01`, strange ica000 screenshort on desktop

## Missing data parts
- `m_19_02`, posner 2a csv missing; subject 19 may have to be dropped from some analysis
- `m_16_02`, posner 2a csv missing; subject 16 may have to be dropped from some analysis


### new codes after relabelling
| event           | START | END |
| --------------- | ----- | --- |
| start screen    | 10    | 11  |
| end screen      | 20    | 21  |
| continue screen | 30    | 31  |
| trial           | 1     | 101 |
| fc              | 40    | 41  |
| valid stim      | 51    | 52  |
| invalid stim    | 50    | 52  |
| cue_l           | 60    | 61  |
| cue_r           | 70    | 71  |
| cue_c           | 80    | 81  |
