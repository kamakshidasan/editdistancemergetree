from helper import *

# Get the paths
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))

# Take the names of files as arguments
filename = sys.argv[1]

# Get right-most node for each node
right_dictionary = get_dictionary(file_path, [filename, RIGHT_NODE_PREFIX])

# Get parent of each node
parent_dictionary = get_dictionary(file_path, [filename, PARENT_NODE_PREFIX])

# Get function value of each node
label_dictionary = get_dictionary(file_path, [filename, LABEL_NODE_PREFIX])

# Get persistence of each node
difference_dictionary = get_dictionary(file_path, [filename, DIFFERENCE_NODE_PREFIX])

# Get pairs of each node
pairs_dictionary = get_dictionary(file_path, [filename, PAIRS_NODE_PREFIX])

# Get vertex indices for each node
index_mapping = get_dictionary(file_path, [filename, MAPPING_NODE_PREFIX])

# Get size of both the trees
size = len(parent_dictionary.keys())

# How much are we planning to compare?
extents = [1, right_dictionary[1]]

inverse_index_map = {v: k for k, v in index_mapping.iteritems()}

#print index_mapping
#print inverse_index_map
#print right_dictionary
#print parent_dictionary
#print label_dictionary
#print difference_dictionary
#print pairs_dictionary
#print index_mapping
#print size
#print extents

class Node(object):
	def __init__(self, vertex, scalar, persistence):
		self.vertex = vertex
		self.scalar = scalar
		self.persistence = persistence
		self.parent = None
		self.merged_nodes = []
		self.children = []
		self.pairs = []
		self.merged = False
		self.preorder_index = None

	def add_child(self, child):
		self.children.append(child)

	def merge_node(self, node):
		self.merged_nodes.append(node)

	def add_pair(self, pair):
		self.pairs.append(pair)

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
		for child in self.children:
			return str(child)

# return the height for a given node
def height(node):
	if node is None:
		return 0

	max_depth = 0
	for child in node.children:
		max_depth = max(max_depth, height(child))

	return max_depth + 1

# Function to traverse level order traversal of tree
def traverse_level_order(node):
	h = height(node)
	# traverse from below
	for i in range(h+1, 0, -1):
		traverse_level(node, i)
		#print ''


# find the ratio from bottom to top
def traverse_level(node, level):
	if node is None:
		return
	if level == 1:
		# do this merging only for saddles
		if node.is_saddle():
			# lets not tinker with the root
			if not node.parent.is_root():
				ratio =  (node.scalar -  node.parent.scalar)/node.persistence
				if ratio < 0.005:
					# transfer children of node to parent
					node.parent.children.extend(node.children)
					# remove children of current node after transfer
					node.children = []
					# make node to be merged with parent
					node.parent.merge_node(node)
					# remove node from children of parent
					node.parent.children.remove(node)
					# mark node as merged
					# the way to access other outer nodes would be using node.parent
					node.merged = True
					print inverse_index_map[node.vertex], ratio, node.vertex, node.parent.vertex, node.pairs[0].vertex, 'merge'
				#else:
				#	print inverse_index_map[node.vertex], ratio, 'chill :)'
	elif level > 1:
		# traverse backwards
		for child in reversed(node.children):
			traverse_level(child, level - 1)

preorder_index = 1

def preorder(node):
	global preorder_index
	if node is None:
		return

	node.preorder_index = preorder_index
	if not node.is_root():
		print preorder_index, node, node.parent.vertex
	else:
		print preorder_index, node

	preorder_index+=1

	for child in node.children:
		preorder(child)

root = None
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

traverse_level_order(root)

preorder(root)
