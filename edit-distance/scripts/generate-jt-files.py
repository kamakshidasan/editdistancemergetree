# This file is only present because Talha spoilt my fun of implementing unordered tree comparison

from helper import *

# Take the names of files as arguments
file_name =  sys.argv[1]
filename = get_file_name(file_name)

# Get the paths
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
dictionary = get_output_path(file_path, [filename], folder_name = DICTIONARY_FOLDER)
results_path = get_output_path(file_path, [EDIT_DISTANCE_RESULT, CSV_EXTENSION], folder_name = RESULTS_FOLDER)

# Get right-most node for each node
rights = get_dictionary(file_path, [filename, RIGHT_NODE_SUFFIX])

# Get parent of each node
parents = get_dictionary(file_path, [filename, PARENT_NODE_SUFFIX])

# Get function value of each node
labels = get_dictionary(file_path, [filename, LABEL_NODE_SUFFIX])

# Get persistence of each node
differences = get_dictionary(file_path, [filename, DIFFERENCE_NODE_SUFFIX])

# Get pairs of each node
pairs = get_dictionary(file_path, [filename, PAIRS_NODE_SUFFIX])

# Get inverse index map of each node
inverse_index_map = get_dictionary(file_path, [filename, MAPPING_NODE_SUFFIX])

# Get size of both the trees
size = len(parents.keys())

# Initialize children dictionary - this is not computed earlier
children = {}
for node in range(0, size+1):
	children[node] = []

# Store an array with the number of children
number_children = [0] * (size+1)

# Populate the children dictionary and list
for child in parents.keys():
	parent = parents[child]
	if parent != 0:
		child = inverse_index_map[child]
		children[parent].append(child)
		number_children[parent] += 1

# write data to jt file
jt_file_path = get_output_path(file_path, [filename, JT_EXTENSION], folder_name = JT_FOLDER)
jt_file = open(jt_file_path, 'w')
jt_file.write(str(size)+ '\n')

for node in inverse_index_map.keys():
		jt_file.write(get_jt_node(node, pairs, inverse_index_map, labels, parents, children, number_children))

jt_file.close()
