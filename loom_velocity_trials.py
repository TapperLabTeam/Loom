import pickle
import sys
import matplotlib.pyplot as plt
udf_path = sys.argv[3]
sys.path.append(udf_path)
from signal_udfs import unpickle
from signal_udfs import plot_all_signals

file_handle = sys.argv[1]
save_handle = sys.argv[2]


import_pkl = unpickle(sys.argv[4:])
import_data = import_pkl[0]

#Set up data structures for holding individual trial data
time = [[] for x in range(len(import_data['Loom TS']))]
norm_time = [[] for x in range(len(import_data['Loom TS']))]
velocity = [[] for x in range(len(import_data['Loom TS']))]
names = ['Trial ' + str(x + 1) for x in range(len(import_data['Loom TS']))]

base_vel = [[] for x in range(len(import_data['Loom TS']))]
loom_vel = [[] for x in range(len(import_data['Loom TS']))]
post_vel = [[] for x in range(len(import_data['Loom TS']))]

keynames = ['Time', 'Velocity', 'Base Velocity', 'Loom Velocity', 'Post Velocity', 'Names']
trial_dict = {name: [] for name in keynames}

#Extract trial data based on looming timestamps
for ts_num, ts in enumerate(import_data['Loom TS']):
    for point_num, point in enumerate(import_data['Time']):
        if point >= (ts - 8) and point < ts:
            norm_time[ts_num].append(point - ts)
            velocity[ts_num].append(import_data['Velocity'][point_num])
            base_vel[ts_num].append(import_data['Velocity'][point_num])
        if point >= ts and point <= ts + 8:
            norm_time[ts_num].append(point - ts)
            velocity[ts_num].append(import_data['Velocity'][point_num])
            loom_vel[ts_num].append(import_data['Velocity'][point_num])
        if point > ts + 8 and point <= ts + 18:
            norm_time[ts_num].append(point - ts)
            velocity[ts_num].append(import_data['Velocity'][point_num])
            post_vel[ts_num].append(import_data['Velocity'][point_num])

#Assign extracted trial data to trial_dict, plot, and save .pkl
trial_dict['Time'] = norm_time
trial_dict['Velocity'] = velocity
trial_dict['Base Velocity'] = base_vel
trial_dict['Loom Velocity'] = loom_vel
trial_dict['Post Velocity'] = post_vel
trial_dict['Names'] = names

pickle.dump(trial_dict, open('velocity_trial_dict.pkl','wb'))
