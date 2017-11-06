import os
os.system('date')
import time
start_time = time.time()

import itertools
import sys
import pickle
import random

# Only me and god knows how this code works
# In a few days only god will now

filename1 =  sys.argv[1]
filename2 = sys.argv[2]

parent_path = os.getcwd() + '/'
dictionary_path = parent_path + 'dictionary/'
distance_path = parent_path + 'distance/'
results_path = parent_path + 'results.csv'

dictionary1 = dictionary_path + filename1
dictionary2 = dictionary_path + filename2

distance1 = distance_path + filename1

with open(dictionary1+'-right.txt', 'rb') as handle:
  r1 = pickle.loads(handle.read())

with open(dictionary2+'-right.txt', 'rb') as handle:
  r2 = pickle.loads(handle.read())

with open(dictionary1+'-parent.txt', 'rb') as handle:
  p1 = pickle.loads(handle.read())

with open(dictionary2+'-parent.txt', 'rb') as handle:
  p2 = pickle.loads(handle.read())

with open(dictionary1+'-labels.txt', 'rb') as handle:
  l1 = pickle.loads(handle.read())

with open(dictionary2+'-labels.txt', 'rb') as handle:
  l2 = pickle.loads(handle.read())

with open(dictionary1+'-difference.txt', 'rb') as handle:
  d1 = pickle.loads(handle.read())

with open(dictionary2+'-difference.txt', 'rb') as handle:
  d2 = pickle.loads(handle.read())

size1 = len(p1.keys())
size2 = len(p2.keys())

Q = {}
Q1 = {}
Q2 = {}

a = 0

array = [1, r1[1], 1, r2[1]]
print array

def b1(i):
	return d1[i]/2.0

def b2(j):
	return d2[j]/2.0

def p(i, j):
	return abs(l1[i] - l2[j])

def checkBadExtents1(i1, i):
	if (i <= 0 or i > size1 or i1 <= 0 or i1 > size1):
		return True
	return False


def checkBadExtents2(j1, j):
	if (j <= 0 or j > size2 or j1 <= 0 or j1 > size2):
		return True
	return False


def Qf(i1, i, j1, j):
	#print i1, i, j1, j

	try:
		Q[i1][i][j1][j] += 0
	except:
		if i1 not in Q.keys():
			Q[i1] = {}
		if i not in Q[i1].keys():
			Q[i1][i] = {}
		if j1 not in Q[i1][i].keys():
			Q[i1][i][j1] = {}
		if j not in Q[i1][i][j1].keys():
			Q[i1][i][j1][j] = {}

	t1, t2 = True, True
	if (j < j1 or checkBadExtents2(j1, j)):
		t2 = False
	if (i < i1 or checkBadExtents1(i1, i)):
		t1 = False
	if (t1 == False and t2 == False):
		Q[i1][i][j1][j] = 0
		return Q[i1][i][j1][j]
	elif (t1 == False or t2 == False):
		Q[i1][i][j1][j] = float('inf')
		return Q[i1][i][j1][j]

	if (bool(Q[i1][i][j1][j])):
		#print 'Q', i1, i, j1, j, Q[i1][i][j1][j]
		return Q[i1][i][j1][j]
	else:
		zeroth = Qf(i1, i - 1, j1, j - 1)
		first = Q1f(i1, i, j1, j)
		second = Q2f(i1, i, j1, j)
		Q[i1][i][j1][j] = min(zeroth + p(i, j), first, second)
		#print 'Q', i1, i, j1, j, Q[i1][i][j1][j]
		return Q[i1][i][j1][j]


