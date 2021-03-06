import os, re, shutil, pickle, inspect, csv, sys, math

# List of constants
CSV_EXTENSION = '.csv'
TXT_EXTENSION = '.txt'
BIN_EXTENSION = '.bin'
VTP_EXTENSION = '.vtp'
PNG_EXTENSION = '.png'
DOT_EXTENSION = '.dot'
JT_EXTENSION = '.jt'

PAIRS_INFIX = '-pairs-'
TREE_INFIX = '-tree-'
NODES_INFIX = '-nodes-'
ARCS_INFIX = '-arcs-'
SCREENSHOT_INFIX = '-screenshot-'
COMPARE_PREFIX = 'compare-'
EDIT_DISTANCE_RESULT = 'results'

RIGHT_NODE_SUFFIX = '-right'
PARENT_NODE_SUFFIX = '-parent'
LABEL_NODE_SUFFIX = '-labels'
DIFFERENCE_NODE_SUFFIX = '-difference'
PAIRS_NODE_SUFFIX = '-pairs'
MAPPING_NODE_SUFFIX = '-mapping'

TREE_TYPE_SPLIT = 'split'

Q_IDENTIFIER = '-Q'
Q1_IDENTIFIER = '-Q1'
Q2_IDENTIFIER = '-Q2'

S_IDENTIFIER = '-S'
S1_IDENTIFIER = '-S1'
S2_IDENTIFIER = '-S2'

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
PAIRS_FOLDER = 'pairs'
TREES_FOLDER = 'trees'
SCRIPTS_FOLDER = 'scripts'
SCREENSHOT_FOLDER = 'screenshots'
INTERMEDIATE_FOLDER = 'intermediate'
PERSISTENCE_FOLDER = 'persistence'
DICTIONARY_FOLDER = 'dictionary'
RESULTS_FOLDER = 'results'
MATRICES_FOLDER = 'matrices'
IMAGES_FOLDER = 'images'
GRAPHS_FOLDER = 'graph'
COMPARE_GRAPHS_FOLDER = 'compare-graphs'
COMPARE_IMAGES_FOLDER = 'compare-images'
MERGED_GRAPHS_FOLDER = 'merged-graphs'
MERGED_IMAGES_FOLDER = 'merged-images'
DEBUG_FOLDER = 'debug'
JT_FOLDER = 'jt'
CLIQUE_GRAPHS_FOLDER = 'clique-graphs'

PYTHON_COMMAND = 'python'
PARAVIEW_COMMAND = 'paraview'

COMPUTE_SCRIPT = 'compute.py'
SPLIT_MAKE_GRAPH_SCRIPT = 'split-make-graph.py'
SPLIT_MAKE_GRAPH_LEFT_SCRIPT = 'split-make-graph-left.py'
MAKE_IMAGE_SCRIPT = 'make-image.sh'
MAKE_STABLE_SCRIPT = 'make-stable.py'
GENERATE_JT_FILES_SCRIPT = 'generate-jt-files.py'

INFINITY = float('inf')

UNKNOWN_COST = float('-inf')
RELABEL_IDENTIFIER = 0

T1_STARTING_GAP_IDENTIFIER = 1
T1_CONTINUING_GAP_IDENTIFIER = 2
T1_GENERIC_GAP_IDENTIFIER = 3
T1_RIGHT_GAP_IDENTIFIER = 4

T2_STARTING_GAP_IDENTIFIER = 5
T2_CONTINUING_GAP_IDENTIFIER = 6
T2_GENERIC_GAP_IDENTIFIER = 7
T2_RIGHT_GAP_IDENTIFIER = 8

S_MATRIX_IDENTIFIER = 0
S1_MATRIX_IDENTIFIER = 1
S2_MATRIX_IDENTIFIER = 2

GAP_NODE = -1

# get working directory and add '/' at the end
def cwd():
	return os.path.join(os.getcwd(), '')

# get path of current file
def current_path():
	return os.path.abspath(inspect.getfile(inspect.currentframe()))

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

def get_folder(name):
	return get_output_path(cwd(), [], folder_name=name)

def get_input_path(file_path):
	return os.path.join(get_parent_path(file_path), INPUT_FOLDER)

# Takes contourForest.TreeType parameter and returns a string
def get_tree_type(tree_type):
	return tree_type.split(' ')[0].lower()

# join two strings
def join_strings(strings):
	return '-'.join(strings)

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
	
	print command
	os.system(command)
	
