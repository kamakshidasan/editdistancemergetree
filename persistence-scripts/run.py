import fileinput
import re
import os

def file_replace(fname, pat, s_after):
    # first, see if the pattern is even in the file.
    with open(fname) as f:
        if not any(re.search(pat, line) for line in f):
            return # pattern does not occur in file so we are done.

    # pattern is in the file, so perform replace operation.
    with open(fname) as f:
        out_fname = fname + ".tmp"
        out = open(out_fname, "w")
        for line in f:
            out.write(re.sub(pat, s_after, line))
        out.close()
        os.rename(out_fname, fname)

working_directory = '/home/nagarjun/Desktop/bitbucket/editdistancemergetree/persistence-scripts/'

file_list = os.listdir(working_directory + 'input/')
wildcard = 'adhitya.vtk'

file_list.insert(0, wildcard)

for i in range(1, len(file_list)):
	file_replace(working_directory + 'get-persistence-fast.py', file_list[i-1], file_list[i])
	os.system('paraview --script=get-persistence-fast.py')
	print file_list[i] + ' Done! :)'

file_replace(working_directory + 'get-persistence-fast.py', file_list[i], wildcard)

print 'Persistence Diagrams computed :)'
