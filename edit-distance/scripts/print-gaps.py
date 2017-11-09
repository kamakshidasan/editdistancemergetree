import os, time
import itertools, sys, pickle, inspect
from helper import *

# Remove the try-catch once testing is complete
try:
	__file__
except:
	sys.argv = [sys.argv[0], 'tv_102', 'tv_103']
	
def printIndices(dictionary, k):
	try:
		try:

			i = k[2]
			j = k[4]
			operation = k[5]
			message = k[6]
			cost = round(k[7],3)

			#print i, j, operation, message, cost

			if operation in [RELABEL_IDENTIFIER]:
				print i+1, 'is relabelled to ', j+1, 'with a cost of ', cost, index_mapping1[i+1], index_mapping2[j+1]
				map1[i+1] = j+1
				map2[j+1] = i+1
				cost1[i+1] = round(label2[i+1] - label1[j+1],3)
				cost2[j+1] = 0
				
			elif operation in [T1_STARTING_GAP_IDENTIFIER, T1_CONTINUING_GAP_IDENTIFIER]:
				print i+1, ' is a gap in T1', 'with a cost of', cost * -1, index_mapping1[i+1]
				map1[i+1] = GAP_NODE
				# I may be wrong here. Ask Vijay
				cost1[i+1] = cost * -1
			elif operation in [T1_GENERIC_GAP_IDENTIFIER]:
				#print i, ' is a gap in T1'
				map1[i] = GAP_NODE
				cost1[i] = cost
			elif operation in [T2_STARTING_GAP_IDENTIFIER, T2_CONTINUING_GAP_IDENTIFIER]:
				print j+1, ' is a gap in T2', 'with a cost of', cost, index_mapping2[j+1]
				map2[j+1] = GAP_NODE
				cost2[j+1] = cost
			elif operation == T2_GENERIC_GAP_IDENTIFIER:
				#print j, ' is a gap in T2'
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
		print 'Done! :)'
		return None

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

def print_tree():
	for i in range(1, right1[1]+1):
		j = map1[i]
		scalar1 = round(label1[i], 3)
		if j != GAP_NODE:
			scalar2 = round(label2[j], 3)
			print i, index_mapping1[i], scalar1, index_mapping1[pairs1[i]]
			#print index_mapping2[j], scalar2, index_mapping2[pairs2[j]], cost1[i]
		else:
			print i, index_mapping1[i], scalar1, index_mapping1[pairs1[i]], cost1[i], GAP_NODE

	print ""

	for j in range(1, right2[1]+1):
		i = map2[j]
		scalar2 = round(label2[j], 3)
		if i != GAP_NODE:
			scalar1 = round(label1[i], 3)
			print j, index_mapping2[j], scalar2, index_mapping2[pairs2[j]]
			#print index_mapping1[i], scalar1, index_mapping1[pairs1[i]], cost2[j]
		else:
			print j, index_mapping2[j], scalar2, index_mapping2[pairs2[j]], cost2[j], GAP_NODE
	
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
traverse(S, extents)
print_tree()
print "*******"
print ""