# You can't send in arguments here!
def run_paraview_script(script_name):
	# paraview --script= <script_name>
	command = PARAVIEW_COMMAND + ' --script=' + script_name
	os.system(command)

def run_shell_script(script_name, arguments):
	command = './' + script_name

	for argument in arguments:
		command += ' ' + argument
	
	os.system(command)

def run_jar(jar_file, arguments):
	# java -jar <jar_file>
	command = JAR_COMMAND + ' ' + jar_file

	# java -jar <jar_file> <arguments>
	for argument in arguments:
		command += ' ' + argument
	os.system(command)

def get_dictionary(file_path, arguments):
	# extension is always BIN
	arguments.append(BIN_EXTENSION)
	dictionary_path = get_output_path(file_path, arguments, folder_name = DICTIONARY_FOLDER)

	with open(dictionary_path, 'rb') as handle:
		current_dictionary = pickle.loads(handle.read())
	
	return current_dictionary

def get_matrix(file_path, arguments):
	# extension is always BIN
	arguments.append(BIN_EXTENSION)
	
	# combine the filenames together
	arguments[0:2] = [join_strings(arguments[0:2])]

	dictionary_path = get_output_path(file_path, arguments, folder_name = MATRICES_FOLDER)

	with open(dictionary_path, 'rb') as handle:
		current_dictionary = pickle.loads(handle.read())
	
	return current_dictionary


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

# used in run: sort files according to characters and numeric
def sort_files(s):
	# seperate on '_'
	timestep, sep, index = s.partition('_')
	# seperate on 'index.extension'
	index, sep, extension = index.partition('.')
	# isnumeric only works for unicode strings
	if unicode(index, 'utf-8').isnumeric():
		return int(index)
	return float('inf')

# Pretty print the time taken
def pretty_print_time(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	time_taken =  "%d:%02d:%02d" % (h, m, s)
	return time_taken

# save dictionary to file
def save_dictionary(dictionary, file_name, identifier):
	dictionary_file_arguments = [file_name, identifier, BIN_EXTENSION]
	dictionary_file_path = get_output_path(current_path(), dictionary_file_arguments, folder_name = DICTIONARY_FOLDER)
	with open(dictionary_file_path, 'wb') as handle:
		pickle.dump(dictionary, handle)

# used in edit-distance to save intermediate matrices
def save_matrix(dictionary, filenames, identifier):
	matrix_file_arguments = [join_strings(filenames), identifier, BIN_EXTENSION]
	matrix_file_path = get_output_path(current_path(), matrix_file_arguments, folder_name = MATRICES_FOLDER)
	with open(matrix_file_path, 'wb') as handle:
		pickle.dump(dictionary, handle)

def find_coords(vertex_index):
	x_dim = y_dim = z_dim = 300
	z = vertex_index/(x_dim*y_dim)
	xy = vertex_index - z * x_dim * y_dim
	y = xy/x_dim
	x = xy - y * x_dim
	return (x, y, z)

def find_distance(vertex_index):
	[x, y, z] = find_coords(vertex_index)
	return math.sqrt(x*x + y*y + z*z)

# used for printing in split-make-graph-*.py
def get_label(index, pairs, mappings, labels):
	scalar = round(labels[index], 3)
	label = str(index) + " [" + str(pairs[index]) + "]" + "\\n"
	label += str(mappings[index]) + "\\n"
	label += str(scalar)
	label_attribute = "label=""\"" + label +"\""
	return label_attribute

def get_node(index, pairs, mappings, labels):
	label_attribute = get_label(index, pairs, mappings, labels)
	return str(mappings[index]) + " [" + label_attribute + "]\n"

def get_connectivity(index, parent, mapping):
	if parent[index] != 0:
		node1 = str(mapping[index])
		connector = ' -> '
		node2 = str(mapping[parent[index]])
		line = node2 + connector + node1 + '\n'
		return line
	else:
		return ''

# write tree for unordered traversal
def get_jt_node(index, pairs, mapping, labels, parent, children, number_children):
	vertex_index = mapping[index]
	if parent[index] == 0:
		parent_index = -1
	else:
		parent_index = mapping[parent[index]]
	pair_index = mapping[pairs[index]]
	max_node_index = -1 # Not used by Talha
	scalar = labels[index]
	number_children = number_children[index]
	children_indices = children[index]

	node_arguments = [index, vertex_index, parent_index, pair_index, max_node_index, scalar]
	if number_children != 0:
		node_arguments.append(number_children)
		for child in children_indices:
			node_arguments.append(child)

	return  ' '.join(str(x) for x in node_arguments) + '\n'
