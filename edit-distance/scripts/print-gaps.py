import os, time
import itertools, sys, pickle, inspect
from helper import *

# Remove the try-catch once testing is complete
try:
	__file__
except:
	sys.argv = [sys.argv[0], 'tv_102', 'tv_103']

colors = ['white', 'khaki', 'seagreen', 'IndianRed', 'mediumpurple', 'darkorange', 'yellowgreen', 'gold', 'orchid2', 'PeachPuff', 'skyblue', 'coral', 'plum', 'darkolivegreen', 'crimson', 'DarkGoldenrod3', 'mediumvioletred', 'sienna3', 'cyan', 'darkseagreen', 'rosybrown', 'honeydew']

def traverse(dictionary, indices):
	indices = printIndices(dictionary, indices)
	if indices is None:
		return
	if len(indices) == 2:
		print 'The matrix has been opened :|'
	if (indices[0] == S_MATRIX_IDENTIFIER):
		traverse(S,indices)
	elif(indices[0] == S1_MATRIX_IDENTIFIER):
		traverse(S1, indices)
	elif(indices[0] == S2_MATRIX_IDENTIFIER):
		traverse(S2, indices)
	else:
		print 'Error!'

def get_label(index, pairs, mappings, labels, costs):
	scalar = round(labels[index], 3)
	label = str(index) + " [" + str(pairs[index]) + "]" + "\\n"
	label += str(mappings[index]) + " " + str() + "\\n"
	label += str(scalar)
	label_attribute = "label=""\"" + label +"\""
	return label_attribute

def get_style(index):
	if index == GAP_NODE:
		style_attribute = "shape=diamond style=filled fillcolor=lightslategray"
	else:
		 style_attribute = "shape=circle style=filled fillcolor=" + colors[index]
	return style_attribute

def get_node(index, pairs, mappings, labels, costs, color_index):
	label_attribute = get_label(index, pairs, mappings, labels, costs)
	style_attribute = get_style(color_index)
	return str(mappings[index]) + " [" + label_attribute  + " " + style_attribute + "]\n"

def get_connectivity(index, parent, mapping):
	if parent[index] != 0:
		node1 = str(mapping[index])
		connector = ' -> '
		node2 = str(mapping[parent[index]])
		line = node2 + connector + node1 + '\n'
		return line
	else:
		return ''

def print_tree():
	file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
	filenames = join_strings([filename1, filename2])
	compare_path = get_output_path(file_path, [COMPARE_PREFIX, filenames, DOT_EXTENSION], folder_name=COMPARE_GRAPHS_FOLDER)
	compare_file = open(compare_path, 'w')

	# print header for first tree
	compare_file.write("digraph T1 {\n")

	# print nodes dictionary for first tree
	for i in range(1, right1[1]+1):
		if map1[i] != GAP_NODE:
			compare_file.write(get_node(i, pairs1, index_mapping1, label1, cost1, i))
		else:
			compare_file.write(get_node(i, pairs1, index_mapping1, label1, cost1, GAP_NODE))
	
	# print nodes connectivity for first tree
	for i in range(1, right1[1]+1):
		compare_file.write(get_connectivity(i, parent1, index_mapping1))

	compare_file.write("}\n\n")

	# print header for second tree
	compare_file.write("digraph T2 {\n")

	# print nodes dictionary for second tree
	for j in range(1, right2[1]+1):
		compare_file.write(get_node(j, pairs2, index_mapping2, label2, cost2, map2[j]))

	# print nodes connectivity for second tree
	for j in range(1, right2[1]+1):
		compare_file.write(get_connectivity(j, parent2, index_mapping2))

	compare_file.write("}\n")

	compare_file.close()

	# get comparison image
	run_shell_script(MAKE_IMAGE_SCRIPT, [compare_path])

