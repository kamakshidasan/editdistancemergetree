from helper import *

# Get the paths
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))

# Take the names of files as arguments
full_file_name = sys.argv[1]
file_name = get_file_name(full_file_name)

# Get right-most node for each node
right_dictionary = get_dictionary(file_path, [file_name, RIGHT_NODE_SUFFIX])

# Get parent of each node
parent_dictionary = get_dictionary(file_path, [file_name, PARENT_NODE_SUFFIX])

# Get function value of each node
label_dictionary = get_dictionary(file_path, [file_name, LABEL_NODE_SUFFIX])

# Get persistence of each node
difference_dictionary = get_dictionary(file_path, [file_name, DIFFERENCE_NODE_SUFFIX])

# Get pairs of each node
pairs_dictionary = get_dictionary(file_path, [file_name, PAIRS_NODE_SUFFIX])

# Get vertex indices for each node
index_mapping = get_dictionary(file_path, [file_name, MAPPING_NODE_SUFFIX])

# Get size of both the trees
size = len(parent_dictionary.keys())

# How much are we planning to compare?
extents = [1, right_dictionary[1]]

inverse_index_map = {v: k for k, v in index_mapping.iteritems()}

root = None
preorder_index = 1
ratio_threshold = 0.07

merged_index_map = {}
merged_inverse_index_map = {}
merged_right = {}
merged_parent = {}
merged_label = {}
merged_difference = {}
merged_pairs = {}

class Node(object):
	def __init__(self, vertex, scalar, persistence):
		self.vertex = vertex
		self.scalar = scalar
		self.persistence = persistence
		self.parent = None
		self.merged_nodes = []
		self.children = []
		self.pair = None
		self.merged = False
		self.index = None

	def add_child(self, child):
		self.children.append(child)

	def merge_node(self, parent):
		# sign papers for adoption
		for child in self.children:
			child.parent = parent
		# transfer children of node to parent
		parent.children.extend(self.children)
		# remove children of current node after transfer
		self.children = []
		# make node to be merged with parent
		parent.merged_nodes.append(self)
		# remove node from children of parent
		parent.children.remove(self)
		# mark node as merged
		# the way to access other outer nodes would be using node.parent
		self.merged = True

	def add_pair(self, pair):
		self.pair = pair

	def is_leaf(self):
		return (self.children == None)

	def is_root(self):
		return (self.parent == None)

	def is_saddle(self):
		return ((not(self.is_root())) and (not(self.is_leaf())))

	def has_merged_nodes(self):
		return not not self.merged_nodes()

	# simple print node function. Usage: print str(node)
	def __str__(self):
		return str(self.vertex) + " " + str(self.scalar) + " " + str(self.persistence)

	# simple print children function. Usage: node.print_children()
	def print_children(self):
		children_names = ""
		for child in self.children:
			children_names +=  " " + str(child.vertex)
		return children_names

# return the height for a given node
def height(node):
	if node is None:
		return 0

	max_depth = 0
	for child in node.children:
		max_depth = max(max_depth, height(child))

	return max_depth + 1

# Function to traverse level order traversal of tree
def merge_unstable_saddles(node):
	h = height(node)
	# traverse from below
	for i in range(h+1, 0, -1):
		traverse_level(node, i)
		#print ''


# find the ratio from bottom-up
def traverse_level(node, level):
	if node is None:
		return
	if level == 1:
		# do this merging only for saddles
		if node.is_saddle():
			# lets not tinker with the root
			if not node.parent.is_root():
				parent = node.parent
				ratio =  (node.scalar -  parent.scalar)
				if ratio < ratio_threshold:
					node.merge_node(parent)
					print round(ratio,4), node.vertex, parent.vertex, 'merge'
				#else:
				#	print inverse_index_map[node.vertex], ratio, 'chill :)'
	elif level > 1:
		# traverse backwards
		for child in reversed(node.children):
			traverse_level(child, level - 1)

# find new pairs for nodes whose pairs have been merged
def synchronize_pairs(node):
	if node is None:
		return

	#if not node.is_root():
	#	print node.vertex, node.parent.vertex, node.pair.vertex, node.print_children(), node.pair.parent.vertex

	# if persistence pair of a node has been merged: get a new pair
	# keep looking for a parent which has not been merged
	if node.pair.merged == True:
		parent = node.pair.parent
		while parent.merged != False:
			parent = parent.parent
		node.pair = parent

	#if not node.is_root():
	#	print node.vertex, node.parent.vertex, node.pair.vertex

	for child in node.children:
		synchronize_pairs(child)


