.. _annular_mask_script:

|hard| |FA| Creating a script for the mask file
===============================================

Now, to get the |grassLogo|:guilabel:`r.neighbors` algorithm to work correctly, we
need to create a mask file script.

.. warning::
   This is a |hard| exercise. Only do this if you have extra time left.
   Otherwise, go directly to the :ref:`solution <mask_script_solution>`. Doing
   this exercise will also help you with :ref:`create_rasterize_script`.

Creating a model
................

#. We will create a model that we will convert to a script. Click
   |processingModel|:menuselection:`--> Create New Model...`
#. Drag in the following inputs:
   
   * |signPlus|:guilabel:`Number`: 

     * :guilabel:`Description`: :file:`Inner radius`
     * :guilabel:`Number type`: |fieldInteger|:file:`Integer` 
     * :guilabel:`Minimum value`: :file:`0` 
     * :guilabel:`Default value`: :file:`1` 

   * |signPlus|:guilabel:`Number`: :file:`Outer radius`, similar to Inner radius

#. Name the model :file:`Annulus mask for r.neighbors`. Optionally, also give it a group name.

#. Click the |saveAsPython| *Export as Script Algorithm* icon. 

   The following script will appear. Places where we will insert some of our own
   code are highlighted.

   .. `literalinclude:: scripts/annulus_r_neighbors.py
      :lines: 1-11,13, 16-21,23-27,39-58
      :emphasize-lines: 11,13, 18, 23
      `:linenos:

Add additional parameters
.........................

In the model, we have only added two inputs. However, our algorithm should also have
an output. At line 11, insert the following:

.. literalinclude:: scripts/annulus_r_neighbors.py
   :lines: 12

and within the :code:`initAlgorithm` function (line 18) insert:

.. literalinclude:: scripts/annulus_r_neighbors.py
   :lines: 22

Convert parameters to workable format
.....................................

There is one problem with these processing parameters, however: they are not actually
values that we can work with. However, we want to be able to use them as numbers or strings (in
the case of file names). For this we will use the :meth:`parameterAsInt() <QgsProcessingAlgorithm.parameterAsInt()>` and
:meth:`parameterAsFileDestination()` At line 23, insert the following.: 

.. literalinclude:: scripts/annulus_r_neighbors.py
   :lines: 29-32

Perform calculations
....................

What we want is a function that creates a file like below for an inner, resp. outer
radius  of: :math:`r_i=1,r_o=3`

.. literalinclude:: scripts/r_1_3

This file is a mask file with weights e.g. numbers between 0 and 1, that tell GRASS
how much this cell matters for the calculation of the tpi.

.. note::

   I did not come up with these calculations myself, but found them on stackexchange.
   Sadly, I forgot where.

Note that the 0 in between
all the 1s is the center is the point that corresponds to the center. It is actually at coordinates
:math:`(x_0,y_0)=(3,3)` (start counting at 0). This is what |grassLogo|:guilabel:`r.neighbors` expects. It follows that
:math:`x_0=y_0=r_o`. Let :math:`d` be the distance to this point. Then, we want all
points to be 1 for which:

.. math:: d\geq r_i \land d \leq r_0

holds and 0 otherwise. The (eucludian) distance can be calculated by:

.. math::
   d := \sqrt{(x-x_0)^2+(y-y_0)^2}\\
      = \sqrt{(x-r_o)^2+(y-r_o)^2}

where :math:`x,y` are the coordinates of the Currently processed point.
To put this in code, we first need to import the corresponding functions:

.. literalinclude:: scripts/annulus_r_neighbors.py
   :lines: 15

and then make the calculations. Here :code:`a ** b` means :math:`a^b`. Also note
that the size of our array is :math:`2r_o+1`

.. literalinclude:: scripts/annulus_r_neighbors.py
   :lines: 34, 35

Then, we save our file to :code:`outloc` in decimal (:code:`"%d"`) format:

.. literalinclude:: scripts/annulus_r_neighbors.py
   :lines: 37

Your final script should look like this:

.. _mask_script_solution:

.. admonition:: |basic| Solution
   :class: dropdown

   If you didn't follow the above |FA|, you can use the below script. 

   #. In the Processig Toolkbox, click the 
      |pythonFile|:menuselection:`--> Create New Script...`
   #. copy-paste the following code into the text editor that popped up:

      .. literalinclude:: scripts/annulus_r_neighbors.py
         :emphasize-lines: 12,15,22,29-37
         :linenos:

   #. |fileSave| Save the script. It should now show up in the toolbox:

      .. figure:: img/script_in_toolbox.png
         :align: center

|basic| Testing the annulus mask
.................................

Now you have made the annulus mask file, either by following the instructions or
skipping to the solution, now it is time to test whether the annulus mask we just made actually works.

#. Search for :file:`annulus mask for r.neighbors` in the processing pane and run it.

   Use default settings, but set :guilabel:`annular mask` to a file name with a :file:`.txt` extension

   .. figure:: img/test_annulus.png
      :align: center

#. If you have any errors, *read the error*, see where it comes from and resolve them.

#. open the file and verify if it is made correctly.


.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |FA| replace:: Follow Along:
.. |basic| image:: /static/common/basic.png
.. |fieldInteger| image:: /static/common/mIconFieldInteger.png
   :width: 1.5em
.. |fileSave| image:: /static/common/mActionFileSave.png
   :width: 1.5em
.. |grassLogo| image:: /static/common/grasslogo.png
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
