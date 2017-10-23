#### import the simple module from the paraview
from paraview.simple import *
import os, csv, sys
import subprocess
from helper import *

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

file_path = '/home/raghavendra/Desktop/persistence-distances/input/tv_3.vtk'
persistence_theshold = 0.1

file_name = get_file_name(file_path)
parent_path = get_parent_path(file_path)

# create a new 'Legacy VTK Reader'
vtkFile = LegacyVTKReader(FileNames=[file_path])

# display data
renderView1 = GetActiveViewOrCreate('RenderView')
vtkFileDisplay = Show(vtkFile, renderView1)

# reset view to fit data
renderView1.ResetCamera()
renderView1.InteractionMode = '2D'

# show color bar/color legend
vtkFileDisplay.SetScalarBarVisibility(renderView1, True)

# get color and opacity transfer function/color map for 'volume_scalars'
volume_scalarsLUT = GetColorTransferFunction('volume_scalars')
volume_scalarsPWF = GetOpacityTransferFunction('volume_scalars')

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitHorizontal(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'Render View'
renderView2 = CreateView('RenderView')

# place view in the layout
layout1.AssignView(2, renderView2)

# create and show'TTK PersistenceDiagram'
persistenceDiagram = TTKPersistenceDiagram(Input=vtkFile)
persistenceDiagramDisplay = Show(persistenceDiagram, renderView2)

# reset view to fit data
renderView2.ResetCamera()
renderView2.InteractionMode = '2D'

# split cell
layout1.SplitVertical(2, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')

# place view in the layout
layout1.AssignView(6, spreadSheetView1)

# show persistence data in view
persistenceDiagramDisplay_1 = Show(persistenceDiagram, spreadSheetView1)

# get paths for new intermediate output files
persistent_points = get_output_path(file_path, [PERSISTENCE_POINTS_SUFFIX, CSV_EXTENSION])
persistent_cells = get_output_path(file_path, [PERSISTENCE_CELLS_SUFFIX, CSV_EXTENSION])
input_field = get_output_path(file_path, [FIELD_DATA_SUFFIX, CSV_EXTENSION])

# export view
ExportView(persistent_points, view=spreadSheetView1)
ExportView(persistent_cells, view=spreadSheetView1)

# show input data in view
vtkFileDisplay_1 = Show(vtkFile, spreadSheetView1)

# export view
ExportView(input_field, view=spreadSheetView1)

num_persistent_points = persistenceDiagram.GetDataInformation().GetNumberOfPoints()

vtk_data = servermanager.Fetch(vtkFile)
persistence_data = servermanager.Fetch(persistenceDiagram)

#print persistenceDiagram.CellData.GetArray(0)
#print persistence_data.GetCellData().GetArray(0).GetValue(0)

birth_scalar = None
birth_vertex = None
birth_type = None

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
		death_scalar = scalar_value
		death_vertex = vertex_id
		death_type = vertex_type
		
		persistence = death_scalar - birth_scalar

		if persistence > persistence_theshold:
			print round(death_scalar, 3), round(birth_scalar, 3), round(persistence, 3)
	
	# Store for next time
	else:
		birth_scalar = scalar_value
		birth_vertex = vertex_id
		birth_type = vertex_type

# Close Paraview instance
os._exit(0)
