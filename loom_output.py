import sys
sys.path.append(sys.argv[3])
from signal_udfs import unpickle
import pandas as pd

file_handle = sys.argv[1]
save_handle = sys.argv[2]

#Unpack data dict pickles
pkl_files = unpickle(sys.argv[4:])

#velocity_trial_dict = pkl_files[0]
shelter_time_dict = pkl_files[1]
freeze_trial_dict = pkl_files[2]

#Remove trial traces from freeze_df output
remove_keys = ['Time', 'Velocity', 'Base Velocity', 'Loom Velocity', 'Post Velocity']
trial_dict = {name:[] for name in remove_keys}

for name in remove_keys:
    removed = freeze_trial_dict.pop(name)

#Create output dataframes of dictionaries
#velocity_df = pd.DataFrame.from_dict(velocity_trial_dict)
shelter_df = pd.DataFrame.from_dict(shelter_time_dict)
freeze_df = pd.DataFrame.from_dict(freeze_trial_dict) #contains data for velcity_df


#Slap dataframes together and write as .csv
output_df = pd.concat([freeze_df, shelter_df], axis = 1, ignore_index = False)
output_df.to_csv(save_handle[:-4] + '_main_calc_output.csv', index = False)
