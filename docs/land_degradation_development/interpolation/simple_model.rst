=======================
Creating a simple model
=======================

In this exercise we will be creating a simple model with
:doc:`/docs/user_manual/processing/modeler`. In this exercise you will work with
Model Builder yourself. This is an important tool since you will use it often in
Chapter 3 of this practical. Here you will automate a series of operations so
that they can be executed with just one click. It will also allow you to make
changes to parameter settings and then quickly re-run the model. This allows you
to compare changes in your model output and link them to the changes that you
made earlier. In this exercise, you will create a model that determines the
Topographic Position Index (TPI) of a DEM. The TPI is given by the equation:

.. math:: TPI=DEM-\mathrm{focalmean}\left(DEM,annulus,1,orad\right)

The TPI can be used to determine whether a location is on a ridge or valley.
This can be useful when you are creating your own adaptation strategies! 

As you can see in :numref:`fig_tpi`, the TPI can differ, based on the radius.
This is useful so you can distinguish between large and small features.

.. _fig_tpi:

.. figure:: https://landscapearchaeology.org/figures/TPI_diagram.png
   :align: center

   Topographic index depends on Neighborhood size. (https://landscapearchaeology.org/2019/tpi/)

Implementing the algorithm
--------------------------

#. In the Processing toolbox, select 
   |processingModel|:menuselection:`--> Create new Model`

   .. figure:: img/create_model.png
      :align: center

   The following window will show:

   .. figure:: /docs/user_manual/processing/img/modeler_canvas.png
      :align: center

   Our TPI model needs two inputs: 
   
   * A Digital Elevation Model (DEM) raster
   * The radius for the zonal statistics.

#. In the *Inputs* pane, scroll down until you see
   |signPlus|:guilabel:`Raster Layer`. drag it into the model view. The
   following dialog will show:

   .. figure:: img/raster_input_dialog.png
      :align: center
   
   Enter :file:`DEM` as name and press :guilabel:`OK`.

   .. note::
      The checkboxes define how the inputs are shown when you open a model:

      * Your created model will not run without |checkbox|:guilabel:`Mandatory`
        inputs
      * |unchecked|:guilabel:`advanced` inputs will be under a drop-down menu

#. Drag a |signPlus|:guilabel:`Number` into  the modeler. Give it a:

   * :guilabel:`Description`: :file:`Outer radius`
   * :guilabel:`Number type`: :file:`Integer`
   * :guilabel:`Munimum value`: :file:`2`
   * :guilabel:`Default value`: :file:`3`

   Your modeler should now look like this:

   .. _fig_model_inputs:

   .. figure:: img/model_inputs.png
      :align: center

      Model with only inputs
   
   .. tip:: Snapping
      You can enable snapping by :menuselection:`View --> Enable snapping`

#. Now, we are going to include our first algorithm. 

   #. Click :guilabel:`Algorithms` (highlighted in :numref:`fig_model_inputs`).
   #. Search for |saga|:guilabel:`Focal Statistics`, drag it into the view and
      fill in the pop-up window as follows:

      * Under :guilabel:`Grid`, press the |integer| drop-down and select
        |processingModel|:guilabel:`Model Input`. It should be on :File:`DEM`
        already since this is the only raster type model input.
      * :guilabel:`Include Center Cell`: |integer|:file:`No`
      * :guilabel:`Kernel Type`: |integer|:file:`[1] Circle`
      * :guilabel:`Radius`: |processingModel|:file:`Outer radius`
      * the rest on default settings
   
   #. Press :guilabel:`OK`

      Your model should now look like this (with some rearranging):

      .. figure:: img/model_focal_statistics.png
         :align: center

#. Drag the |logo|:guilabel:`Raster calculator` into the view. Fill in the
   dialog as follows:

   * :guilabel:`Expression`: 
     :file:`"DEM@1"-"'Mean Value' from algorithm 'Focal Statistics'@1"`. Get the
     names by double-clicking them in the :guilabel:`Layers` list.
   * :guilabel:`Reference Layers (...)`:
     :menuselection:`... -->`|checkbox|:guilabel:`DEM`.
   * |processingOutput|:guilabel:`Output`: :file:`TPI`

   and press :guilabel:`OK`.

   .. note::
      In :file:`DEM@1`, the :file:`@1` refers to *Band 1*. Thus, the raster
      calculator supports operations on rasters with multiple bands.
   
   Press :guilabel:`OK` to add it to the model. It should now look like this:

   .. figure:: img/model_full.png
      :align: center

#. Before we can save our model, we have to give it a name. Below
   :guilabel:`Model Properties`, give it the :guilabel:`Name` 
   :file:`Topographic Position Index (TPI)`
#. Save your model by pressing the |fileSave| icon or :kbd:`Ctrl+S`. Give it a
   descriptive name.

Running the model
-----------------

.. note::
   Currently (Oct 2021), layers from a GeoPackage cannot be selected as raster
   inputs in the Graphical Modeler. See the related 
   `Feature request <https://github.com/qgis/QGIS/issues/38607>`_ and a 
   `Possible workaround <https://gis.stackexchange.com/questions/329294/adding-a-geopackage-layer-as-a-hardwired-input-to-an-algorithm-in-the-qgis-graph>`_
   .
   However, we will be working around this by loading our data into the project first.

#. Load the :guilabel:`Hadocha_dem` layer into your map if it isn't there yet.
#. Now we have created the model, it is time to run it! There are two ways to do
   so:

   #. From within the Graphical Modeler:
      
      Press the |play| button or :kbd:`F5`.

   #. From the Processing Toolbox:

      Notice that there is a new drop-down menu labeled
      |processingModel|:guilabel:`Models`. There, your model named 
      |processingModel|:guilabel:`Topographic Position Index` is shown. Run it
      like any other tool!

#. Either way, now select :file:`Hadocha_DEM` as :guilabel:`DEM`. and 
   :guilabel:`outer radius` :file:`3`. :guilabel:`Run` the model and your output
   should look like this:
   
   .. figure:: img/TPI.png

|IC| Wrapping up
----------------

Now, you have learned how to use the graphical modeler and to calculate the
Topographic Position Index. Both are very useful. We will excessively use the
Graphical Modeler later for the MMF erosion model, and you could use the TPI for
determining where to apply specific measures.

.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.


.. |checkbox| image:: /static/common/checkbox.png
   :width: 1.3em
.. |fileSave| image:: /static/common/mActionFileSave.png
   :width: 1.5em
.. |integer| image:: /static/common/mIconFieldInteger.png
   :width: 1.5em
.. |logo| image:: /static/common/logo.png
   :width: 1.5em
.. |play| image:: /static/common/mActionPlay.png
   :width: 1.5em
.. |processingModel| image:: /static/common/processingModel.png
   :width: 1.5em
.. |processingOutput| image:: /static/common/mIconModelOutput.png
   :width: 1.5em
.. |saga| image:: /static/common/providerSaga.png
   :width: 1.5em
.. |signPlus| image:: /static/common/symbologyAdd.png
   :width: 1.5em
.. |unchecked| image:: /static/common/checkbox_unchecked.png
   :width: 1.3em
