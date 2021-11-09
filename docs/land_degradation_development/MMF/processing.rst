====================================
Processing the data in the MMF model
====================================

Now it is time to start processing our data. We will describe fully how to
implement the first set of equations. We will be making quite some small models
that can later all be combined into one big model. This will help in debugging.

.. figure:: img/MMF_flowchart.png
   :align: center

Estimating effective rainfall (:math:`P_e`)
-------------------------------------------

The rainfall kinetic energy (:math:`KE [\frac{J}{m^2}]`) is a function of
effective rainfall (:math:`P_e` ), i.e. the fraction of mean annual rainfall
(:math:`P`) that is not intercepted by vegetation (:math:`A`). Thus:

.. math::
   :label: eq_p_effective

   P_e = P(1-A)

#. Create a new model
#. Give it two *Raster Layer* inputs: :file:`P` and :file:`A` 
#. Drag in a |gdal|:ref:`gdalrastercalculator` or a
   |logo|:ref:`qgisrastercalculator`.

   :|gdal| GDAL: Fill in the following:
                 
                 * :guilabel:`Input layer A`: |processingModel|:file:`A` 
                 * :guilabel:`Number of raster band for A`: |integer|:file:`1` 
                 * :guilabel:`Input layer B`: |processingModel|:file:`B` 
                 * :guilabel:`Number of raster band for B`: |integer|:file:`1` 
                 * :guilabel:`Expression`: |integer|:file:`B*(1-A)`
                 * |processingOutput| :guilabel:`Calculated:` : :file:`Pe` 

   :|logo| Native: Fill in like so:

                   * :guilabel:`Expression`: :file:`"P@1"*(1-"A@1")`
                   * :guilabel:`Reference Layer(s)`: |processingModel|:file:`A`
                     or :file:`P`
                   * |processingOutput| :guilabel:`Output`: :file:`Pe` 

   Notice the difference in :guilabel:`Expression` between the two. Because we
   are directly using inputs, the expression in |logo| is still relatively
   compact. However, if you start stacking algorithms on top of each other, they
   may quickly become quite long

#. Optionally, set a default location for the output raster
#. Name the model :file:`01_effective_rainfall` and save it under a name

Leaf Drainage and Direct Throughfall
------------------------------------

#. Create a new model named :file:`02_leaf_drainage` 
#. Drag in the necessary raster layer inputs for the following equations:

   .. math:: LD = P_e \cdot CC\\
      DT = P_e - LD
   
   .. admonition:: Solution
      :class: dropdown

      .. figure:: img/model_02_leaf_drainage.png

.. _kinetic_energy:

Kinetic energy
--------------

#. Create a new model named :file:`03_kinetic_energy` 
#. Drag in the inputs for the followinw equations:

   .. math:: 
      KE_{DT} = DT\cdot(11.9+8.7\log(P_i))\\
      KE_{LD} = LD\cdot(18.80\cdot\sqrt{PH}-5.88)\\
      KE = KE_{DT}+KE_{LD}
   
   Where :math:`P_i=11\frac{mm}{h}` is the rainfall intensity and :math:`PH` is the
   plant height.

   .. note::
      In the |gdal|:ref:`gdalrastercalculator`, you can use any Numpy
      functions, such as `log10 <https://numpy.org/doc/stable/reference/generated/numpy.log10.html#numpy.log10>`_. 
      or sqrt. Additionally, powers are written as: ``2**3=8``.
   
   .. admonition:: Checkpoint

      Check that :math:`KE_{DT}\in[0,31254]` and :math:`KE_{LD}\in[816,17846]`.
      (For a rainfall of 1744)
   
   .. admonition:: Hint
      :class: dropdown

      You can rename your algorithms, so that you can actually distinguish them!
      Otherwise, they will all be called 
      :guilabel:`"Calculated" from algorithm "Raster Calculator"`:

      .. figure:: img/model_03_kinetic_energy.png
         :align: center   


Surface Runoff
--------------