def printIndices(dictionary, k):
	try:
		try:
			# parse values from array
			i = k[2]
			j = k[4]
			operation = k[5]
			message = k[6]
			cost = round(k[7],3)

			#print i, j, operation, message, cost

			# according to each operation store associated mapping and cost
			if operation in [RELABEL_IDENTIFIER]:
				# i+1 is relabelled to j+1
				map1[i+1] = j+1
				map2[j+1] = i+1
				cost1[i+1] = cost
				cost2[j+1] = 0
			elif operation in [T1_STARTING_GAP_IDENTIFIER, T1_CONTINUING_GAP_IDENTIFIER]:
				# i+1 is a gap in T1
				map1[i+1] = GAP_NODE
				# Adhitya may be wrong here. Ask Vijay
				cost1[i+1] = cost * -1
			elif operation in [T1_GENERIC_GAP_IDENTIFIER]:
				# i is a gap in T1
				map1[i] = GAP_NODE
				cost1[i] = cost
			elif operation in [T2_STARTING_GAP_IDENTIFIER, T2_CONTINUING_GAP_IDENTIFIER]:
				# j+1 is a gap in T2
				map2[j+1] = GAP_NODE
				cost2[j+1] = cost
			elif operation == T2_GENERIC_GAP_IDENTIFIER:
				# j is a gap in T2
				map2[j] = GAP_NODE
				cost2[j] = cost
			else:
				print 'Govinda'

		except IndexError:
			# This should only happen only during the first call of this function
			pass
			
		next_comparison = dictionary[k[1]][k[2]][k[3]][k[4]]

		return next_comparison
	except:
		#print 'Done! :)'
		return None
	
	
# Get the paths
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))

# Take the names of files as arguments
filename1 =  sys.argv[1]
filename2 = sys.argv[2]

try:
	# Get right-most node for each node
	right1 = get_dictionary(file_path, [filename1, RIGHT_NODE_PREFIX])
	right2 = get_dictionary(file_path, [filename2, RIGHT_NODE_PREFIX])

	# Get parent of each node
	parent1 = get_dictionary(file_path, [filename1, PARENT_NODE_PREFIX])
	parent2 = get_dictionary(file_path, [filename2, PARENT_NODE_PREFIX])

	# Get function value of each node
	label1 = get_dictionary(file_path, [filename1, LABEL_NODE_PREFIX])
	label2 = get_dictionary(file_path, [filename2, LABEL_NODE_PREFIX])

	# Get persistence of each node
	difference1 = get_dictionary(file_path, [filename1, DIFFERENCE_NODE_PREFIX])
	difference2 = get_dictionary(file_path, [filename2, DIFFERENCE_NODE_PREFIX])

	pairs1 = get_dictionary(file_path, [filename1, PAIRS_NODE_PREFIX])
	pairs2 = get_dictionary(file_path, [filename2, PAIRS_NODE_PREFIX])

	index_mapping1 = get_dictionary(file_path, [filename1, MAPPING_NODE_PREFIX])
	index_mapping2 = get_dictionary(file_path, [filename2, MAPPING_NODE_PREFIX])

	# Get size of both the trees
	size1 = len(parent1.keys())
	size2 = len(parent2.keys())

	# How much are we planning to compare?
	extents = [0, 1, right1[1], 1, right2[1]]

	# Get the intermediate matrices
	Q = get_matrix(file_path, [filename1, filename2, Q_IDENTIFIER])
	Q1 = get_matrix(file_path, [filename1, filename2, Q1_IDENTIFIER])
	Q2 = get_matrix(file_path, [filename1, filename2, Q2_IDENTIFIER])

	S = get_matrix(file_path, [filename1, filename2, S_IDENTIFIER])
	S1 = get_matrix(file_path, [filename1, filename2, S1_IDENTIFIER])
	S2 = get_matrix(file_path, [filename1, filename2, S2_IDENTIFIER])

	# store mappings from one tree to another
	map1 = {}
	map2 = {}

	# store costs from one tree to another
	cost1 = {}
	cost2 = {}

except:
	print "Something bad happened :(", filename1, filename2

print "*******"

print filename1, filename2

# Start tracing back from the back
try:
	traverse(S, extents)
	print_tree()
except:
	print 'Govinda'

print "*******"