def arrange_tree(node):
	global preorder_index
	if node is None:
		return

	node.index = preorder_index

	# Stupid sorting. Adhitya: Change after Vijay opposes this [This should be based on both trees]
	distances = [find_distance(child.vertex) for child in node.children]
	distance_indices = [x for x,y in sorted(enumerate(distances), key = lambda x: x[1])]
	node.children = [x for y,x in sorted(zip(distances, node.children))]
	#print node.index, node.vertex, distances, node.print_children(), distance_indices

	preorder_index += 1

	for child in node.children:
		arrange_tree(child)

# return the right most node for a given node 
def right_leaf(node):
	if (node == None):
		return
	elif (not node.children):
		return node
	else:
		# return the last child for each node
		return right_leaf(node.children[-1])

def preorder(node, index_map, inverse_map, right, parent, label, difference, pairs):
	if (node == None):
		return
	else:
		index_map[node.vertex] = node.index
		inverse_map[node.index] = node.vertex
		right[node.index] = (right_leaf(node)).index
		label[node.index] = node.scalar

		if node.parent == None:
			parent[node.index] = 0
		else:
			parent[node.index] = node.parent.index

		# eventhough the pairs have changed, you can as well take the initial persistence
		difference[node.index] = abs(node.scalar - node.pair.scalar)

		pairs[node.index] = node.pair.index

		# print node.vertex, node.scalar, node.pair.vertex, parent_dictionary[node.index]

		for child in node.children:
			preorder(child, index_map, inverse_map, right, parent, label, difference, pairs)

def write_graph(right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary, inverse_map):
	# Print the graph
	graph_file_path = get_output_path(file_path, [file_name, TXT_EXTENSION], folder_name = MERGED_GRAPHS_FOLDER)
	graph_file = open(graph_file_path, 'w')
	graph_file.write('digraph {\n')

	for node in inverse_map.keys():
		graph_file.write(get_node(node, pairs_dictionary, inverse_map, label_dictionary))

	for node in inverse_map.keys():
		graph_file.write(get_connectivity(node, parent_dictionary, inverse_map))

	graph_file.write('}')
	graph_file.close()

	# write graph as image
	image_file_path = get_output_path(file_path, [file_name, PNG_EXTENSION], folder_name = MERGED_IMAGES_FOLDER)
	os.system('dot -Tpng ' + graph_file_path + ' > ' + image_file_path)

def create_tree():
	tree_nodes = [None]
	# create n-ary tree with parent-children-pairs binding
	for index in parent_dictionary.keys():

		vertex_id = index_mapping[index]
		scalar_value = label_dictionary[index]
		parent_index = parent_dictionary[index]
		persistence_value = difference_dictionary[index]
		pair_index = pairs_dictionary[index]

		node = Node(vertex_id, scalar_value, persistence_value)
		tree_nodes.append(node)

		#print str(node)

		if parent_dictionary[index] == 0:
			root = node
		else:
			# add child to parent and vice-versa
			tree_nodes[parent_index].add_child(node)
			node.parent = tree_nodes[parent_index]

		# otherwise the node would have not been created
		if pair_index < index:
			tree_nodes[index].add_pair(tree_nodes[pair_index])
			tree_nodes[pair_index].add_pair(tree_nodes[index])

	# all parent-children-pairs binding have been created now
	# throw away tree_nodes list for all you care
	# not necessary, but for the shear pleasure of killing someone
	del tree_nodes

	return root

def save_dictionaries():
	# save dictionaries to respective files
	save_dictionary(merged_right, file_name, RIGHT_NODE_SUFFIX)
	save_dictionary(merged_parent, file_name, PARENT_NODE_SUFFIX)
	save_dictionary(merged_label, file_name, LABEL_NODE_SUFFIX)
	save_dictionary(merged_difference, file_name, DIFFERENCE_NODE_SUFFIX)
	save_dictionary(merged_pairs, file_name, PAIRS_NODE_SUFFIX)
	save_dictionary(merged_inverse_index_map, file_name, MAPPING_NODE_SUFFIX)

root = create_tree()

merge_unstable_saddles(root)

synchronize_pairs(root)

arrange_tree(root)

preorder(root, merged_index_map, merged_inverse_index_map, merged_right,\
 merged_parent, merged_label, merged_difference, merged_pairs)

write_graph(merged_right, merged_parent, merged_label, merged_difference,\
 merged_pairs, merged_inverse_index_map)

save_dictionaries()

print file_name, 'Merging Done :)'