Now, this will be a bit more complicated. We will be using a |saga| SAGA
algorithm called :guilabel:`Catchment Area (Flow Tracing)`. This is only
available in version 7.3.0 (not in 7.8.2).

The Soil moisture storage capacity :math:`S_c` is calculated by

.. math:: S_c = 10000 \cdot W_{fc}\cdot \rho_{bd}\cdot EHD\sqrt{\frac{ET_{c,adj}}{ET_c}}

Where :math:`W_{fc}` is soil moisture, :math:`\rho_{bd}` is Bulk density,
:math:`EHD` is effective hydrological depth and :math:`\frac{ET_{c,adj}}{ET_c}`
is the ratio of evapotranspiration.

The resulting estimate for surface runoff is then:

.. math:: 
   SR = P\cdot \exp\left(-\frac{S_c}{P_0}\right)\\
   P_0 = \frac{P}{n}

where :math:`P_0` is the mean rain per day: Annual rainfall :math:`P` and number
of rainy days :math:`n=160`.

#. Create a model implementing the above equations
#. Load the map for :math:`SR`. It should look like this:

   .. figure:: img/model_04_SR_map.png
      :align: center

      The values should be :math:`SR\in[0,57]` 

   Next, we need to route the flow. That is: for each pixel we know the runoff,
   and we want to calculate how it flows over the catchment. For this we will
   use the |saga| :guilabel:`Catchment Area (flow tracing)` algorithm. However,
   our DEM contains some flat areas and depressions from which the algorithm
   does not know where to direct the flow. For this, we will use the 
   |saga|:guilabel:`Fill Sinks` algorithm.

   .. warning::
      |saga| SAGA is **very** specific when it comes to misaligned rasters. It
      can be that your rasters misalign by :math:`10^{-6}` and it will give a
      :file:`The Following layers were not correctly generated` error. If this
      is the case, double-check and triple-check if your rasters are aligned
      under :menuselection:`Layer Properties --> Information` **Extent**

#. In your model, drag in a |saga|:guilabel:`Fill sinks` and set it to
   |processingModel| :file:`DEM` (Create a new input). The minimum slope is good
   on default settings.
#. Drag in a |saga|:guilabel:`Catchment area (flow tracing)` and fill it in like
   this:

   * :guilabel:`Elevation`: 
     |processing|:file:`"Filled DEM" from algorithm "Fill sinks"`
   * :guilabel:`Flow Accumulation units`: |integer|:file:`[0] number of cells`
   * :guilabel:`Weights`: |processingModel|:file:`"Calculated from algorithm "SR"`
   * :guilabel:`Method`: |integer|:file:`[2] DEMON` This is the flow routing
     algorithm. It is more advanced than Dinf that ArcGIS uses, but still
     relatively convergent, as opposed to the kinematic routig algorithm.
     `Reference <http://www.saga-gis.org/saga_tool_doc/2.2.5/ta_hydrology_2.html>`_
   * |processingOutput|:guilabel:`Flow Accumulation`: :file:`SR_acc` 

#. Run the model. If everything works correctly, you should get the following output:

   .. figure:: img/model_04_acc_map.png
      :align: center

      Your values should be :math:`\in[0,800000]` 

   Now, we are not interested in how much flow accumulates in the river areas.
   We will say that for any cell with :math:`SR>1400` this is a river area and
   set :math:`SR_{final}=0` there.

#. Drag in a Raster calculator. The expression you should fill in is:
   :file:`IF("SR"<1400,"SR",0)`. Depending on which raster calculator,
   :file:`"SR"` is either :file:`A` or :file:`"'SR' from algorithm 'SR'@1"`. The
   resulting output should look like this:

   .. figure:: img/model_04_SR_final_map.png
      :align: center
   
   .. tip::
      If you find yourself filling in inputs all the time, you can create a new
      model, drag in the |processingModel|:guilabel:`04_surface_runoff`
      algorithm, and selecting the inputs as paths to the rasters.

