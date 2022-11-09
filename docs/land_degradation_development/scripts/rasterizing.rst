.. _create_rasterize_script:

|hard| |FA| Making a script for batch rasterizing (Optional)
------------------------------------------------------------

.. note::

   This solution has been given `on stackexchange <https://gis.stackexchange.com/a/414677/156742>`_

During rasterization in the previous exercise, we had to hard-code some values
and it was quite cumbersome. In this exercise we will be making a script where
we can select all fields that we want rasterized. Then, we will adjust the model.

.. warning::
   This is a |hard| hard exercise. Do not get lost in this, but only follow if
   you have extra time. The entire script is provided at the end. You may want
   to copy that if you lack time. Also, all exercises can be finished by
   copy-pasting the |gdal| Rasterize algorithm as in
   :numref:`fig_rasterize_manual`.

Making a script is very similar to making a model. In fact, all models can be
exported to a Python script. This is very useful so we can get the skeleton of
the script by making a model.
What we eventually want is a tool like this:

.. figure:: img/script_prompt.png
   :align: center

   The batch rasterization prompt. All :guilabel:`Fields to select` will be
   turned into rasters, saved as :file:`.tiff` files inside :file:`01_input`
   folder. 

Creating a template model
.........................

#. Create a model and drag in the following inputs:
   
   * |signPlus| Raster Layer: :file:`like raster`
   * |signPlus| Vector Layer: :file:`Vector`
   * |signPlus| Vector Fields: :file:`Fields to rasterize`
     
     * :guilabel:`Parent layer`: :file:`vector`:
     * :guilabel:`Allowed data type`: :file:`number`
     * |checkbox|:guilabel:`Accept multiple fields`
     * |checkbox|:guilabel:`Select all fields by default`
   
   * |signPlus| File/Folder: :file:`Output folder`
   * |checkbox| |signPlus| Boolean: :file:`Load output layers`

#. Drag in the |gdal|:ref:`gdalrasterize` algorithm with:
   
   * :guilabel:`Input layer`: |processingModel|:file:`vector`
   * :guilabel:`Field to use for a burn-in value`:
     |processingModel|:file:`Fields to rasterize`
   * :guilabel:`Output raster size units`: 
     |fieldInteger|:file:`Georeferenced units`
   * :guilabel:`Output extent`: |processingModel|:file:`like raster`

#. Name the model :file:`Batch rasterize`
#. Click the |saveAsPython| *Save as Python* icon. 

Inspecting the resulting Python script
......................................

A new screen will appear with quite a long script. Let's break it down! It
starts by a *docstring* (indicated by :file:`"""`):

.. literalinclude:: scripts/batch_rasterize_raw.py
   :linenos:
   :lines: 1-6

Next, we import all necessary *classes* and *modules*:

.. literalinclude:: scripts/batch_rasterize_raw.py
   :lineno-start: 8
   :lines: 8-16
   :emphasize-lines: 1,8

Next, the start of our class starts. This is indicated by:

.. literalinclude:: scripts/batch_rasterize_raw.py
   :lineno-start: 18
   :lines: 18

.. note:: Inheritance
   Our :class:`BatchRasterize` class *inherits from*
   :class:`QgsProcessingAlgorithm <qgis.core.QgsProcessingAlgorithm>` (indicated by the brackets).
   This means that all methods and attributes of
   :class:`QgsProcessingAlgorithm <qgis.core.QgsProcessingAlgorithm>` are also available for
   :class:`BatchRasterize`.

All later lines are indented. This means that everything defines aspects of
that class. There are two important methods:

.. literalinclude:: scripts/batch_rasterize_raw.py
   :lineno-start: 20
   :lines: 20-24

Is run at the start of the algorithm. Here we define which inputs are
available in the prompt. Note that all inputs are filled out. That's
convenient!

Next, the :class:`ProcessAlgorithm <qgis.core.ProcessAlgorithm>` function executes the actual model:

.. literalinclude:: scripts/batch_rasterize_raw.py
   :lineno-start: 26
   :lines: 26-51

* :class:`feedback <qgis.core.QgsProcessingFeedback>` is how we can
  communicate with the user.
* :file:`results` is a dictionary for results
* :file:`outputs` is a dictionary for outputs (results to be loaded into
  QGIS)
* :file:`alg_params` is a dictionary with all parameters for
  |gdal|:ref:`gdalrasterize`. As you can see, the :file:`EXTENT`,
  :file:`FIELD` and :file:`INPUT` are already set.
* :meth:`processing.run` finally runs |gdal|:ref:`gdalrasterize`. and stores
  it as :file:`RasterizeVectorToRaster` inside :file:`outputs`.

The final methods define the name and group of the tool and speak for themselves
(We also do not need to change these):

.. literalinclude:: scripts/batch_rasterize_raw.py
   :lineno-start: 53
   :lines: 53-66

Converting parameters to layers
...............................

.. admonition:: Solution
   :class: dropdown

   If you didn't follow the above |FA|, you can use the below script. 

   #. In the Processig Toolkbox, click the 
      |pythonFile|:menuselection:`--> Create New Script...`
   #. copy-paste the following code:

   .. literalinclude:: scripts/batch_rasterize_final.py
      :linenos:


.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |FA| replace:: Follow Along:
.. |checkbox| image:: /static/common/checkbox.png
   :width: 1.3em
.. |fieldInteger| image:: /static/common/mIconFieldInteger.png
   :width: 1.5em
.. |gdal| image:: /static/common/gdal.png
   :width: 1.5em
.. |hard| image:: /static/common/hard.png
.. |processingModel| image:: /static/common/processingModel.png
   :width: 1.5em
.. |pythonFile| image:: /static/common/mIconPythonFile.png
   :width: 1.5em
.. |saveAsPython| image:: /static/common/mActionSaveAsPython.png
   :width: 1.5em
.. |signPlus| image:: /static/common/symbologyAdd.png
   :width: 1.5em
