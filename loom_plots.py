import sys
sys.path.append(sys.argv[3])
from signal_udfs import unpickle
from signal_udfs import plot_all_signals
import matplotlib.pyplot as plt

file_handle = sys.argv[1]
save_handle = sys.argv[2]

pkl_files = unpickle(sys.argv[4:])

import_data = pkl_files[0]
trial_dict = pkl_files[1]

#Plot full velocity trace
plt.plot(import_data['Time'], import_data['Velocity'])
plt.xlabel('Time (s)')
plt.ylabel('Velocity (cm/s)')
plt.savefig(save_handle[:-4] + '_full_velocity_trace.png')
plt.close()

#Plot loom trial velocity traces
plot_all_signals(trial_dict['Time'], trial_dict['Velocity'], 'Time (s)', 'Velocity (cm/s)', save_handle[:-4] + '_trial_velocity_traces')
