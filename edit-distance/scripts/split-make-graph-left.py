import csv, sys
import pickle
import os

filename = (sys.argv[1]).split('.')[0]
parent_path = '/home/nagarjun/Desktop/bitbucket/editdistancemergetree/edit-distance/'
tree_path = parent_path + 'trees/'
dictionary_path = parent_path + 'dictionary/'
image_path = parent_path + 'images/'
graph_path = parent_path + 'graph/'
pairs_path = parent_path + 'pairs/'
contour_file = tree_path + 'split-tree-' + filename + '.csv'
pairs_file = pairs_path + 'split-pairs-' + filename + '.csv'
output_file = filename

scalars = {}
visited = {}
adjacency = {}
index_map = {}
pairs = {}

index = 1

r1 = {}
p1 = {}
l1 = {}
d1 = {}
pp1 = {}

level_nodes_order = []
level_nodes_dictionary = {}
restructured_nodes_dictionary = {}

graph_path = graph_path + output_file + '.txt'
image_path = image_path + output_file + '.png'

root = None


class Tree(object):
	def __init__(self):
		self.parent = None
		self.left = None
		self.right = None
		self.value = None


def compare_nodes(a, b):
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


def preorder(tree, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary):
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

		preorder(tree.left, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary)
		preorder(tree.right, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary, pairs_dictionary)


def right_leaf(tree):
	if (tree == None):
		return
	elif (tree.right == None):
		if (tree.left != None):
			return right_leaf(tree.left)
		else:
			return tree.value
	else:
		return right_leaf(tree.right)


# Function to  print level order traversal of tree
def printLevelOrder(root):
	h = height(root)
	for i in range(1, h + 1):
		printGivenLevel(root, i)
	# print ''


def printGivenLevel(root, level):
	if root is None:
		return
	if level == 1:
		# Create arrays and mappings
		# print root.value
		level_nodes_order.append(root)
		level_nodes_dictionary[root.value] = root
		newNode = Tree()
		newNode.value = root.value
		restructured_nodes_dictionary[root.value] = newNode
	elif level > 1:
		printGivenLevel(root.left, level - 1)
		printGivenLevel(root.right, level - 1)


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

def restructured_preorder(root):
	global index
	if root != None:
		index_map[root.value] = index
		line = str(root.value) + ' ' + '[' + 'label=' + "\"" + str(root.value) + " " + str(round(scalars[root.value], 4)) + ' (' + str(index) + ')' + "\"" + ']' + '\n'
		graph_file.write(line)
		index += 1
		restructured_preorder(root.left)
		restructured_preorder(root.right)

with open(contour_file, 'rb') as csvfile:
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

with open(pairs_file, 'rb') as persistence_pairs:
	persistence_pairs.readline()
	spamreader = csv.reader(persistence_pairs, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		node1 = int(row[0])
		node2 = int(row[1])

		if (node1 in scalars.keys()) and (node2 in scalars.keys()):
			pairs[node1] = node2
			pairs[node2] = node1

tree = Tree()
tree.value = root
tree.parent = tree
traverse(0, root, tree)

preorder(tree, r1, p1, l1, d1, pp1)

printLevelOrder(tree)

# Make parent of each node syncronized
for node in level_nodes_order:
	restructured_nodes_dictionary[node.value].parent = level_nodes_dictionary[node.value].parent

# Remove global minimum and its pair in level order traversal
global_minimum = level_nodes_order[0]
global_minimum_pair = level_nodes_dictionary[pairs[global_minimum.value]]
level_nodes_order.remove(global_minimum)
level_nodes_order.remove(global_minimum_pair)

#print global_minimum.value, global_minimum_pair.value
restructured_minimum = level_nodes_order[0].value


for node in level_nodes_order:
	left_node = None
	right_node = None
	paired_node = pairs[node.value]

	# Then the first node is a saddle
	if len(adjacency[paired_node]) == 1:
		current = level_nodes_dictionary[paired_node].parent
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

# Restore variables again for preorder and restructured_preorder
index = 1
index_map = {}
r1 = {}
p1 = {}
l1 = {}
d1 = {}
pp1 = {}

# Print the graph
graph_file = open(graph_path, 'w')
graph_file.write('digraph {\n')

restructured_nodes_dictionary[global_minimum.value].left = restructured_nodes_dictionary[restructured_minimum]

restructured_tree = restructured_nodes_dictionary[global_minimum.value]
restructured_preorder(restructured_tree)

for node in restructured_nodes_dictionary.keys():
	# Prevent self loop for global minimum
	if node != global_minimum.value:
		line = str(restructured_nodes_dictionary[node].parent.value) + '->' + str(restructured_nodes_dictionary[node].value) + '\n'
		graph_file.write(line)

graph_file.write('}')
graph_file.close()

preorder(restructured_tree, r1, p1, l1, d1, pp1)

inv_map = {v: k for k, v in index_map.iteritems()}

os.system('dot -Tpng ' + graph_path + ' > ' + image_path)

with open(dictionary_path + output_file + '-right.bin', 'wb') as handle:
	pickle.dump(r1, handle)

with open(dictionary_path + output_file + '-parent.bin', 'wb') as handle:
	pickle.dump(p1, handle)

with open(dictionary_path + output_file + '-labels.bin', 'wb') as handle:
	pickle.dump(l1, handle)

with open(dictionary_path + output_file + '-difference.bin', 'wb') as handle:
	pickle.dump(d1, handle)

with open(dictionary_path + output_file + '-pairs.bin', 'wb') as handle:
	pickle.dump(pp1, handle)

with open(dictionary_path + output_file + '-mapping.bin', 'wb') as handle:
	pickle.dump(inv_map, handle)

print filename, 'Done :)'
