|moderate| |FA| Creating a script for aligning rasters
======================================================

In this practical, due to the high number of operations, it can happen that
rasters misalign by floating-point errors. In this case, SAGA algorithms will
not run. In this exercise, we will put this into a script, so that we can use it in the graphical modeler.
into a script in this exercise.

Creating the model
..................

Create a model named :file:`align` and give it two inputs:

* |rasterLayer| :file:`input`
* |rasterLayer| :file:`align`


