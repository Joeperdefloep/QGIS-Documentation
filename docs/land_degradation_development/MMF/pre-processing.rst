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
-----------------------------
Even though GeoPackages are very useful for easy sharing of data, there are some
small quirks when opening rasters from them for models we made ourselves.
Therefore, we will be dumping all our rasters in a folder. 

#. Create a folder :file:`01_input` inside :file:`GIS_files`.

|basic| |FA| Updating :guilabel:`Hadocha_landuse`
------------------------------------

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

Even though 



Updating :guilabel:`Hadocha_soil`
---------------------------------