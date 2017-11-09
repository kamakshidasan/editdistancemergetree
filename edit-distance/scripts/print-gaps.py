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
			print round(k[6],3), k[5]
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
		print 'Something is about to happen! :|'
	if (indices[0] == 0):
		traverse(S,indices)
	elif(indices[0] == 1):
		traverse(S1, indices)
	elif(indices[0] == 2):
		traverse(S2, indices)
	else:
		print 'Error!'
	
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

	mapping1 = get_dictionary(file_path, [filename1, MAPPING_NODE_PREFIX])
	mapping2 = get_dictionary(file_path, [filename2, MAPPING_NODE_PREFIX])

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

except:
	print "Something bad happened :(", filename1, filename2
	
print filename1, filename2

# Start tracing back from the back
traverse(S, extents)

