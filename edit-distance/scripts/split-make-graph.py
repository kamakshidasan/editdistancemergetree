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
visited= {}
adjacency = {}
index_map = {}
pairs = {}

index = 1

r1 = {}
p1 = {}
l1 = {}
d1 = {}
pp1 = {}

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
			if(parentNode.left == None):
				parentNode.left = current
			else:
				parentNode.right = current
			current.parent = parentNode
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

#maximum_scalar = float("-inf")

#for i in scalars:
#	maximum_scalar = max(maximum_scalar, scalars[i])

#print filename+','+str(maximum_scalar)

#for i in scalars:
#	scalars[i] = maximum_scalar - scalars[i]

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

inv_map = {v: k for k, v in index_map.iteritems()}

graph_path = graph_path + output_file + '.txt'
image_path = image_path + output_file + '.png'
graph_file = open(graph_path, 'w')
graph_file.write('digraph {\n')

#print sorted(inv_map.keys(), reverse = True)

for i in inv_map.keys():
	#print inv_map[i], i, r1[i], p1[i], l1[i], d1[i]

	if p1[i] != 0:
		node1 = "\"" + str(inv_map[i]) + " " +str(round(scalars[inv_map[i]],4)) + ' ('+str(i)+')' +"\""
		connector = ' -> '
		node2 = "\""+ str(inv_map[p1[i]]) + " " + str(round(scalars[inv_map[p1[i]]],4)) + ' ('+str(p1[i])+')' +"\""
		end = ';'
		line = node2 + connector + node1 + end +'\n'
		graph_file.write(line)

graph_file.write('}')
graph_file.close()

os.system('dot -Tpng '+ graph_path+' > '+image_path)

with open(dictionary_path + output_file +'-right.bin', 'wb') as handle:
  pickle.dump(r1, handle)

with open(dictionary_path + output_file +'-parent.bin', 'wb') as handle:
  pickle.dump(p1, handle)

with open(dictionary_path + output_file +'-labels.bin', 'wb') as handle:
  pickle.dump(l1, handle)

with open(dictionary_path + output_file +'-difference.bin', 'wb') as handle:
  pickle.dump(d1, handle)

with open(dictionary_path + output_file + '-pairs.bin', 'wb') as handle:
	pickle.dump(pp1, handle)

with open(dictionary_path + output_file + '-mapping.bin', 'wb') as handle:
	pickle.dump(inv_map, handle)
