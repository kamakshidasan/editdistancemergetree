# Display Split Tree, Persistence Diagram with Threshold and a Spreadsheet!
# Note: Camera Position will change according to input data.
# Workaround: Trace + Click on Z- Axis icon on top + Paste Camera Position

from paraview.simple import *
import csv, os
from datetime import datetime
from helper import *

paraview.simple._DisableFirstRenderCameraReset()

# start timer
startTime = datetime.now()

# initialize Path variables
# file name with extension
full_file_name = 'adhitya.vtk'
parent_path = cwd()
data_path = get_input_path(parent_path)
file_path = join_file_path(data_path, full_file_name)
file_name = get_file_name(full_file_name)

# create a new 'Legacy VTK Reader'
vtkFile = LegacyVTKReader(FileNames=[file_path])
simplification_percentage = 3

# show data in view
renderView1 = GetActiveViewOrCreate('RenderView')
vtkFileDisplay = Show(vtkFile, renderView1)
vtkFileDisplay.Representation = 'Slice'

# reset view based on data extents
renderView1.ResetCamera()
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [200, 150, 1500]
renderView1.CameraFocalPoint = [200, 150, 0]
renderView1.CameraParallelScale = 400

# show color bar/color legend and transfer function
vtkFileDisplay.SetScalarBarVisibility(renderView1, True)
GetColorTransferFunction('volume_scalars')

# create a new 'Clean to Grid'
cleantoGrid1 = CleantoGrid(Input=vtkFile)
cleantoGrid1Display = Show(cleantoGrid1, renderView1)
Hide(vtkFile, renderView1)

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(Input=cleantoGrid1)
extractSurface1Display = Show(extractSurface1, renderView1)
Hide(cleantoGrid1, renderView1)

# get new layout
layout1 = GetLayout()
layout1.SplitHorizontal(0, 0.5)

# set active view
SetActiveView(None)

# create and place a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [545, 680]
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.StereoType = 0
renderView2.Background = [0.32, 0.34, 0.43]

# create a Persistence Diagram for input scalar field
persistenceDiagram = TTKPersistenceDiagram(Input=extractSurface1)
persistenceDiagramDisplay = Show(persistenceDiagram, renderView2)
persistenceDiagramDisplay.Representation = 'Surface'
persistenceDiagram = GetActiveSource()
persistenceDiagram.UseInputOffsetField = 1

# reset view based on data extents
renderView2.ResetCamera()
renderView2.InteractionMode = '2D'
renderView2.CameraPosition = [0, 0.5, 10000.0]
renderView2.CameraFocalPoint = [0, 0.5, 0.0]


# create Threshold for Persistence

# find max persistence by iterating across the diagram! 
persistence_data = servermanager.Fetch(persistenceDiagram)

# Get the number of persistent points and arcs
num_persistent_points = persistenceDiagram.GetDataInformation().GetNumberOfPoints()
num_persistent_cells = persistenceDiagram.GetDataInformation().GetNumberOfCells()

max_persistence = 0
for index in range(num_persistent_cells):
	current_persistence = persistence_data.GetCellData().GetArray('Persistence').GetValue(index)
	max_persistence = max(current_persistence, max_persistence)

persistenceThreshold = Threshold(Input=persistenceDiagram)
persistenceThreshold.Scalars = ['CELLS', 'Persistence']

# filter all persistent pairs above minimum persistence threshold
min_persistence = (simplification_percentage *  max_persistence) / 100.0
persistenceThreshold.ThresholdRange = [min_persistence, max_persistence]

Hide(persistenceDiagram, renderView2)
persistenceThresholdDisplay = Show(persistenceThreshold, renderView2)


# set active view and source
SetActiveView(renderView1)
SetActiveSource(vtkFile)

# create a new 'TTK TopologicalSimplification'
tTKTopologicalSimplification1 = TTKTopologicalSimplification(Domain=extractSurface1,
    Constraints=persistenceThreshold)
tTKTopologicalSimplification1.UseInputOffsetField = 1
tTKTopologicalSimplification1Display = Show(tTKTopologicalSimplification1, renderView1)
Hide(extractSurface1, renderView1)

# create a new 'TTK ContourForests'
contourForest = TTKContourForests(Input=tTKTopologicalSimplification1)
contourForest.UseInputOffsetField = 1
contourForest.TreeType = 'Split Tree'
contourForest.ArcSampling = 0
contourForest.ArcSmoothing = 100.0
tree_type = get_tree_type(contourForest.TreeType)

