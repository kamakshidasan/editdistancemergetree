# Edit Distance

To be able to run code from this repository, install TTK using [these](https://topology-tool-kit.github.io/installation.html) guidlelines. This code has been tested with TTK 0.96 on Ubuntu 16.04/MacOS High Sierra. 

This repository provides code to perform the following tasks.

- Display a scalar field
- Compute its persistence diagram
- Simplify scalar field using persistence diagram
- Display critical points
- Compute Merge Trees

- Edit Distance between Merge Trees
- Face Segmentation based on Merge Trees

To run the code:

- Place your data within a folder titled 'input'
- For details on other folders you may want to create, look into `helper.py` and `compute.py`
- Then execute, `python run.py`
- To run TTK parallelly, execute `python test.py <number of cores> <start_index> <end_index>

For more information on Edit Distances, refer to Sridharamurthy et al., Edit distances for comparing merge trees. [link](http://vgl.csa.iisc.ac.in/pub/paper.php?pid=054)
For more information on Face Segmentation, refer to Sharma and Natarajan, On-Demand Augmentation of Contour Trees. [link](http://vgl.serc.iisc.ernet.in/pub/paper.php?pid=055)

