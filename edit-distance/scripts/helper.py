import os, re, shutil

# List of constants
CSV_EXTENSION = '.csv'
TXT_EXTENSION = '.txt'
VTP_EXTENSION = '.vtp'
PNG_EXTENSION = '.png'

PERSISTENCE_PAIRS_SUFFIX = '-persistent-pairs'
PERSISTENCE_POINTS_SUFFIX = '-persistent-points_data'
PERSISTENCE_CELLS_SUFFIX = '-persistent-cells_data'
FIELD_DATA_SUFFIX = '-field_data'

PAIRS_INFIX = '-pairs-'
TREE_INFIX = '-tree-'
SCREENSHOT_INFIX = '-screenshot-'

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
PAIRS_FOLDER = 'pairs'
TREES_FOLDER = 'trees'
SCRIPTS_FOLDER = 'scripts'
SCREENSHOT_FOLDER = 'screenshots'

PYTHON_COMMAND = 'python'
PARAVIEW_COMMAND = 'paraview'

COMPUTE_SCRIPT = 'compute.py'

# get working directory and add '/' at the end
def cwd():
	return os.path.join(os.getcwd(), '')

# Replace a pattern with another in a file
def replace_wildcard(fname, pat, s_after):
    # first, see if the pattern is even in the file.
    with open(fname) as f:
        if not any(re.search(pat, line) for line in f):
            return # pattern does not occur in file so we are done.

    # pattern is in the file, so perform replace operation.
    with open(fname) as f:
        out_fname = fname + ".tmp"
        out = open(out_fname, "w")
        for line in f:
            out.write(re.sub(pat, s_after, line))
        out.close()
        os.rename(out_fname, fname)

# Return the just the name when path is False
# Return the name appended with the parent path when path is True
def get_file_name(file_path, path = False):
	file_name = os.path.splitext(os.path.basename(file_path))[0]
	parent_path = get_parent_path(file_path)
	if path:
		return join_file_path(parent_path, file_name)
	else:
		return file_name

def get_file_extension(file_path):
	file_basename = os.path.basename(file_path)
	file_text = os.path.splitext(file_basename)
	return file_text[1]

def get_parent_path(file_path):
	return os.path.abspath(os.path.join(file_path, os.pardir))

def get_input_path(file_path):
	return os.path.join(get_parent_path(file_path), INPUT_FOLDER)

# Takes contourForest.TreeType parameter and returns a string
def get_tree_type(tree_type):
	return tree_type.split(' ')[0].lower()

# Get a new filename in the output directory
# This takes in a file from input directory and gives out a string with ../output/file_name
# arguments can be sent in a list to the aforementioned string
# output_folder can be set to False for ../file_name
# pass the folder name if you don't want the default output_folder

def get_output_path(file_path, arguments, output_folder = True, folder_name = None):
	if folder_name is None:
		output_path = os.path.join(get_parent_path(get_parent_path(file_path)), OUTPUT_FOLDER)
	else:
		output_path = os.path.join(get_parent_path(get_parent_path(file_path)), folder_name)

	# Add '/' at the end
	output_path = os.path.join(output_path, '')

	if output_folder == False:
		output_path = get_parent_path(file_path)

	# Magic: Prefix with file name! :facepalm:
	#output_path = os.path.join(output_path, get_file_name(file_path))

	for argument in arguments:
		output_path += argument

	return output_path

def join_file_path(file_path, file_name):
	return os.path.join(file_path, file_name)

def run_python_script(script_name, arguments):
	# python <script_name>
	command = PYTHON_COMMAND + ' ' + script_name
	 	
	# python <script_name> <arguments>
	# Add all the arguments to the command
	for argument in arguments:
		command += ' ' + argument
	os.system(command)
	
# You can't send in arguments here!
def run_paraview_script(script_name):
	# paraview --script= <script_name>
	command = PARAVIEW_COMMAND + ' --script=' + script_name
	os.system(command)

def run_jar(jar_file, arguments):
	# java -jar <jar_file>
	command = JAR_COMMAND + ' ' + jar_file

	# java -jar <jar_file> <arguments>
	for argument in arguments:
		command += ' ' + argument
	os.system(command)

def get_folder(file_path, folder_name = None):
	# This will give you a path with the folder name appended	
	output_path = get_output_path(file_path, [], folder_name = folder_name)
	return output_path

# Create an output folder if it does not exist
def create_output_folder(file_path):
	output_path = get_output_folder(file_path)

	# Check if it exists
	if not os.path.exists(output_path):
		os.makedirs(output_path)

# Delete the output folder
def delete_output_folder(file_path):
	shutil.rmtree(get_output_folder(file_path))

def sort_files(s):
	# seperate on '_'
	timestep, sep, index = s.partition('_')
	# seperate on 'index.extension'
	index, sep, extension = index.partition('.')
	# isnumeric only works for unicode strings
	if unicode(index, 'utf-8').isnumeric():
		return int(index)
	return float('inf')
