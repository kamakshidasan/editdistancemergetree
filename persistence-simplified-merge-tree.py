# Display Split Tree, Persistence Diagram with Threshold and a Spreadsheet!
# Note: Camera Position will change according to input data.
# Workaround: Trace + Click on Z- Axis icon on top + Paste Camera Position

from paraview.simple import *

# create a new 'Legacy VTK Reader'
vtkFile = LegacyVTKReader(FileNames=['/home/nagarjun/Desktop/adhitya/data/tv_101.vtk'])

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

# get new layout
layout1 = GetLayout()
layout1.SplitHorizontal(0, 0.5)

# set active view
SetActiveView(None)

# create and place a new 'Render View'
renderView2 = CreateView('RenderView')
layout1.AssignView(2, renderView2)

# create a Persistence Diagram for input scalar field
persistenceDiagram = TTKPersistenceDiagram(Input=vtkFile)
persistenceDiagramDisplay = Show(persistenceDiagram, renderView2)

# reset view based on data extents
renderView2.ResetCamera()
renderView2.InteractionMode = '2D'
renderView2.CameraPosition = [0, 0.5, 10000.0]
renderView2.CameraFocalPoint = [0, 0.5, 0.0]

# create Threshold for Persistence
########################################################################
# ADHITYA : Find max persistence by iterating across the diagram! 
#######################################################################

persistenceThreshold = Threshold(Input=persistenceDiagram)
persistenceThreshold.Scalars = ['CELLS', 'Persistence']
persistenceThreshold.ThresholdRange = [0.05, 1.9]
persistenceThresholdDisplay = Show(persistenceThreshold, renderView2)

# set active view and source
SetActiveView(renderView1)
SetActiveSource(vtkFile)

# create a new 'Clean to Grid'
cleantoGrid1 = CleantoGrid(Input=vtkFile)
cleantoGrid1Display = Show(cleantoGrid1, renderView1)
Hide(vtkFile, renderView1)

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(Input=cleantoGrid1)
extractSurface1Display = Show(extractSurface1, renderView1)
Hide(cleantoGrid1, renderView1)

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

# get layout
layout2 = GetLayout()
layout2.SplitVertical(2, 0.5)
SetActiveView(None)

# create SpreadSheet View for displaying data
spreadSheetView1 = CreateView('SpreadSheetView')
layout2.AssignView(6, spreadSheetView1)

# show nodes of computed contour forest in view
contourForestDisplayNodes = Show(contourForest, spreadSheetView1)
