====================
Getting to know QGIS
====================

|basic| Getting the files
-------------------------

.. todo: See if we can get this from the Git repository - need to allow sharing
   from WU(R)


Get the files from brightspace, and unzip to a location of your choice. All
relevant files are stored in a GeoPackage and additional tabular data is stored
in an :file:`.xlsx` file. Files like these are very useful for easy data
management in Libreoffice Calc or MS Excel. Furthermore, they are also editable
in QGIS or Python.


|basic| Introduction to the interface
-------------------------------------

For an introduction to the interface, follow :ref:`interface_overview`. 
Then, try adding your own maps to the interface. These are
:file:`Hadocha_dem`, :file:`Hadocha_landuse` and :file:`Hadocha_soil`.

|basic| Changing layer Symbology
--------------------------------
.. note:
   this section has been largely copied from the training manual.

The symbology of a layer is its visual appearance on the map.
The basic strength of GIS over other ways of representing data with spatial
aspects is that with GIS, you have a dynamic visual representation of the data
you're working with.

Therefore, the visual appearance of the map (which depends on the symbology of
the individual layers) is very important. The end user of the maps you produce
will need to be able to easily see what the map represents. Equally as
important, you need to be able to explore the data as you're working with it,
and good symbology helps a lot.

In other words, having proper symbology is not a luxury or just nice to have.
In fact, it's essential for you to use a GIS properly and produce maps and
information that people will be able to use.

|basic| |FA| Legend with unique values
-------------------------------------------------------------------------------

To change a layer's symbology, open its :guilabel:`Layer Properties`. Let's
begin by changing the color of the :guilabel:`Hadocha_landuse` layer.

#. Right-click on the :guilabel:`Hadocha_landuse` layer in the layers list.
#. Select the menu item :guilabel:`Properties...` in the menu that appears.

   .. note:: By default, you can also access a layer's properties by
     double-clicking on the layer in the Layers list.

   .. tip:: The |symbology| button at the top of the :guilabel:`Layers`
     panel will open the :guilabel:`Layer Styling` panel. You can use this
     panel to change some properties of the layer: by default, changes will be
     applied immediately!

1. In the :guilabel:`Layer Properties` window, select the |symbology|
   :guilabel:`Symbology` tab:

   .. figure:: img/layer_properties_style.png
      :align: center

2. In the top drop-down menu, select |categorizedSymbol|:guilabel:`Categorized`.
3. In the :guilabel:`Value` drop-down, select |text|:File:`FEATURE`.
4. Click :guilabel:`Classify` to load all values into the list.
5. In the :guilabel:`Symbol` drop-down menu, you can select a colour for each
   attribute |selectColor|.
6. Click :guilabel:`OK` again in the :guilabel:`Layer Properties` window, and
   you will see the color change being applied to the layer.

.. tip::
   In the :menuselection:`Style --> Save as Default` you can save your symbology
   to the layer, so it will be loaded like this into another QGIS project.

|basic| |TY|
-------------------------------------------------------------------------------

Change the colours of the :guilabel:`Hadocha_soil` layer to matching shades of
brown for the different soiltypes. Try using the :guilabel:`Layer Styling` panel
this time.

.. admonition:: Solution
   :class: dropdown

   Your layer should look somethig like this:

   .. figure:: img/soil_symbology.png
      :align: center


.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |FA| replace:: Follow Along:
.. |TY| replace:: Try Yourself
.. |basic| image:: /static/common/basic.png
.. |categorizedSymbol| image:: /static/common/rendererCategorizedSymbol.png
   :width: 1.5em
.. |selectColor| image:: /static/common/selectcolor.png
.. |symbology| image:: /static/common/symbology.png
   :width: 2em
.. |text| image:: /static/common/text.png
   :width: 1.5em
