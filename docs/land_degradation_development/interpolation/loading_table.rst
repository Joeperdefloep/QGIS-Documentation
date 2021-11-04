==========================================================
|basic| Loading a table and converting to a point layer
==========================================================

In this section, we will be handling point data from an Excel table. and
converting it to a point layer. Finally, we will *interpolate* the point layer to
obtain the precipitation in our Hadocha watershed. One interesting aspect is
that the coordinates of the weather stations are in a different Coordinate
Reference System (CRS) than the rest of our data, and we will have to reproject
them.

|FA| Loading and selecting the table data
-----------------------------------------

First, we have to load the data. 

#. In the *Browser* pane, find :menuselection:`GIS_files --> data --> rainfall.xlsx`.
   This is the rainfall file we will be using. Load it into the
   project and |openTable|:guilabel:`Open Attribute Table`. 

   You are looking at processed data from `NCEI
   <https://www.ncei.noaa.gov/maps/monthly/>`_. They provide measured data from
   weather stations on the world. However, not al years had data for all months.
   For each station, the precipitation was summed for all years that had 12
   months of data. Then, the average was taken over these years. As you can see,
   not all stations have data for a sufficient number of years.

#. Why is this a problem? What do you think is an acceptable number of years?

   .. admonition:: Solution and steps
      :class: dropdown

      We think an acceptable amount of years is 5 for this case. Ideally, we
      would want at least 10 years, but given the available data, we found that
      more stations outweighed more years. Now, we will select the stations that
      have :math:`years \geq 5` years of data.

      #. In the processing toolbox, look for |logo|:menuselection:`Vector
         selection --> Extract by attribute`. and fill it in like so:

         .. figure:: img/extract_attribute.png
            :align: center
            :alt: Input layer has Rainfall Sheet 1, Selection attribute is years, operator greater than equal and Value [optional] 5.
      
      #. optionally, make the new layer permanent

|FA| Converting to a point layer and reprojecting
-------------------------------------------------

#. To find out where our points end up, we want to see where we are on the
   earth. For that, we will load the OpenStreetMap *basemap* under
   |xyz|:guilabel:`XYZ Tiles` in the Browser.
#. Find the |processing|:guilabel:`Create point layer from table` algorithm.

   1. Set the :guilabel:`Extracted (attribute)` layer as Input layer
   2. Set |selectString|:guilabel:`X field` to |fieldFloat|:file:`LONGITUDE`
   3. Set |selectString|:guilabel:`Y field` to |fieldFloat|:file:`LATITUDE`
   4. Leave the :guilabel:`Target CRS` on :file:`EPSG:4326 - WGS84`. This is the
      CRS that our table data is in. We do not have an option to reproject now
      and will do that in the next step.

   You should get the following points:

   .. figure:: img/points_table.png
      :align: center
   
   If they are on a different location on the world, check your settings!

#. Find the |processing|:guilabel:`Reproject layer` tool.

   #. select |pointLayer|:file:`Points from table [EPSG:4326]` as
      :guilabel:`Input Layer`
   #. As :guilabel:`Target CRS`, set |selectString|:file:`UTM zone 37N`

      Your new layer :guilabel:`Reprojected` should be exactly on top of the old
      layer.

#. Optionally, make the layer permanent.

.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |FA| replace:: Follow Along:
.. |basic| image:: /static/common/basic.png
.. |fieldFloat| image:: /static/common/mIconFieldFloat.png
   :width: 1.5em
.. |logo| image:: /static/common/logo.png
   :width: 1.5em
.. |openTable| image:: /static/common/mActionOpenTable.png
   :width: 1.5em
.. |pointLayer| image:: /static/common/mIconPointLayer.png
   :width: 1.5em
.. |processing| image:: /static/common/processingAlgorithm.png
   :width: 1.5em
.. |selectString| image:: /static/common/selectstring.png
   :width: 2.5em
.. |xyz| image:: /static/common/mIconXyz.png
   :width: 1.5em
