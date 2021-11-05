=======================
Pre-processing the data
=======================

In GIS you always need to process the raw data, to make it suitable as input for
your application. We consider this as the first step in the process. In total
there are three different phases: the pre-processing phase, where the input data
will be created from the raw data. The second phase is the processing, where
every step in the MMF method will be completed. The last phase is combining the
different steps to the complete model.

.. figure:: img/preprocessing_chart.png
   :align: center

   Flowchart for the complete preprocessing workflow.

|basic| Managing files for processing
-------------------------------------

Even though GeoPackages are very useful for easy sharing of data, there are some
small quirks when opening rasters from them for models we made ourselves.
Therefore, we will be dumping all our rasters in a folder. 

#. Create a folder :file:`01_input` inside :file:`GIS_files`.

|basic| |FA| Updating :guilabel:`Hadocha_landuse`
-------------------------------------------------

Since updating the landuse map has the shortest workflow, we'll work on that
first. The data in :file:`data/Hadocha_landuse.xlsx` still needs some editing.

Pre-processing the tabular data
...............................

#. Open :file:`data/Hadocha_data.xlsx` in a spreadsheet editor like Libreoffice
   Calc
#. In the :guilabel:`landuse_properties_table` tab, have a look at the data. As
   you can see, the Cropland data is not annual, but hs different values for
   each month. Since the MMF model is annual, we need annual data. Calculate the
   annual intercepted rainfall (:math:`A`) by:

   .. _eq_intercepted_rainfall: 

   .. math::
      :label: eq_rainfall

      A = \frac{A_{sow}*M_{sow}+A_{grow}*M_{grow}+A_{after}*M_{after}}{12}
    
   Where :math:`A_{sow,grow,after}` is the intercepted rainfall for that period
   (sowing, growing and after harvest) and :math:`M_{sow,grow,after}` the number
   of months in each period.

#. Calculate the other other factors by substituting :math:`A` in :ref:`eq_rainfall`
#. Make sure to name the row :file:`Cropland`

.. note::
   The rows will later be used to perform a :ref:`qgisjoinattributestable`
   operation. This will give the :guilabel:`Cropland` features of
   :guilabel:`Hadocha_landuse` the values of
   :guilabel:`landuse_properties_table`. This will only work if both rows have
   **exactly the same** names.

Joining the data
................

Even though the join operation is only a single operation, we will put it inside
a model, so we can immediately rasterize the data afterwards.

#. Create a new model named :file:`update landuse` and |fileSave| Save it.

.. note::
   Relative paths and layer selection are still not as good in QGIS. Therefore,
   will present some workarounds here that are a bit more advanced. However, for
   this model we will be using inputs. Note that since these are layers in a
   GeoPackage c.q. sheets in a spreadsheet, they have to be loaded into the
   project first.

#. We need the following inputs:

   #. Vector Layer
      
      * :guilabel:`Description` landuse
      * :guilabel:`Geometry type` |selectString|:file:`Polygon`
      * |checkbox|:guilabel:`Mandatory`
      * |unchecked|:guilabel:`Advanced`

   #. Vector field
      
      * :guilabel:`Description` :file:`Landuse join field`
      * :guilabel:`Parent layer` |selectString|:file:`Landuse`
      * :guilabel:`Allowed data type` |selectString|:file:`String`
      * |unchecked|:guilabel:`Accept multiple fields`
      * :guilabel:`Default value: :file:`FEATURE`
    
   #. Vector Layer
       
      * :guilabel:`Description` :file:`Landuse properties`
      * :guilabel:`Geometry type` |selectString|:file:`No geometry required`
    
   #. Vector field

      * :guilabel:`Description` :file:`properties table join field`
      * :guilabel:`Parent layer` |selectString|:file:`Landuse properties`
      * :guilabel:`Allowed data type` |selectString|:file:`String`
      * |unchecked|:guilabel:`Accept multiple fields`
      * :guilabel:`Default value: :file:`Landuse`

#. Drag the |logo| :ref:`qgisjoinattributestable` algorithm into the modeler.
   
   * :guilabel:`Input layer`:  |processingModel| :file:`Landuse`
   * :guilabel:`Table field`: |processingModel| :file:`Landuse join field` 
   * :guilabel:`Input layer 2`: |processingModel| :file:`Landuse properties`
   * :guilabel:`Table field 2`: |processingModel| :file:`Properties table join field`
   * |processingOutput|:guilabel:`Joined layer [optional]`: :file:`Landuse_joined` 
   
