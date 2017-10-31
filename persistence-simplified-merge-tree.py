#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
tv_174vtk = LegacyVTKReader(FileNames=['/home/nagarjun/Desktop/adhitya/data/tv_174.vtk'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1100, 680]

# show data in view
tv_174vtkDisplay = Show(tv_174vtk, renderView1)
# trace defaults for the display properties.
tv_174vtkDisplay.Representation = 'Slice'

# reset view to fit data
renderView1.ResetCamera()

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [149.5, 149.5, 10000.0]
renderView1.CameraFocalPoint = [149.5, 149.5, 0.0]

# show color bar/color legend
tv_174vtkDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'volume_scalars'
volume_scalarsLUT = GetColorTransferFunction('volume_scalars')

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitHorizontal(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [545, 680]
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.StereoType = 0
renderView2.Background = [0.32, 0.34, 0.43]

# place view in the layout
layout1.AssignView(2, renderView2)

# create a new 'TTK PersistenceDiagram'
tTKPersistenceDiagram1 = TTKPersistenceDiagram(Input=tv_174vtk)

# show data in view
tTKPersistenceDiagram1Display = Show(tTKPersistenceDiagram1, renderView2)
# trace defaults for the display properties.
tTKPersistenceDiagram1Display.Representation = 'Surface'

# reset view to fit data
renderView2.ResetCamera()

#changing interaction mode based on data extents
renderView2.InteractionMode = '2D'
renderView2.CameraPosition = [5.86147143621929e-05, 0.49984899163246155, 10000.0]
renderView2.CameraFocalPoint = [5.86147143621929e-05, 0.49984899163246155, 0.0]

# create a new 'Threshold'
threshold1 = Threshold(Input=tTKPersistenceDiagram1)

# Properties modified on threshold1
threshold1.Scalars = ['CELLS', 'Persistence']
threshold1.ThresholdRange = [0.05, 1.9993959076057357]

# show data in view
threshold1Display = Show(threshold1, renderView2)
# trace defaults for the display properties.
threshold1Display.Representation = 'Surface'

# hide data in view
Hide(tTKPersistenceDiagram1, renderView2)

# destroy renderView2
Delete(renderView2)
del renderView2

# close an empty frame
layout1.Collapse(2)

# set active view
SetActiveView(renderView1)

# set active source
SetActiveSource(tv_174vtk)

# create a new 'Clean to Grid'
cleantoGrid1 = CleantoGrid(Input=tv_174vtk)

# show data in view
cleantoGrid1Display = Show(cleantoGrid1, renderView1)
# trace defaults for the display properties.
cleantoGrid1Display.Representation = 'Surface'

# hide data in view
Hide(tv_174vtk, renderView1)

# show color bar/color legend
cleantoGrid1Display.SetScalarBarVisibility(renderView1, True)

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(Input=cleantoGrid1)

# show data in view
extractSurface1Display = Show(extractSurface1, renderView1)
# trace defaults for the display properties.
extractSurface1Display.Representation = 'Surface'

# hide data in view
Hide(cleantoGrid1, renderView1)

# show color bar/color legend
extractSurface1Display.SetScalarBarVisibility(renderView1, True)

# create a new 'TTK TopologicalSimplification'
tTKTopologicalSimplification1 = TTKTopologicalSimplification(Domain=extractSurface1,
    Constraints=threshold1)

# Properties modified on tTKTopologicalSimplification1
tTKTopologicalSimplification1.UseInputOffsetField = 1

# show data in view
tTKTopologicalSimplification1Display = Show(tTKTopologicalSimplification1, renderView1)
# trace defaults for the display properties.
tTKTopologicalSimplification1Display.Representation = 'Surface'

# hide data in view
Hide(extractSurface1, renderView1)

# show color bar/color legend
tTKTopologicalSimplification1Display.SetScalarBarVisibility(renderView1, True)

# create a new 'TTK ContourForests'
tTKContourForests1 = TTKContourForests(Input=tTKTopologicalSimplification1)

# Properties modified on tTKContourForests1
tTKContourForests1.UseInputOffsetField = 1
tTKContourForests1.TreeType = 'Split Tree'
tTKContourForests1.ArcSampling = 0
tTKContourForests1.ArcSmoothing = 100.0

# show data in view
tTKContourForests1Display = Show(tTKContourForests1, renderView1)
# trace defaults for the display properties.
tTKContourForests1Display.Representation = 'Surface'

# hide data in view
Hide(tTKTopologicalSimplification1, renderView1)

# show color bar/color legend
tTKContourForests1Display.SetScalarBarVisibility(renderView1, True)

# show data in view
tTKContourForests1Display_1 = Show(OutputPort(tTKContourForests1, 1), renderView1)
# trace defaults for the display properties.
tTKContourForests1Display_1.Representation = 'Surface'

# hide data in view
Hide(tTKTopologicalSimplification1, renderView1)

# show color bar/color legend
tTKContourForests1Display_1.SetScalarBarVisibility(renderView1, True)

# show data in view
tTKContourForests1Display_2 = Show(OutputPort(tTKContourForests1, 2), renderView1)
# trace defaults for the display properties.
tTKContourForests1Display_2.Representation = 'Surface'

# hide data in view
Hide(tTKTopologicalSimplification1, renderView1)

# show color bar/color legend
tTKContourForests1Display_2.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(tTKContourForests1)

# set active source
SetActiveSource(tTKContourForests1)

# create a new 'TTK SphereFromPoint'
tTKSphereFromPoint1 = TTKSphereFromPoint(Input=tTKContourForests1)

# Properties modified on tTKSphereFromPoint1
tTKSphereFromPoint1.Radius = 10.0

# show data in view
tTKSphereFromPoint1Display = Show(tTKSphereFromPoint1, renderView1)
# trace defaults for the display properties.
tTKSphereFromPoint1Display.Representation = 'Surface'

# hide data in view
Hide(tTKContourForests1, renderView1)

# show color bar/color legend
tTKSphereFromPoint1Display.SetScalarBarVisibility(renderView1, True)

# set scalar coloring
ColorBy(tTKSphereFromPoint1Display, ('POINTS', 'NodeType'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(volume_scalarsLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
tTKSphereFromPoint1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
tTKSphereFromPoint1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'NodeType'
nodeTypeLUT = GetColorTransferFunction('NodeType')

# set active source
SetActiveSource(tTKContourForests1)

# find source
tTKContourForests1_1 = FindSource('TTKContourForests1')

# create a new 'Tube'
tube1 = Tube(Input=OutputPort(tTKContourForests1_1,1))

# Properties modified on tube1
tube1.Vectors = [None, '']

# show data in view
tube1Display = Show(tube1, renderView1)
# trace defaults for the display properties.
tube1Display.Representation = 'Surface'

# hide data in view
Hide(OutputPort(tTKContourForests1, 1), renderView1)

# show color bar/color legend
tube1Display.SetScalarBarVisibility(renderView1, True)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(volume_scalarsLUT, renderView1)

# change solid color
tube1Display.DiffuseColor = [0.0, 0.6666666666666666, 0.0]

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [149.5, 149.5, 10000.0]
renderView1.CameraFocalPoint = [149.5, 149.5, 0.0]
renderView1.CameraParallelScale = 211.4249275747777

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
