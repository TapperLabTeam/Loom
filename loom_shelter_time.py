import pickle
import sys
import numpy as np
import pandas as pd
import warnings

def convert_to_ints(str_list):
    arr = np.array(str_list)
    arr[arr == '-'] = 0
    num_arr = arr.astype('int')
    return num_arr

def get_next_switch_time(ts1):
    ts1_idx = np.where(np.array(import_data['Time']) >= ts1)[0][0] # get the index where the input timestamp occurs
    ts2_idx = loc_switch_idxs[loc_switch_idxs > ts1_idx][0] # get the index of the next location switch
    switch_ts = import_data['Time'][ts2_idx] # output the time at the switch index
    return switch_ts

udf_path = sys.argv[3]
sys.path.append(udf_path)
from signal_udfs import unpickle

file_handle = sys.argv[1]
save_handle = sys.argv[2]

import_pkl = unpickle(sys.argv[4:])
import_data = import_pkl[0]

# convert '-' strings to zero reate array of the indexes where location changes value
detected = convert_to_ints(import_data['Arena'])
loc_switch_idxs = np.where(np.diff(detected.astype('int'),prepend=np.nan))[0]

shelter_latencies = []
in_shelter_start_times =[]
times_in_shelter = []
shelter_out_times = []
poke_outs = []

for loom_num, timestamp in enumerate(import_data['Loom TS']):
    # get index of ethovision time closest to manual timestamp
    loom_time_idx = np.where(np.array(import_data['Time']) >= timestamp)[0][0]
   
    # get index of first location switch after loom and confirm is from detected to undetected
    shelter_start_idx = loc_switch_idxs[loc_switch_idxs >= loom_time_idx][0]
    assert import_data['Arena'][shelter_start_idx-1] == 1
    assert import_data['Arena'][shelter_start_idx] != 1
   
    # add values to lists
    in_shelter_start_time = import_data['Time'][shelter_start_idx]
    shelter_latency = in_shelter_start_time - timestamp
   
    if shelter_latency > 90:
        # exclude times where greater than 90s between loom and reaching the shelter
        in_shelter_start_times.append(float('nan'))
        shelter_latencies.append(float('nan'))
        warnings.warn(f'{int(shelter_latency)}s latency to shelter for loom #{int(loom_num)}. Values set to NaN.')
    else:
        in_shelter_start_times.append(in_shelter_start_time)
        shelter_latencies.append(in_shelter_start_time - timestamp)


for loom_num, shelter_ts in enumerate(in_shelter_start_times):
    # get first time mouse is detected in arena again
    out_shelt_ts = get_next_switch_time(shelter_ts)
    reenter_ts = get_next_switch_time(out_shelt_ts)
    poke_out = 0 # track how many times mouse pokes out of shelter
    time_out_of_shelter = reenter_ts - out_shelt_ts
   
    # keep looping until an "out of shelter" event longer than 1s occurs
    while time_out_of_shelter < 1:
        next_out_ts = get_next_switch_time(reenter_ts)
        next_reenter = get_next_switch_time(next_out_ts)
       
        # reset values
        out_shelt_ts = next_out_ts
        reenter_ts = next_reenter
        poke_out = poke_out + 1  
        time_out_of_shelter = next_reenter - next_out_ts  
       
    time_in_shelter = out_shelt_ts - shelter_ts
    times_in_shelter.append(time_in_shelter)
    poke_outs.append(poke_out)

#Put shelter_latencies and time_in_shelter in dict and dump pickle for output
shelter_dict = {'Latency to Shelter': [], 'Time in Shelter': []}
shelter_dict['Latency to Shelter'] = shelter_latencies
shelter_dict['Time in Shelter'] = times_in_shelter
pickle.dump(shelter_dict, open('shelter_time_dict.pkl','wb'))
