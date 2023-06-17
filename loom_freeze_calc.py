import sys
sys.path.append(sys.argv[3])
from signal_udfs import unpickle
from loom_udfs import freeze_time_calc
import statistics
import math
import pandas as pd
import pickle

file_handle = sys.argv[1]
save_handle = sys.argv[2]

pkl_files = unpickle(sys.argv[4:])
trial_dict = pkl_files[0]

#Calculate avg baseline velocity, peak loom velocity, and average post-loom velocity
base_vel_avg = []
loom_vel_peak = []
post_vel_avg = []

for trial_num, trial in enumerate(trial_dict['Base Velocity']):
    base_vel_avg.append(statistics.mean(trial))
    loom_vel_peak.append(max(trial_dict['Loom Velocity'][trial_num]))
    post_vel_avg.append(statistics.mean(trial_dict['Post Velocity'][trial_num]))

trial_dict['Mean Base Velocity'] = base_vel_avg
trial_dict['Peak Loom Velocity'] = loom_vel_peak
trial_dict['Mean Post Velocity'] = post_vel_avg

#Calculate locomotor speed sindex (LSI) for loom stimuli and post-looms
loom_lsi = []
post_lsi = []

for trial_num, trial in enumerate(trial_dict['Mean Base Velocity']):
    loom_lsi.append(math.log10(trial_dict['Peak Loom Velocity'][trial_num]/trial))
    post_lsi.append(math.log10(trial_dict['Mean Post Velocity'][trial_num]/trial))

trial_dict['Loom LSI'] = loom_lsi
trial_dict['Post LSI'] = post_lsi

#Determine type of freezing
freeze_type = []

for trial_num, trial in enumerate(trial_dict['Loom LSI']):
    if trial > 0 and trial_dict['Post LSI'][trial_num] < 0:
        freeze_type.append('Escape Freeze')
    if trial < 0 and trial_dict['Post LSI'][trial_num] < 0:
        freeze_type.append('Freeze Only')
    if trial > 0 and trial_dict['Post LSI'][trial_num] > 0:
        freeze_type.append('Undetermined')
    if trial < 0 and trial_dict['Post LSI'][trial_num] > 0:
        freeze_type.append('Undetermined')

trial_dict['Freeze Type'] = freeze_type

#Determine time spent freezing defined as anything below baseline velocity. (NOTE: may need a time frozen criterion to determine freezing more accurately)
names = ['Base Freeze Time', 'Loom Freeze Time', 'Post Freeze Time']
for name in names:
    trial_dict[name] = [[] for x in range(len(trial_dict['Time']))]
    
for trial_num, trial in enumerate(trial_dict['Base Velocity']):
    trial_dict['Base Freeze Time'][trial_num] = freeze_time_calc(trial_dict['Time'][trial_num], trial, trial_dict['Mean Base Velocity'][trial_num])
    trial_dict['Loom Freeze Time'][trial_num] = freeze_time_calc(trial_dict['Time'][trial_num], trial_dict['Loom Velocity'][trial_num], trial_dict['Mean Base Velocity'][trial_num])
    trial_dict['Post Freeze Time'][trial_num] = freeze_time_calc(trial_dict['Time'][trial_num], trial_dict['Post Velocity'][trial_num], trial_dict['Mean Base Velocity'][trial_num])

#Update trial_dict.pkl file
pickle.dump(trial_dict, open('freeze_trial_dict.pkl','wb'))
