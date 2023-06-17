import sys
import pandas as pd
import pickle

file_handle = sys.argv[1]
save_handle = sys.argv[2]

#Import data from .csv input file
import_data = {'Time': [], 'Velocity': [], 'Arena': [],'Shelter': [], 'Loom TS': [], 'Shelter In TS': [], 'Shelter Out TS': [], 'Shelter Visit Length': []}

time = []
velocity = []
arena = []
shelter = []
loom_ts = []
shelter_in_ts = []
shelter_out_ts = []
shelter_visit = []

for line_num, line in enumerate(open(file_handle)):
    line = line.strip().split(',')
    if line_num > 0:
        for point_num, point in enumerate(line):
            if point_num == 0:
                time.append(float(point))
            if point_num == 1:
                if point != '-':
                    velocity.append(float(point))
                else:
                    velocity.append('NaN')
            if point_num == 2:
                if point != '-':
                    arena.append(int(point))
                else:
                    arena.append(point)
            if point_num == 3:
                if point != '-':
                    shelter.append(int(point))
                else:
                    shelter.append(point)
            if point_num == 4:
                if point != '':
                    loom_ts.append(float(point))
            if point_num == 5:
                if point != 0 and point != '':
                    shelter_in_ts.append(float(point))
            if point_num == 6:
                if point != 0 and point != '':
                    shelter_out_ts.append(float(point))
            if point_num == 7:
                if point != 0 and point != '':
                 shelter_visit.append(float(point))

import_data['Time'] = time
import_data['Velocity'] = velocity
import_data['Arena'] = arena
import_data['Loom TS'] = loom_ts
import_data['Shelter'] = shelter
import_data['Shelter In TS'] = shelter_in_ts
import_data['Shelter Out TS'] = shelter_out_ts
import_data['Shelter Visit Length'] = shelter_visit
            
#Interpolate missing data using linear interpretation.
interp_df = pd.DataFrame.from_dict(import_data['Velocity'])
interp_df = interp_df.astype('float')
interp_df_2 = interp_df.interpolate(method = 'linear', limit_direction = 'both')

import_data['Velocity'] = interp_df_2[0].values.tolist()

pickle.dump(import_data, open('import_data.pkl','wb'))
