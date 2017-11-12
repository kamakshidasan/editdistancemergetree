import csv, sys
from helper import *

file_name = (sys.argv[1]).split('.')[0]
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
tree_type = TREE_TYPE_SPLIT

scalars = {}
visited= {}
adjacency = {}
index_map = {}
pairs = {}
inverse_index_map = {}

index = 1

right_dictionary = {}
parent_dictionary = {}
label_dictionary = {}
difference_dictionary = {}
pairs_dictionary = {}

root = None

class Tree(object):
	def __init__(self):
		self.parent = None
		self.left = None
		self.right = None
		self.value = None

def compare_nodes(a, b):
	#if scalars[a] > scalars[b]:
	# Adhitya: Testing spatial ordering
	if a > b:
		return 1
	else:
		return -1

def traverse(i, root, parent_node):
	#print root, scalars[root], i
	global index
	index_map[root] = index
	index += 1
	visited[root] = True
	adjacency[root].sort(compare_nodes)
	adjacency[root].reverse()
	for j, node in enumerate(adjacency[root]):
		if(visited[node] == False):
			current = Tree()
			if(parent_node.left == None):
				parent_node.left = current
			else:
				parent_node.right = current
			current.parent = parent_node
			current.value = node
			traverse(j, node, current)

def preorder(tree, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary):
	if(tree == None):
		return
	else:
		right_dictionary[index_map[tree.value]] = index_map[right_leaf(tree)]
		label_dictionary[index_map[tree.value]] = scalars[tree.value]
		if tree.value != tree.parent.value:
			parent_dictionary[index_map[tree.value]] = index_map[tree.parent.value]
		else:
			parent_dictionary[index_map[tree.value]] = 0
	
		difference_dictionary[index_map[tree.value]] = abs(scalars[tree.value] - scalars[pairs[tree.value]])

		pairs_dictionary[index_map[tree.value]] = index_map[pairs[tree.value]]

		#print tree.value, index_map[tree.value], scalars[tree.value], parent_dictionary[index_map[tree.value]]

		preorder(tree.left, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary)
		preorder(tree.right, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary)

def right_leaf(tree):
	if(tree == None):
		return
	elif(tree.right == None):
		if(tree.left != None):
			return right_leaf(tree.left)
		else:
			return tree.value
	else:
		return right_leaf(tree.right)
		
		
def get_merge_tree():
	# Get merge tree path
	tree_file_arguments = [tree_type, TREE_INFIX, file_name, CSV_EXTENSION]
	tree_file_path = get_output_path(file_path, tree_file_arguments, folder_name = TREES_FOLDER)

	# Read merge tree file
	with open(tree_file_path, 'rb') as csvfile:
		csvfile.readline() 
		spamreader = csv.reader(csvfile, delimiter=' ')
		for r in spamreader:
			row = r[0].split(',')
			node1 = int(row[0])
			node2 = int(row[1])
		
			scalars[node1] = float(row[2])
			scalars[node2] = float(row[3])
		
			visited[node1] = False
			visited[node2] = False

			if node1 not in adjacency.keys():
				adjacency[node1] = []

			if node2 not in adjacency.keys():
				adjacency[node2] = []

			adjacency[node1].append(node2)
			adjacency[node2].append(node1)

	for i in adjacency.keys():
		if len(adjacency[i]) == 1:
			if (scalars[i] < scalars[adjacency[i][0]]):
				root = i
	return root

def get_persistent_pairs():
	# Get persistence pairs
	pairs_file_arguments = [tree_type, PAIRS_INFIX, file_name, CSV_EXTENSION]
	pairs_file_path = get_output_path(file_path, pairs_file_arguments, folder_name = PAIRS_FOLDER)

	with open(pairs_file_path, 'rb') as persistence_pairs:
		persistence_pairs.readline() 
		spamreader = csv.reader(persistence_pairs, delimiter=' ')
		for r in spamreader:
			row = r[0].split(',')
			node1 = int(row[0])
			node2 = int(row[1])

			if (node1 in scalars.keys()) and (node2 in scalars.keys()):
				pairs[node1] = node2
				pairs[node2] = node1
	
def write_graph():
	# Print the graph
	graph_file_path = get_output_path(file_path, [file_name, TXT_EXTENSION], folder_name = GRAPHS_FOLDER)
	graph_file = open(graph_file_path, 'w')
	graph_file.write('digraph {\n')

	#print sorted(inverse_index_map.keys(), reverse = True)

	for i in inverse_index_map.keys():
		#print inverse_index_map[i], i, r1[i], p1[i], l1[i], d1[i]

		if parent_dictionary[i] != 0:
			node1 = "\"" + str(inverse_index_map[i]) + " " +str(round(scalars[inverse_index_map[i]],4)) + ' ('+str(i)+')' +"\""
			connector = ' -> '
			node2 = "\""+ str(inverse_index_map[parent_dictionary[i]]) + " " + str(round(scalars[inverse_index_map[parent_dictionary[i]]],4)) + ' ('+str(parent_dictionary[i])+')' +"\""
			end = ';'
			line = node2 + connector + node1 + end +'\n'
			graph_file.write(line)

	graph_file.write('}')
	graph_file.close()
	
	# write graph as image
	image_file_path = get_output_path(file_path, [file_name, PNG_EXTENSION], folder_name = IMAGES_FOLDER)
	os.system('dot -Tpng ' + graph_file_path + ' > ' + image_file_path)
	
def save_dictionaries():
	# save dictionaries to respective files
	save_dictionary(right_dictionary, file_name, RIGHT_NODE_PREFIX)
	save_dictionary(parent_dictionary, file_name, PARENT_NODE_PREFIX)
	save_dictionary(label_dictionary, file_name, LABEL_NODE_PREFIX)
	save_dictionary(difference_dictionary, file_name, DIFFERENCE_NODE_PREFIX)
	save_dictionary(pairs_dictionary, file_name, PAIRS_NODE_PREFIX)
	save_dictionary(inverse_index_map, file_name, MAPPING_NODE_PREFIX)
	
root = get_merge_tree()
get_persistent_pairs()

tree = Tree()
tree.value = root
tree.parent = tree
traverse(0, root, tree)

preorder(tree, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary)

# store inverse of index map
inverse_index_map = {v: k for k, v in index_map.iteritems()}
write_graph()

save_dictionaries()

print file_name, 'Done :)'