def Q1f(i1, i, j1, j):
	#print i1, i, j1, j

	try:
		Q1[i1][i][j1][j] += 0
	except:
		if i1 not in Q1.keys():
			Q1[i1] = {}
		if i not in Q1[i1].keys():
			Q1[i1][i] = {}
		if j1 not in Q1[i1][i].keys():
			Q1[i1][i][j1] = {}
		if j not in Q1[i1][i][j1].keys():
			Q1[i1][i][j1][j] = {}


	t1, t2 = True, True
	if (j < j1 or checkBadExtents2(j1, j)):
		t2 = False
	if (i < i1 or checkBadExtents1(i1, i)):
		t1 = False
	if (t2 == False):
		Q1[i1][i][j1][j] = a + b1(i) * i
		#print 'Q1', i1, i, j1, j, Q1[i1][i][j1][j]
		return Q1[i1][i][j1][j]
	elif (t1 == False):
		Q1[i1][i][j1][j] = float('inf')
		#print 'Q1', i1, i, j1, j, Q1[i1][i][j1][j]
		return Q1[i1][i][j1][j]

	if (bool(Q1[i1][i][j1][j])):
		#print 'Q1', i1, i, j1, j, Q1[i1][i][j1][j]
		return Q1[i1][i][j1][j]
	else:
		minimum = float('inf')
		for k in range(j1, j + 1):
			zeroth = Qf(p1[i] + 1, i - 1, k + 1, j)
			first = Q1f(i1, p1[i], j1, k)
			minimum = min(minimum, first + zeroth + b1(i))
		zeroth = Qf(i1, i - 1, j1, j)
		first = Q1f(i1, i - 1, j1, j)
		Q1[i1][i][j1][j] = min(zeroth + a + b1(i), first + b1(i), minimum)
		#print 'Q1', i1, i, j1, j, Q1[i1][i][j1][j]
		return Q1[i1][i][j1][j]


def Q2f(i1, i, j1, j):
	#print i1, i, j1, j

	try:
		Q2[i1][i][j1][j] += 0
	except:
		if i1 not in Q2.keys():
			Q2[i1] = {}
		if i not in Q2[i1].keys():
			Q2[i1][i] = {}
		if j1 not in Q2[i1][i].keys():
			Q2[i1][i][j1] = {}
		if j not in Q2[i1][i][j1].keys():
			Q2[i1][i][j1][j] = {}

	t1, t2 = True, True
	if (j < j1 or checkBadExtents2(j1, j)):
		t2 = False
	if (i < i1 or checkBadExtents1(i1, i)):
		t1 = False
	if (t1 == False):
		Q2[i1][i][j1][j] = a + b2(j) * i
		#print 'Q2', i1, i, j1, j, Q2[i1][i][j1][j]
		return Q2[i1][i][j1][j]
	elif (t2 == False):
		Q2[i1][i][j1][j] = float('inf')
		#print 'Q2', i1, i, j1, j, Q2[i1][i][j1][j]
		return Q2[i1][i][j1][j]

	if (bool(Q2[i1][i][j1][j])):
		#print 'Q2', i1, i, j1, j, Q2[i1][i][j1][j]
		return Q2[i1][i][j1][j]
	else:
		minimum = float('inf')
		for k in range(i1, i + 1):
			zeroth = Qf(k + 1, i, p2[j] + 1, j - 1)
			second = Q2f(i1, k, j1, p2[j])
			minimum = min(minimum, second + zeroth + b2(j))
		zeroth = Qf(i1, i, j1, j - 1)
		second = Q2f(i1, i, j1, j - 1)
		Q2[i1][i][j1][j] = min(zeroth + a + b2(j), second + b2(j), minimum)
		#print 'Q2', i1, i, j1, j, Q2[i1][i][j1][j]
		return Q2[i1][i][j1][j]


for i1, j1 in itertools.product(range(1, size1 + 1), range(1, size2 + 1)):
	for i in range(i1, r1[i1] + 1):
		for j in range(j1, r2[j1] + 1):
			#print i1, i, j1, j
			Q1[i1][i][j1][j] = Q1f(i1, i, j1, j)
			Q2[i1][i][j1][j] = Q2f(i1, i, j1, j)
			Q[i1][i][j1][j] = Qf(i1, i, j1, j)
			#print ''

difference = Q[1][r1[1]][1][r2[1]]
difference = "%.9f" % difference

seconds = time.time() - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
time_taken =  "%d:%02d:%02d" % (h, m, s)

csvfile = open(results_path, 'a')

# Change this when the filename format changes
timestep_value = filename1.split('tv_')[1]
csvfile.write(timestep_value + ',' + str(difference) +'\n')
csvfile.close()

seconds = time.time() - start_time
print 'Difference: ', difference, 'Time Taken: ', time_taken
os.system('date')
