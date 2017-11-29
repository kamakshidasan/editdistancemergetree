from helper import *
import networkx as nx
import matplotlib.pyplot as plt
import itertools

# Take the names of files as arguments
filename1 =  sys.argv[1]
filename2 = sys.argv[2]

# Get the paths
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
dictionary1 = get_output_path(file_path, [filename1], folder_name = DICTIONARY_FOLDER)
dictionary2 = get_output_path(file_path, [filename2], folder_name = DICTIONARY_FOLDER)
results_path = get_output_path(file_path, [EDIT_DISTANCE_RESULT, CSV_EXTENSION], folder_name = RESULTS_FOLDER)

# Get right-most node for each node
right1 = get_dictionary(file_path, [filename1, RIGHT_NODE_SUFFIX])
right2 = get_dictionary(file_path, [filename2, RIGHT_NODE_SUFFIX])

# Get parent of each node
parent1 = get_dictionary(file_path, [filename1, PARENT_NODE_SUFFIX])
parent2 = get_dictionary(file_path, [filename2, PARENT_NODE_SUFFIX])

# Get function value of each node
label1 = get_dictionary(file_path, [filename1, LABEL_NODE_SUFFIX])
label2 = get_dictionary(file_path, [filename2, LABEL_NODE_SUFFIX])

# Get persistence of each node
difference1 = get_dictionary(file_path, [filename1, DIFFERENCE_NODE_SUFFIX])
difference2 = get_dictionary(file_path, [filename2, DIFFERENCE_NODE_SUFFIX])

# Get pairs for each node
pairs1 = get_dictionary(file_path, [filename1, PAIRS_NODE_SUFFIX])
pairs2 = get_dictionary(file_path, [filename2, PAIRS_NODE_SUFFIX])

# Get index mapping for each node
index_mapping1 = get_dictionary(file_path, [filename1, MAPPING_NODE_SUFFIX])
index_mapping2 = get_dictionary(file_path, [filename2, MAPPING_NODE_SUFFIX])

# Get size of both the trees
size1 = len(parent1.keys())
size2 = len(parent2.keys())

root1 = None
root2 = None

tree_nodes = [[], []]

class TreeNode(object):
	def __init__(self, vertex, scalar, persistence):
		self.vertex = vertex
		self.scalar = scalar
		self.persistence = persistence
		self.parent = None
		self.children = []
		self.pair = None

	def add_child(self, child):
		self.children.append(child)

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


class GraphNode(object):
	def __init__(self, node1, node2):
		self.u = node1
		self.v = node2
		self.weight = (node1.persistence/2.0) + (node2.persistence/2.0) + abs(node1.scalar - node2.scalar)
		self.edges = []
		self.index = 0

def create_tree(parent_dictionary, index_mapping, label_dictionary, difference_dictionary, pairs_dictionary, tree_index):
	root = None
	nodes = [None]
	# create n-ary tree with parent-children-pairs binding
	for index in parent_dictionary.keys():

		vertex_id = index_mapping[index]
		scalar_value = label_dictionary[index]
		parent_index = parent_dictionary[index]
		persistence_value = difference_dictionary[index]
		pair_index = pairs_dictionary[index]

		node = TreeNode(vertex_id, scalar_value, persistence_value)
		nodes.append(node)

		#print str(node)

		if parent_dictionary[index] == 0:
			root = node
		else:
			# add child to parent and vice-versa
			nodes[parent_index].add_child(node)
			node.parent = nodes[parent_index]

		# otherwise the node would have not been created
		if pair_index < index:
			nodes[index].add_pair(nodes[pair_index])
			nodes[pair_index].add_pair(nodes[index])

	del nodes[0]
	tree_nodes[tree_index] = nodes

	return root

def get_ancestors(node):
	ancestors = []
	while node.parent != None:
		ancestors.append(node.parent)
		node = node.parent
	return ancestors

def get_descendants(node):
	descendants = []
	def traverse(node):
		for child in node.children:
			descendants.append(child)
			traverse(child)
	traverse(node)
	return descendants

def print_ancestors(node):
	ancestors = get_ancestors(node)
	return [ancestor.vertex for ancestor in ancestors]

def print_descendants(node):
	descendants = get_descendants(node)
	return [descendant.vertex for descendant in descendants]

def traverse_tree(node):
	print str(node.vertex), 'Ancestors: ', print_ancestors(node), 'Descendants: ', len(print_descendants(node))
	
	for child in node.children:
		traverse_tree(child)

def is_descendant(node1, node2):
	if (node1 in get_descendants(node2)):
		return True
	else:
		return False

def traverse_nodes(nodes):
	for node in nodes:
		print str(node.vertex), 'Ancestors: ', print_ancestors(node), 'Descendants: ', len(print_descendants(node))

root1 = create_tree(parent1, index_mapping1, label1, difference1, pairs1, 0)
root2 = create_tree(parent2, index_mapping2, label2, difference2, pairs2, 1)

product_graph = nx.Graph()
graph_nodes = []

graph_node_index = 1
for node1, node2 in itertools.product(tree_nodes[0], tree_nodes[1]):
	graph_node = GraphNode(node1, node2)
	graph_node.index = graph_node_index
	graph_nodes.append(graph_node)
	product_graph.add_node(graph_node)
	graph_node_index += 1

for node1 in product_graph.nodes():
	for node2 in product_graph.nodes():
		if (node1.u != node2.u) and (node1.v != node2.v):
			if (is_descendant(node1.u, node2.u) and is_descendant(node1.v, node2.v)):
				product_graph.add_edge(node1, node2)
			elif (is_descendant(node2.u, node1.u) and is_descendant(node2.v, node1.v)):
				product_graph.add_edge(node1, node2)
			elif ((not(is_descendant(node1.u, node2.u))) and (not(is_descendant(node1.v, node2.v)))):
				product_graph.add_edge(node1, node2)
			elif ((not(is_descendant(node2.u, node1.u))) and (not(is_descendant(node2.v, node1.v)))):
				product_graph.add_edge(node1, node2)
			else:
				continue

#nx.draw(product_graph)
#plt.show()



print len(product_graph.nodes())
print len(product_graph.edges())

clique_graph_arguments = [join_strings([filename1,filename2]), TXT_EXTENSION]
clique_graph_path = get_output_path(file_path, clique_graph_arguments, folder_name = CLIQUE_GRAPHS_FOLDER)
clique_graph_file = open(clique_graph_path, 'w')

clique_graph_file.write("p edge " + str(len(product_graph.nodes())) + " " + str(len(product_graph.edges())) + "\n")
for node in product_graph.nodes():
	clique_graph_file.write("n "+ str(node.index) + " " + str(int(node.weight * 100)) + "\n")

for edge in product_graph.edges():
	(node1, node2) = edge
	clique_graph_file.write("e "+ str(node1.index) + " " + str(node2.index) + "\n")

maximum_clique = "1 17 33 50 71 83 102 109 126 142 159 175 193 209 225"
maximum_clique = map(int, maximum_clique.split())
print maximum_clique

cost = 0
for node in maximum_clique:
	graph_node = graph_nodes[node-1]
	cost += graph_node.weight
	print graph_node.u.vertex, graph_node.v.vertex

print cost
