===================================
|moderate| Interpolating point data
===================================

Next, we will be interpolating our data. There are many different algorithms for
doing this, from simple algorithms that take the value of the closest point
(Nearest Neighbour), to complex spline  or 
`Kriging <https://en.wikipedia.org/wiki/Kriging>`  interpolation techniques. We will be
exploring the nearest neighbour, Inverse Distance Weighting and several splines
in this chapter. Finally, we will obtain our rainfall value from the |saga|:guilabel:`Thin
Plate Spline` algorithm. It is recommended to first read 
:doc:`/docs/gentle_gis_introduction/spatial_analysis_interpolation`.

Nearest Neighbour
-----------------

#. Find and open the |gdal|:guilabel:`Grid (Nearest Neighbour)` algorithm. 
#. Set :guilabel:`Point Layer` to |pointLayer|:file:`Reprojected [EPSG:32637]`
#. Set :menuselection:`Advanced Parameters --> Z value from field [optional]`
   to |fieldFloat|:file:`PRCP`.
#. Run the algorithm. The output map should look like this:

   .. figure:: img/nearest_neighbour.png
      :align: center
       
      Nearest neighbour interpolated precipitation

   .. admonition:: |hard| Challenge

      It seems to be possible to 
      `Set cellsize <https://gis.stackexchange.com/questions/394134/cell-size-in-grid-nearest-neighbour-in-qgis>`_
      and extent in a similar way, so that your grid is automatically clipped
      to :guilabel:`Hadocha_dem`.

Inverse Distance Weighting
--------------------------

Inverse distance weighting is an interpolation method in which the influence of a
datapoint on the value of the interpolated raster decreases with distance.

1. Find and open the |logo|:guilabel:`IDW interpolation` tool
2. Set :guilabel:`Vector layer` to |pointLayer|:file:`Reprojected`
3. As :guilabel:`Interpolation attribute` select |fieldFloat|:file:`PRCP`
4. Press the |signPlus| button to add the layer to the selection.
5. For :guilabel:`Extent`, select :menuselection:`... --> Calculate from layer --> Reprojected`.
6. As :guilabel:`Pixel size X` and :guilabel:`Pixel size Y` enter :file:`1970`.
   The :guilabel:`Rows` and :guilabel:`Columns` fields should adjust.
7. :guilabel:`Run` the algorithm. Your map should look like this:

   .. figure:: img/idw.png
      :align: center
        
      IDW interpolated precipitation.

8. |hard| try to get similar results with algorithms from |gdal| GDAL and
   |grassLogo| GRASS

Spline interpolation
--------------------

A spline is a piecewise defined polynomial. There are many different ways to
generate a spline from a set of datapoints. We will be using a thin plate
spline which creates a minimum curvature surface through all datapoints.

1. find and open the |saga|:guilabel:`Thin plate spline` tool
   You may encounter the following warning that you can safely ignore:

.. warning::
   SAGA version <version> is not officially supported - algorithms may encounter issues

2. For :guilabel:`Points` select |pointLayer|:file:`Reprojected [EPSG:32637]`.
3. Set :guilabel:`Attribute` to |fieldFloat|:file:`PRCP`
#. Set :guilabel:`search range` to |selectString|:file:`[1] global`
#. Set :guilabel:`Number of Points` to |selectString|:file:`[1] All points within search distance`
#. Set :guilabel:`Search direction` to |selectString|:file:`[0] all directions`
5. for :guilabel:`Cellsize` enter :file:`1970`
#. And finally, set :guilabel:`Fit` to |selectString|:file:`[1] cells`
6. :guilabel:`Run` the algorithm. Your output should look like this:
    
   .. figure:: img/thin_plate_spline.png
      :align: center

      Thin plate spline interpolation

   notice that the raster value extremes exceed the values of the datapoints. This
   is a characteristic of (thin plate) spline interpolation.

|basic| Final interpolation
---------------------------

Now we have looked at different algorithms and compared their characteristics,
it is time to select one and obtain a precipitation raster. Normally, to choose
an interpolation method, you would randomly sample points, perform an
interpolation on them and compare the error between interpolated and data
values. Due to the amount of datapoints, this is not possible, and we choose
thin plate spline by means of expert opinion.

#. Open the |logo|:guilabel:`Zonal statistics` tool.
#. For :guilabel:`Input layer` select :menuselection:`... --> Browse for Layer`
   and select :file:`Hadocha_mask`:

   .. figure:: img/browse_mask.png
      :align: center

   .. note::
      Note that the filepath becomes:
      :file:`path/00_raw_input.gpkg|layername=Hadocha_mask` The last part
      after :file:`|` tells the algorithm which layer to select from the
      GeoPackage. This may be useful if you want to manually enter a path to a
      GeoPackage layer!

#. As :guilabel:`Raster layer` select |raster|:file:`Target Grid [EPSG:32637]`
#. We only want the |checkbox| Mean to be calculated. :guilabel:`Run` the
   algorithm. This creates a vector layer with the average precipitation value for
   our catchment.
#. Open the attribute table and copy the precipitation value to your clipboard
#. If not loaded yet, load the DEM into the map
#. Run the |logo|:guilabel:`Raster calculator` tool with:
    
   * :guilabel:`Expression`: <your precipitation value>,
   * :guilabel:`Reference layer(s) used for automated extent, cellsize and CRS`: |checkbox|
        <DEM file>

#. To save the raster layer in our :file:`01_input.gpkg` database, right-click
   :menuselection:`Export --> Save as...` with:

   * :guilabel:`Format`: |selectString|:file:`GeoPackage`
   * :guilabel:`File name` :file:`<path_to>/01_input.gpkg`
   * :guilabel:`Layer name` :file:`P`
   * the rest default

.. admonition:: Solution
   :class: dropdown

   The rainfall value is 1744

.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |basic| image:: /static/common/basic.png
.. |checkbox| image:: /static/common/checkbox.png
   :width: 1.3em
.. |fieldFloat| image:: /static/common/mIconFieldFloat.png
   :width: 1.5em
.. |gdal| image:: /static/common/gdal.png
   :width: 1.5em
.. |grassLogo| image:: /static/common/grasslogo.png
   :width: 1.5em
.. |hard| image:: /static/common/hard.png
.. |logo| image:: /static/common/logo.png
   :width: 1.5em
.. |moderate| image:: /static/common/moderate.png
.. |pointLayer| image:: /static/common/mIconPointLayer.png
   :width: 1.5em
.. |raster| image:: /static/common/mIconRaster.png
   :width: 1.5em
.. |saga| image:: /static/common/providerSaga.png
   :width: 1.5em
.. |selectString| image:: /static/common/selectstring.png
   :width: 2.5em
.. |signPlus| image:: /static/common/symbologyAdd.png
   :width: 1.5em
