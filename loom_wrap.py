import os
import subprocess

#OPTIONS
input_folder = 'C:/Users/Tim/Documents/Python/Loom/input_folder'
output_folder = 'C:/Users/Tim/Documents/Python/Loom/output_folder'
udf_path = 'C:/Users/Tim/Documents/Python/UDFs'

#Main wrapper loop
input_files = os.listdir(input_folder)

for file_name in input_files:
	print('Processing: ' + file_name + '...')
	file_handle = input_folder + '/' + file_name
	save_handle = output_folder + '/' + file_name
	subprocess.call(['python', 'loom_import.py', file_handle, save_handle])
	subprocess.call(['python', 'loom_velocity_trials.py', file_handle, save_handle, udf_path, 'import_data.pkl'])
	subprocess.call(['python', 'loom_freeze_calc.py', file_handle, save_handle, udf_path, 'velocity_trial_dict.pkl'])
	subprocess.call(['python', 'loom_plots.py', file_handle, save_handle, udf_path, 'import_data.pkl', 'velocity_trial_dict.pkl'])
	subprocess.call(['python', 'loom_shelter_time.py', file_handle, save_handle, udf_path, 'import_data.pkl'])
	subprocess.call(['python', 'loom_output.py', file_handle, save_handle, udf_path, 'velocity_trial_dict.pkl', 'shelter_time_dict.pkl', 'freeze_trial_dict.pkl'])

print('Done')