#. |play|Run the model and look at the attribute table. It should look like
   this:
   
   .. figure:: img/landuse_joined_table.png
      :align: center

   Note that there may be additional, unnecessary columns like :file:`Field9`
   with all :file:`NULL` values. These are okay.

   .. note::
      It may be that your Cropland row will have all *NULL* values. If that is
      the case, check:

      #. If you have calculated the values
      #. It may be that the values don't load if they are a formula. This should
         be a bug and is hopefully solved soon. Replace your formulas with the
         resulting numbers!

Rasterizing the results
.......................

Now, we will be going to rasterize all our outputs. This is done by the
|gdal|:ref:`gdalrasterize` process. This is a bit repetitive and some things
such as pixel size need to be hard-coded. 

#. We will need another input |signPlus| Raster Layer called 
   :file:`reference layer`. This is the layer that will be used to calculate the
   extent.
#. Drag a |gdal|:ref:`gdalrasterize` into the graphical modeler and give it the
   following parameters:

   * :guilabel:`Description`: :file:`Intercepted rainfall`
   * :guilabel:`Input layer`:
     |processing|`"joined layer from process "join attributes by field value"`
   * :guilabel:`Field to use for a burn-in value [optional]`:  :file:`A`
   * :guilabel:`Output raster size units`: 
     |selectString|:file:`Georeferenced units`
   * :guilabel:`width/Horizontal resolution`/
     :guilabel:`Height/Verticalresolution`: :file:`20`
   * :guilabel:`Output extent`: |processingModel|:file:`reference layer`
   * |processingOutput|:guilabel:`Rasterized`: :file:`A`
   
   Your model should now look like this:
   
   .. figure:: img/landuse_model_rasterize_a.png
      :align: center

#. We also want our output to be automatically saved to a non-temporary
   location. Double click the :guilabel:`A` output and set it to a location:

   .. figure:: img/landuse_model_default_output.png
      :align: center

      Setting a default output for intercepted rainfall. :file:`01_input` is a
      folder, not a GeoPackage.

#. Select the |gdal|:guilabel:`Rasterize (vector to raster)` box in the
   processing modeler and copy it by pressing :kbd:`Ctrl+C`. Then paste it using
   :kbd:`Ctrl+V`. In the end we want to have a raster for all the following parameters:

   .. list-table::
      :header-rows: 1

      * - :guilabel:`Field to use for a burn-in value`, |processingOutput|:guilabel:`Rasterized`
        - :guilabel:`Description`
      * - :file:`A`
        - :file:`Intercepted rainfall`
      * - :file:`CC`
        - :file:`Canopy cover`
      * - :file:`PH`
        - :file:`Plant height`
      * - :file:`EHD`
        - :file:`Effective Hydrological depth`
      * - :file:`Cf`
        - :file:`Cover factor`
      * - :file:`GC`
        - :file:`Ground cover`
      * - :file:`Etc`
        - :file:`Evapotranspiration`
   
   Your final model should now look like this:

   .. _fig_rasterize_manual:

   .. figure:: img/landuse_model_rasterize_all.png
      :align: center
      :width: 100%

      Rasterizing all variables manually. 

.. _create_rasterize_script:

|hard| |FA| Making a script for batch rasterizing
-------------------------------------------------

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
     |integer|:file:`Georeferenced units`
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
   :lines: 1,8
   :emphasize-lines: 8,16

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
      

|basic| |FA| Updating :guilabel:`Hadocha_soil`
----------------------------------------------


Now it is time to start working on our soil layer!

#. Create a new 

.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |FA| replace:: Follow Along:
.. |basic| image:: /static/common/basic.png
.. |checkbox| image:: /static/common/checkbox.png
   :width: 1.3em
.. |fileSave| image:: /static/common/mActionFileSave.png
   :width: 1.5em
.. |gdal| image:: /static/common/gdal.png
   :width: 1.5em
.. |hard| image:: /static/common/hard.png
.. |integer| image:: /static/common/mIconFieldInteger.png
   :width: 1.5em
.. |logo| image:: /static/common/logo.png
   :width: 1.5em
.. |play| image:: /static/common/mActionPlay.png
   :width: 1.5em
.. |processing| image:: /static/common/processingAlgorithm.png
   :width: 1.5em
.. |processingModel| image:: /static/common/processingModel.png
   :width: 1.5em
.. |processingOutput| image:: /static/common/mIconModelOutput.png
   :width: 1.5em
.. |pythonFile| image:: /static/common/mIconPythonFile.png
   :width: 1.5em
.. |saveAsPython| image:: /static/common/mActionSaveAsPython.png
   :width: 1.5em
.. |selectString| image:: /static/common/selectstring.png
   :width: 2.5em
.. |signPlus| image:: /static/common/symbologyAdd.png
   :width: 1.5em
.. |unchecked| image:: /static/common/checkbox_unchecked.png
   :width: 1.3em
