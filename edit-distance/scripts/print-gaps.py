import os, time
import itertools, sys, pickle, inspect
from helper import *

# Take the names of files as arguments
filename1 =  sys.argv[1]
filename2 = sys.argv[2]

# Get the paths
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
dictionary1 = get_output_path(file_path, [filename1], folder_name = DICTIONARY_FOLDER)
dictionary2 = get_output_path(file_path, [filename2], folder_name = DICTIONARY_FOLDER)
results_path = get_output_path(file_path, [EDIT_DISTANCE_RESULT, CSV_EXTENSION], folder_name = RESULTS_FOLDER)

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

# Get size of both the trees
size1 = len(parent1.keys())
size2 = len(parent2.keys())

# How much are we planning to compare?
extents = [right1[1], right2[1]]
print extents

# Get the intermediate matrices
Q = get_matrix(file_path, [filename1, filename2, Q_IDENTIFIER])
Q1 = get_matrix(file_path, [filename1, filename2, Q1_IDENTIFIER])
Q2 = get_matrix(file_path, [filename1, filename2, Q2_IDENTIFIER])

S = get_matrix(file_path, [filename1, filename2, S_IDENTIFIER])
S1 = get_matrix(file_path, [filename1, filename2, S1_IDENTIFIER])
S2 = get_matrix(file_path, [filename1, filename2, S2_IDENTIFIER])

print S # lol.
