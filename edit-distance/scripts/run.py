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

#num_files = len(file_list)
num_files = 200

for i in range(1, num_files+1):

	#compute_file = get_output_path(file_path, [COMPUTE_SCRIPT], folder_name = SCRIPTS_FOLDER)
	#replace_wildcard(compute_file, file_list[i-1], file_list[i])
	#run_paraview_script(compute_file)

	split_make_graph_file = get_output_path(file_path, [SPLIT_MAKE_GRAPH_SCRIPT], folder_name = SCRIPTS_FOLDER)
	run_python_script(split_make_graph_file, [file_list[i]])
	
	make_stable_file = get_output_path(file_path, [MAKE_STABLE_SCRIPT], folder_name = SCRIPTS_FOLDER)
	run_python_script(make_stable_file, [file_list[i]])

	generate_jt_file = get_output_path(file_path, [GENERATE_JT_FILES_SCRIPT], folder_name = SCRIPTS_FOLDER)
	run_python_script(generate_jt_file, [file_list[i]])

	files_left = num_files - i
	print file_list[i], 'Done :)', files_left, ' files remaining'



# Back to normalcy :P
#replace_wildcard(compute_file, file_list[i], 'adhitya.vtk')
