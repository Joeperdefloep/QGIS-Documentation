================
First operations
================
In this section, you will perform your first operation on a vector layer: the
Dissolve operation. Furthermore, you will make a Page layout to make a
presentable map out of your layers.

.. tip:: See the :doc:`Processing Guide </docs/training_manual/processing/index>`
    for a more complete introduction to the processing algorithms inside QGIS.


|basic| |FA| A virtual tour through the Hadocha sub-catchment
-------------------------------------------------------------

Now we have added all our layers to the project in the previous exercise, it is
time to explore them a bit. 

1. Open the attribute table of the :guilabel:`Hadocha_landuse` layer. Either
    by selecting the layer and pressing :kbd:`f6`, the |openTable| button on the top
    toolbar, or right-clicking the layer and pressing |openTable|:guilabel:`Open
    attribute table`.

    .. figure:: img/landuse_attribute_table.png
        :align: center

    An attribute table is a useful way for inspecting the data of your layer. It
    is always the first thing you would look at if you get unexpected output.
    Close the attribute table by pressing :kbd:`Esc`.
2. Another way of inspecting a layer is by using |identify|identify. With
    :guilabel:`Hadocha_landuse` selected, press :kbd:`Ctrl+Shift+I` or
    |identify| in the top toolbar. Click the swamp and the following window should pop up:

    .. figure:: img/identify_swamp.png
        :align: center
    
    As you can see, all values of the attribute table are shown.

3. inspect the other layers :guilabel:`Hadocha_soil` and :guilabel:`Hadocha_dem`.

|basic| |FA| Perform a dissolve operation
-----------------------------------------

As we have seen in the attribute tables, there are multiple features that have
the same landuse and soiltypes. To solve this, we will perform a
:ref:`qgisdissolve` operation.

.. note:: There are multiple different providers for algorithms. There is the are
    default |logo| QGIS algorithms, |gdal| GDAL, |saga| SAGA and |grass| GRASS.
    These are different GIS applications that come bundled with QGIS. In this
    exercise we will be using the |logo| algorithm. Feel free to try out the
    other algorithms throughout the practical, but remember to not get too distracted!

1. follow :doc:`Set up </docs/training_manual/processing/set_up>` from the
    processing guide to get the toolbox.

2. Search for :file:`Dissolve` in the search bar |inputText| and select the
    |dissolve| algorithm. 

3. Fill it in like this:

    .. figure:: img/dissolve_landuse.png
        :align: center

    Under :guilabel:`Dissolve field(s) [optional]`, select
    |checkbox|:file:`FEATURE`. Your resulting layer should look like this:

    .. figure:: img/landuse_dissolved.png
    

4. Now, to apply the symbology of the undissolved layer, right-click
    :guilabel:`Hadocha_landuse` in the Layers panel. Now, :menuselection:`Style --> Copy
    style --> All style categories`. On the *Dissolved* layer, click
    :menuselection:`Style --> Paste style --> All style categories` to apply the
    styles.

5. Perform the same operation on :guilabel:`Hadocha_soil`.

Saving your layer to a |geopackage| Geopackage
----------------------------------------------

By default, processes will create a temporary layer, which is saved in a
location that will be erased on reboot and very difficult to find after you close
QGIS. Temporary layers are indicated by the |indicatorMemory| icon.

In this exercise, we will save the layer in a GeoPackage. Very technically, this
is a SQLite SpatiaLite database with specifications for storing spatial vector
and raster data. Because it is a database, a GeoPackage can store multiple
*layers* of either vector or raster data. 
ArcGIS does not support rasters for GeoPackages yet, see :ref:`arcgis_raster`.


1. Right-click the layer and click |save|:guilabel:`Make Permanent...`
2. Fill in the dialog as follows:

    ..figure:: img/save_geopackage.png
        :align: center

    Here, we create a new GeoPackage :file:`01_input.gpkg` with the
    :guilabel:`Dissolved` landuse layer. This is the GeoPackage we will later on
    use for all input data of the MMF erosion model.

3. Save the dissolved soil layer in the same GeoPackage.

.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |FA| replace:: Follow Along:
.. |basic| image:: /static/common/basic.png
.. |checkbox| image:: /static/common/checkbox.png
   :width: 1.3em
.. |dissolve| image:: /static/common/dissolve.png
   :width: 1.5em
.. |gdal| image:: /static/common/gdal.png
   :width: 1.5em
.. |grass| image:: /static/common/grasslogo.png
   :width: 1.5em
.. |identify| image:: /static/common/mActionIdentify.png
   :width: 1.5em
.. |inputText| image:: /static/common/inputtext.png
.. |logo| image:: /static/common/logo.png
   :width: 1.5em
.. |openTable| image:: /static/common/mActionOpenTable.png
   :width: 1.5em
.. |saga| image:: /static/common/providerSaga.png
   :width: 1.5em
