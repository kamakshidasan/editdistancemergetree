import csv, sys
import pickle
from helper import *

file_name = (sys.argv[1]).split('.')[0]
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
tree_type = TREE_TYPE_SPLIT

scalars = {}
visited = {}
adjacency = {}
index_map = {}
pairs = {}

index = 1

right_dictionary = {}
parent_dictionary = {}
label_dictionary = {}
difference_dictionary = {}
pairs_dictionary = {}

level_order_nodes = []
nodes_dictionary = {}
restructured_nodes_dictionary = {}

restructured_index = 1
restructured_index_map = {}
restructured_inverse_index_map = {}

restructured_right ={}
restructured_parent = {}
restructured_label = {}
restructured_difference = {}
restructured_pairs = {}

root = None

class Tree(object):
	def __init__(self):
		self.parent = None
		self.left = None
		self.right = None
		self.value = None


def compare_nodes(a, b):
	#if a > b:
	if scalars[a] > scalars[b]:
		return 1
	else:
		return -1


def traverse(i, root, parentNode):
	# print root, scalars[root], i
	global index
	index_map[root] = index
	index += 1
	visited[root] = True
	adjacency[root].sort(compare_nodes)
	adjacency[root].reverse()
	for j, node in enumerate(adjacency[root]):
		if (visited[node] == False):
			current = Tree()
			if (parentNode.left == None):
				parentNode.left = current
			else:
				parentNode.right = current
			current.parent = parentNode
			current.value = node
			traverse(j, node, current)


def preorder(tree, index_map, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary):
	if (tree == None):
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

		# print tree.value, index_map[tree.value], scalars[tree.value], parent_dictionary[index_map[tree.value]]

		preorder(tree.left, index_map, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary)
		preorder(tree.right, index_map, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary)

# return the right most node for a given node 
def right_leaf(node):
	if (node == None):
		return
	elif (node.right == None):
		if (node.left != None):
			return right_leaf(node.left)
		else:
			return node.value
	else:
		return right_leaf(node.right)

# return the height for a given node 
def height(node):
	if node is None:
		return 0
	else:
		lheight = height(node.left)
		rheight = height(node.right)
		if lheight > rheight:
			return lheight + 1
		else:
			return rheight + 1

# Function to traverse level order traversal of tree
def traverse_level_order(root):
	h = height(root)
	for i in range(1, h + 1):
		traverse_level(root, i)
	# print ''


# Create arrays and mappings
def traverse_level(root, level):
	if root is None:
		return
	if level == 1:
		#print root.value
		
		# store the node object of the tree [without restructuring]
		level_order_nodes.append(root)
		# create a mapping from vertex id to its object
		nodes_dictionary[root.value] = root

		# create a new node for the restructured tree with the same vertex id
		newNode = Tree()
		newNode.value = root.value

		# map newly created nodes with their objects
		restructured_nodes_dictionary[root.value] = newNode

		# Parent for each node will remain the same with any restructuring
		restructured_nodes_dictionary[root.value].parent = root.parent
	elif level > 1:
		traverse_level(root.left, level - 1)
		traverse_level(root.right, level - 1)

def make_restructured_tree(tree):
	
	# traverse the tree in level order and create a duplicate object for each node
	traverse_level_order(tree)

	# Remove global minimum and its pair from restructuring
	# Adhitya knows this is necessary. But has forgotten why. 

	# We traversed in level order [bound to be the first node]
	global_minimum = level_order_nodes[0]
	global_minimum_pair = nodes_dictionary[pairs[global_minimum.value]]
	level_order_nodes.remove(global_minimum)
	level_order_nodes.remove(global_minimum_pair)

	#print global_minimum.value, global_minimum_pair.value
	restructured_minimum = level_order_nodes[0].value

	for node in level_order_nodes:
		left_node = None
		right_node = None
		paired_node = pairs[node.value]

		# Then the first node is a saddle
		if len(adjacency[paired_node]) == 1:
			current = nodes_dictionary[paired_node].parent
			# Current node itself is on the left
			if current.value == node.value:
				# If node on right side, make it left
				if paired_node == current.right.value:
					left_node = paired_node
					right_node = current.left.value
				# If node on left side, it will remain the same
				else:
					left_node = paired_node
					right_node = current.right.value
			# There is more than one node in the monotone upwards path to the saddle
			else:
				while current.parent.value != node.value:
					current = current.parent
				# If node on right side, make it left
				if current.parent.right.value == current.value:
					left_node = current.value
					right_node = current.parent.left.value
				# If node on left side, it will remain the same
				else:
					left_node = current.value
					right_node = current.parent.right.value
			restructured_nodes_dictionary[node.value].left = restructured_nodes_dictionary[left_node]
			restructured_nodes_dictionary[node.value].right = restructured_nodes_dictionary[right_node]

	# Remember global minimum was removed? [Current root is made the left child for the returning node]
	# Pair of global minimum would have been considered during the restructuring
	restructured_nodes_dictionary[global_minimum.value].left = restructured_nodes_dictionary[restructured_minimum]

	# get the root of this restructured tree
	restructured_tree = restructured_nodes_dictionary[global_minimum.value]
	return restructured_tree

def restructured_preorder(root):
	global restructured_index
	if root != None:
		restructured_index_map[root.value] = restructured_index
		restructured_inverse_index_map [restructured_index] = root.value
		restructured_index += 1
		restructured_preorder(root.left)
		restructured_preorder(root.right)

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

def initialize_tree(root):
	tree = Tree()
	tree.value = root
	tree.parent = tree
	return tree

def write_graph(right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary, inverse_map):
	# Print the graph
	graph_file_path = get_output_path(file_path, [file_name, TXT_EXTENSION], folder_name = GRAPHS_FOLDER)
	graph_file = open(graph_file_path, 'w')
	graph_file.write('digraph {\n')

	for node in inverse_map.keys():
		graph_file.write(get_node(node, pairs_dictionary, inverse_map, label_dictionary))

	for node in inverse_map.keys():
		graph_file.write(get_connectivity(node, parent_dictionary, inverse_map))

	graph_file.write('}')
	graph_file.close()

	# write graph as image
	image_file_path = get_output_path(file_path, [file_name, PNG_EXTENSION], folder_name = IMAGES_FOLDER)
	os.system('dot -Tpng ' + graph_file_path + ' > ' + image_file_path)

def save_dictionaries():
	# save dictionaries to respective files
	save_dictionary(restructured_right, file_name, RIGHT_NODE_PREFIX)
	save_dictionary(restructured_parent, file_name, PARENT_NODE_PREFIX)
	save_dictionary(restructured_label, file_name, LABEL_NODE_PREFIX)
	save_dictionary(restructured_difference, file_name, DIFFERENCE_NODE_PREFIX)
	save_dictionary(restructured_pairs, file_name, PAIRS_NODE_PREFIX)
	save_dictionary(restructured_inverse_index_map, file_name, MAPPING_NODE_PREFIX)

# start
root = get_merge_tree()

get_persistent_pairs()

tree = initialize_tree(root)

traverse(0, root, tree)

preorder(tree, index_map, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary)

restructured_tree = make_restructured_tree(tree)

# now that the restructured tree is created, make the dictionaries coherrent
restructured_preorder(restructured_tree)
preorder(restructured_tree, restructured_index_map, restructured_right, restructured_parent, restructured_label, restructured_difference, restructured_pairs)

write_graph(restructured_right, restructured_parent, restructured_label, restructured_difference, restructured_pairs, restructured_inverse_index_map)

print file_name, 'Done :)'

