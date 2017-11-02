import fileinput
import re
import os
from helper import *
import inspect
from datetime import datetime

# get current file path
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
parent_path = cwd()
data_path = get_input_path(parent_path)
file_list = os.listdir(data_path)

# custom sort for ascending order of timesteps
file_list = sorted(file_list, key=sort_files)

# insert a wildcard at the beginning
file_list.insert(0, 'adhitya.vtk')

num_files = len(file_list)

for i in range(1, num_files):

	compute_file = get_output_path(file_path, [COMPUTE_SCRIPT], folder_name = SCRIPTS_FOLDER)
	replace_wildcard(compute_file, file_list[i-1], file_list[i])

	run_paraview_script(compute_file)

	files_left = num_files - (i+1)
	print file_list[i], 'Done :)', files_left, ' files remaining'

# Back to normalcy :P
replace_wildcard(compute_file, file_list[i], 'adhitya.vtk')
	
	#os.system('python split-make-graph.py '+ 'split-'+file_list[i])
	#print file_list[i]
	

	#if file_list[i].startswith('split-'):
	#	print file_list[i]
	#	os.system('python split-make-graph-restructured.py '+file_list[i])
	#else:
	#	os.system('python join-make-graph.py '+file_list[i])
	# os.system('python make-graph.py '+file_list[i])
	#print i, file_list[i]
