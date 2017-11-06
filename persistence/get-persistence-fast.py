# Get the persistence diagram
# This has been made faster by not rendering elements on Paraview ~ Do *not* use this script for debugging!

from paraview.simple import *
import os, csv, sys
import subprocess
from helper import *

# Input file path for which persistence diagram should be computed
#file_path = '/home/nagarjun/Desktop/persistence-distances/persistence/input/adhitya.vtk'
file_path = '/home/nagarjun/Desktop/bitbucket/editdistancemergetree/persistence/input/tv_176.vtk'

# Only pairs having persistence above this theshold will be considered
persistence_theshold = 0.0

# Get naming conventions
file_name = get_file_name(file_path)
parent_path = get_parent_path(file_path)

# Render a screen - useless for this script but chill
renderView = GetActiveViewOrCreate('RenderView')

# create a reader for VTK file and compute the diagram
vtkFile = LegacyVTKReader(FileNames=[file_path])
persistenceDiagram = TTKPersistenceDiagram(Input=vtkFile)

# Show() is a proxy - simply tricking Paraview here
vtkFileDisplay = Show(vtkFile, renderView)
persistenceDiagramDisplay = Show(persistenceDiagram, renderView)

# Get the number of persistent points
num_persistent_points = persistenceDiagram.GetDataInformation().GetNumberOfPoints()

# Probably the most important discovery today! :D
# To get the array data use Fetch()
vtk_data = servermanager.Fetch(vtkFile)
persistence_data = servermanager.Fetch(persistenceDiagram)

# To find the name of the Array
# print persistenceDiagram.CellData.GetArray(0)

birth_scalar = None
birth_vertex = None
birth_type = None

# Prepare file for writing
pairs_file_path = get_output_path(file_path, [PERSISTENCE_PAIRS_SUFFIX, CSV_EXTENSION])
pairs_file = open(pairs_file_path, 'w')

#fieldnames = ['dimension', 'birth_vertex', 'birth', 'birth_type', 'death_vertex', 'death', 'death_type', 'persistence', 'pair_type']
fieldnames = ['dimension', 'Death', 'Birth']

writer = csv.writer(pairs_file, delimiter=',')
writer.writerow(fieldnames)

# The persistent pairs are one after the other
# First comes birth; immediately followed by death [Adhitya getting philosophical :P]

# Iterate over all the points in the persistent diagram
for index in range(num_persistent_points):
	vertex_id = persistence_data.GetPointData().GetArray('VertexIdentifier').GetValue(index)
	vertex_type = persistence_data.GetPointData().GetArray('NodeType').GetValue(index)
	
	# We can find the scalar value of the vertex from the input scalar field
	scalar_value = vtk_data.GetPointData().GetArray('volume_scalars').GetValue(vertex_id)

	#print vertex_id, scalar_value
	
	# If index is even, we are processing death; else just store attributes of birth
	# When death occurs, find persistence and moksha.
	if index & 1:

		# We can find the pair type for each such pair [Laziness of not wanting to compute later]
		pair_type = persistence_data.GetCellData().GetArray('PairType').GetValue((index-1)/2)
		
		death_scalar = scalar_value
		death_vertex = vertex_id
		death_type = vertex_type
		
		persistence = death_scalar - birth_scalar

		if persistence > persistence_theshold:
			content = [0, death_scalar, birth_scalar]

			if (birth_type == 0 or death_type == 0):
				writer.writerow(content)
				print round(death_scalar, 3), round(birth_scalar, 3), round(persistence, 3), vertex_type
			else:
				print "Discarded: ", death_vertex, birth_vertex
	
	# Store for next time
	else:
		birth_scalar = scalar_value
		birth_vertex = vertex_id
		birth_type = vertex_type

pairs_file.close()

# Close Paraview instance
#os._exit(0)