Estimate soil detachment by raindrops :math:`F [\frac{kg}{m^2}]`  and runoff :math:`H []\frac{kg}{m^2}]` 
--------------------------------------------------------------------------------------------------------

Soil particle detachment by runoff :math:`H` is given by:

.. math:: H=10^{-3}\frac{SR^{1.5}}{2COH}\sin(S)(1-GC)

Where :math:`COH [kPa]` is cohesion, :math:`SR [mm]` (use :guilabel:`SR_final` )
volume of surface runoff, :math:`S [\rad]` is slope and :math:`GC [-]` is
fraction of ground cover.

#. Create a new model named :file:`05_detachment`
#. Drag in a :guilabel:`DEM` input and a |gdal| or |logo| slope algorithm.
#. To convert the slope to radians, drag in a |gdal|:ref:`gdalrastercalculator`
   and use the :file:`deg2rad(A)` on |processing|:file:`"Slope" from algorithm "Slope"`
#. Next, drag in a |logo|:ref:`qgisrastercalculator` and fill in the equation.
   (|gdal| does not like )

.. admonition:: Solution
   :class: dropdown

   If you have filled in :guilabel:`A` : |processingModel|:file:`SR`,
   :guilabel:`B` : |processingModel|:file:`COH`, :guilabel:`C` :
   |processing|:file:`"Slope" from algorithm "Slope"`, :guilabel:`D` :
   |processingModel|:file:`GC`, then the final expression is:

   :file:`0.0005*A**1.5/B*sin(deg2rad(C))*(1-D)` 

   In my case, |gdal| did not like raising to a power, and the |logo| raster
   calculator did not work, because :guilabel:`SR` was in a slightly different
   coordinate system. As a result, I calculated it like this:

   .. figure:: img/model_05_h.png
      :align: center

      :guilabel:`SR15` calculates :math:`SR^{1.5}` 

   The final value should be :math:`H\in[0,1.2]`

Soil particle detachment by raindrops, :math:`F` is given by:

.. math:: F=10^{-3}K\cdot KE

where :math:`K [\frac{g}{J}]` is the soil detachability index and :math:`KE [J]`
is kinetic energy determined in :ref:`kinetic_energy`.

#. Add this calculation to the model

Calculating transport capacity and final erosion
------------------------------------------------

Since we will also be using the slope in this model, we will be making the rest
of our calculations in the same model.

The transpor capacity is given by:

.. math:: TC = 10^{-3}C_fSR^2\sin(S)

Again, I used a |logo|:ref:`qgisrastercalculator` to calculate :math:`SR^2`, and
filled this in into the model.

Next, the final erosion is given by:

.. math:: E = \min(F+H, TC)

Use the :file:`minimum()` to calculate this in |gdal|:ref:`gdalrastercalculator`.

.. admonition:: Solution
   :class: dropdown

   The final model looked like this for me:

   .. figure:: img/model_05_final.png
      :align: center

      All processes with custom names are raster calculators. :guilabel:`S2`
      calculates` and :math:`S^2`.
   
   And the final erosion map looked like this:

   .. figure:: img/E.png
      :align: center

      Values are between :math:`0,14.9` 
      

Putting everything into a single model
--------------------------------------

Now, you can create a new model and drag all the algorithms into it! Make sure
to **only** set inputs as paths to files where they are acutally inputs from
pre-processing. Otherwise use an |processing|:guilabel:`Algorithm output` from a
previous algorithm. It should look like this:

.. figure:: img/model_all.png

.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |gdal| image:: /static/common/gdal.png
   :width: 1.5em
.. |integer| image:: /static/common/mIconFieldInteger.png
   :width: 1.5em
.. |logo| image:: /static/common/logo.png
   :width: 1.5em
.. |processing| image:: /static/common/processingAlgorithm.png
   :width: 1.5em
.. |processingModel| image:: /static/common/processingModel.png
   :width: 1.5em
.. |processingOutput| image:: /static/common/mIconModelOutput.png
   :width: 1.5em
.. |saga| image:: /static/common/providerSaga.png
   :width: 1.5em