# show Nodes data in view
contourForestDisplayNodes = Show(contourForest, renderView1)
contourForestDisplayNodes.Representation = 'Surface'
Hide(tTKTopologicalSimplification1, renderView1)
contourForestDisplayNodes.SetScalarBarVisibility(renderView1, True)

# show Arcs data in view
contourForestDisplayArcs = Show(OutputPort(contourForest, 1), renderView1)
contourForestDisplayArcs.Representation = 'Surface'
contourForestDisplayArcs.SetScalarBarVisibility(renderView1, True)

# show Segmentation data in view
contourForestDisplaySegmentation = Show(OutputPort(contourForest, 2), renderView1)
contourForestDisplaySegmentation.Representation = 'Surface'
contourForestDisplaySegmentation.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(contourForest)

# create Spheres for Critical Points
tTKSphereFromPoint1 = TTKSphereFromPoint(Input=contourForest)
tTKSphereFromPoint1.Radius = 10.0
tTKSphereFromPoint1Display = Show(tTKSphereFromPoint1, renderView1)
tTKSphereFromPoint1Display.Representation = 'Surface'
Hide(contourForest, renderView1)
ColorBy(tTKSphereFromPoint1Display, ('POINTS', 'NodeType'))
tTKSphereFromPoint1Display.RescaleTransferFunctionToDataRange(True, False)
tTKSphereFromPoint1Display.SetScalarBarVisibility(renderView1, True)
GetColorTransferFunction('NodeType')

# set active source
SetActiveSource(contourForest)

# create Tubes for Arcs
tube1 = Tube(Input=OutputPort(contourForest,1))
tube1.Vectors = [None, '']
tube1Display = Show(tube1, renderView1)
tube1Display.Representation = 'Surface'
tube1Display = GetDisplayProperties(tube1, view=renderView1)
ColorBy(tube1Display, ('CELLS', 'Type'))

# display initial scalar field
Hide(OutputPort(contourForest,2), renderView1)
Show(vtkFile, renderView1)
SetActiveSource(None)

# set active view
SetActiveView(renderView2)

# create a Persistence Diagram for input scalar field
Hide(persistenceThreshold, renderView2)
persistenceDiagramSimplified = TTKPersistenceDiagram(Input=tTKTopologicalSimplification1)
persistenceDiagramSimplifiedDisplay = Show(persistenceDiagramSimplified, renderView2)
persistenceDiagramSimplifiedDisplay.Representation = 'Surface'
persistenceDiagramSimplified = GetActiveSource()
persistenceDiagramSimplified.UseInputOffsetField = 1

# get layout
layout2 = GetLayout()
layout2.SplitVertical(2, 0.5)
SetActiveView(None)

# create SpreadSheet View for displaying data
spreadSheetView1 = CreateView('SpreadSheetView')
layout2.AssignView(6, spreadSheetView1)

# Write node of contour tree to file
contourForestDisplayNodes = Show(contourForest, spreadSheetView1)
nodes_file_arguments = [tree_type, NODES_INFIX, file_name, CSV_EXTENSION]
nodes_file_path = get_output_path(file_path, nodes_file_arguments, folder_name = INTERMEDIATE_FOLDER)
ExportView(nodes_file_path, view=spreadSheetView1, FilterColumnsByVisibility=1)

# Write arcs of contour tree to file
contourForestDisplayArcs = Show(OutputPort(contourForest,1), spreadSheetView1)
arcs_file_arguments = [tree_type, ARCS_INFIX, file_name, CSV_EXTENSION]
arcs_file_path = get_output_path(file_path, arcs_file_arguments, folder_name = INTERMEDIATE_FOLDER)
ExportView(arcs_file_path, view=spreadSheetView1, FilterColumnsByVisibility=1)

# Write persistent pairs after thresholding to file
pairs_file_arguments = [tree_type, PAIRS_INFIX, file_name, CSV_EXTENSION]
pairs_file_path = get_output_path(file_path, pairs_file_arguments, folder_name = PAIRS_FOLDER)

pairs_file = open(pairs_file_path, 'w')
fieldnames = ['Birth', 'Death']
writer = csv.writer(pairs_file, delimiter=',')
writer.writerow(fieldnames)
birth_vertex = None

# The persistent pairs are one after the other
# First comes birth; immediately followed by death [Adhitya getting philosophical :P]

# Iterate over all the points in the persistent diagram
persistence_threshold_data = servermanager.Fetch(persistenceDiagramSimplified)
# Get the number of persistent points and arcs
num_persistent_threshold_points = persistenceDiagramSimplified.GetDataInformation().GetNumberOfPoints()

