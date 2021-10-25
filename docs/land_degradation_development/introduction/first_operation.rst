=========================================
First operations and making a Page Layout
=========================================
In this section, you will perform your first operation on a vector layer: the
Dissolve operation. Furthermore, you will make a Page layout to make a
presentable map out of your layers.

.. tip:: Processing guide
    See the :doc:`Processing Guide </training_manual/processing_guide/index>`
    For a more complete introduction to the processing algorithms inside QGIS.


|basic| |FA| A virtual tour through the Hadocha sub-catchment
-------------------------------------------------------------

Now we have added all our layers to the project in the previous exercise, it is
time to explore them a bit. 

#. Open the attribute table of the :guilabel:`Hadocha_landuse` layer. Either
    by selecting the layer and pressing :kbd:`f6`, the |openTable| button on the top
    toolbar, or right-clicking the layer and pressing |openTable|:guilabel:`Open
    attribute table`.

    .. figure:: img/landuse_attribute_table.png
        :align: center

    An attribute table is a useful way for inspecting the data of your layer. It
    is always the first thing you would look at if you get unexpected output.
    Close the attribute table by pressing :kbd:`Esc`.
#. Another way of inspecting a layer is by using |identify|identify. With
    :guilabel:`Hadocha_landuse` selected, press :kbd:`Ctrl+Shift+I` or
    |identify| in the top toolbar. Click the swamp and the following window should pop up:

    .. figure:: img/identify_swamp.png
        :align: center
    
    As you can see, all values of the attribute table are shown.

#. inspect the other layers :guilabel:`Hadocha_soil` and :guilabel:`Hadocha_dem`.

|basic| |FA| Perform a dissolve operation
-----------------------------------------

As we have seen in the attribute tables, there are multiple features that have
the same landuse and soiltypes. To solve this, we will perform a
:ref:`qgisdissolve` operation.

.. note:
    There are multiple different providers for algorithms. There is the are
    default |qgis|QGIS algorithms, |GDAL|GDAL, |SAGA|SAGA and |GRASS|GRASS.
    These are different GIS applications that come bundled with QGIS. In this
    exercise we will be using the 

.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |FA| replace:: Follow Along:
.. |basic| image:: /static/common/basic.png
.. |identify| image:: /static/common/mActionIdentify.png
   :width: 1.5em
.. |openTable| image:: /static/common/mActionOpenTable.png
   :width: 1.5em
