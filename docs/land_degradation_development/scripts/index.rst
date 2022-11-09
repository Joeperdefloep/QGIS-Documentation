Making custom scripts with additional functionality
===================================================

One of the reasons QGIS is considered more advanced, is because you will quickly get
into making your own scripts to extend the functionality. We also have to do that some
times in the practical. There, the scripts were provided. However, if you want to do
some more advanced things yourself, it is very useful to know a little bit how to make
your own scripts.

The basic structure in this manual for creating a script is the same:

#. Create a model with the graphic modeler with as many parameters already loaded
#. Export the model to a Python script
#. Add parameters (inputs/outputs) that could not be added in the graphical modeler
#. convert the parameters to actual things that we can work with (such as numbers
   (int/float) or text (string))
#. perform the calculations/processing with the parameters/algorithms
#. maybe some post-processing to properly name outputs.

.. toctree::
   :maxdepth: 2

   annular_mask
   rasterizing