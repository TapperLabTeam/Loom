# Loom
Analyzes behavioral data from looming assay video tracked in Ethovision.

Instructions:
1. Create an "input_folder" and "output_folder" and update the file paths in "loom_wrap.py."
2. Update the file path to the "signal_udfs.py" in "loom_wrap.py."
3. Copy .csv file to "input_folder."
4. .csv files should be formatted thusly: row 1 = row titles, column 1 = ethovision timestamps (seconds), column 2 = velocity trace, column 3 = binary arena detection, column 4 = binary shelter detection, column 5 = start times for looming events (seconds).
5. Run "loom_wrap.py" to execute program.