for index in range(num_persistent_threshold_points):
	vertex_id = persistence_threshold_data.GetPointData().GetArray('VertexIdentifier').GetValue(index)

	# If index is even, we are processing death; else just store attributes of birth
	# When death occurs, find persistence and moksha.
	if index & 1:
		death_vertex = vertex_id
		content = [birth_vertex, death_vertex]
		writer.writerow(content)
	else:
		birth_vertex = vertex_id

pairs_file.close()

# initialize dictionaries
scalars = {}
coords = {}
previous_critical_index = None
previous_critical_scalar = None

with open(nodes_file_path, 'rb') as csvfile:
	csvfile.readline() 
	spamreader = csv.reader(csvfile, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		x = int(row[5])
		y = int(row[6])
		z = int(row[7])
		incorrect_vertex_index = int(row[3])
		scalar_value = float(row[0])
		coords[(x,y,z)] = incorrect_vertex_index
		scalars[incorrect_vertex_index] = scalar_value

# Write the Merge Tree to file
tree_file_arguments = [tree_type, TREE_INFIX, file_name, CSV_EXTENSION]
tree_file_path = get_output_path(file_path, tree_file_arguments, folder_name = TREES_FOLDER)

tree_file = open(tree_file_path, 'w')
fieldnames = ['Node:0', 'Node:1', 'Scalar:0', 'Scalar:1']
writer = csv.writer(tree_file, delimiter=',')
writer.writerow(fieldnames)	

# Read the intermediate arcs file
with open(arcs_file_path, 'rb') as csvfile:
	csvfile.readline()
	spamreader = csv.reader(csvfile, delimiter=' ')
	for index, r in enumerate(spamreader):
		row = r[0].split(',')
		x = int(row[4])
		y = int(row[5])
		z = int(row[6])
		incorrect_vertex_index = coords[(x,y,z)]
		vertex_scalar = scalars[incorrect_vertex_index]

		if index & 1:
			content = [previous_critical_index, incorrect_vertex_index, previous_critical_scalar, vertex_scalar]
			writer.writerow(content)
		else:
			previous_critical_index = incorrect_vertex_index
			previous_critical_scalar = vertex_scalar

tree_file.close()

# Write the persistence diagram after thresholding of only the super/sub level-set [for usage by TDA]
pairs_file_arguments = [tree_type, PAIRS_INFIX, file_name, CSV_EXTENSION]
pairs_file_path = get_output_path(file_path, pairs_file_arguments, folder_name = PERSISTENCE_FOLDER)

pairs_file = open(pairs_file_path, 'w')
fieldnames = ['dimension', 'Death', 'Birth']
writer = csv.writer(pairs_file, delimiter=',')
writer.writerow(fieldnames)
birth_vertex = None
birth_scalar = None
write_row = True

# The persistent pairs are one after the other
# First comes birth; immediately followed by death [Adhitya getting philosophical :P]

# Iterate over all the points in the persistent diagram
persistence_threshold_data = servermanager.Fetch(persistenceDiagramSimplified)
# Get the number of persistent points and arcs
num_persistent_threshold_points = persistenceDiagramSimplified.GetDataInformation().GetNumberOfPoints()

# Iterate across all points in diagram and write persistent pairs
for index in range(num_persistent_threshold_points):
	vertex_id = persistence_threshold_data.GetPointData().GetArray('VertexIdentifier').GetValue(index)
	try:
		vertex_scalar = scalars[vertex_id]
		if index & 1:
			death_vertex = vertex_id
			death_scalar = vertex_scalar
			# There exist values which are not present in the merge-tree
			if write_row:
				content = [0, round(death_scalar,4), round(birth_scalar,4)]
				writer.writerow(content)
				print content
			write_row = True
		else:
			birth_vertex = vertex_id
			birth_scalar = vertex_scalar
			write_row = True
	except:
		# This row contains a value not present in the merge-tree
		write_row = False
		pass

pairs_file.close()


# take screenshot of scalar field
screen_file_arguments = [tree_type, SCREENSHOT_INFIX, file_name, PNG_EXTENSION]
screen_file_path = get_output_path(file_path, screen_file_arguments, folder_name = SCREENSHOT_FOLDER)
SaveScreenshot(screen_file_path, magnification=1, quality=100, view=renderView1)

print datetime.now() - startTime, 'Done! :)'

os._exit(0)

