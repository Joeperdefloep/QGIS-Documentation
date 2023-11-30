===============
Installing QGIS
===============

There are different ways to install QGIS, depending on whether you need any
external processing toolboxes tuch as SAGA, GDAL or GRASS. We need SAGA and it
is nice to be able to have a look at GRASS plugins, so we will use the OSGeo4W
installation method for |win|. For other systems, such as |osx| OSX or |nix| , install
normally as outlined on the `QGIS downloads page <https://qgis.org/en/site/forusers/download.html>`

#. Go to the `QGIS download page <https://www.qgis.org/en/site/forusers/download.html>`_
   and click the `OSGeo4W Network installer <https://download.osgeo.org/osgeo4w/v2/osgeo4w-setup.exe>`_.
#. Run the installer as administrator

   .. figure:: img/osgeo4w_install.png
      :align: center
      :alt: To run as administrator, press the windows key, search for osgeo4w-setup.exe, click the arrow and press run as administrator


#. Select :guilabel:`Express install`
#. now select

   #. |unchecked| :guilabel:`QGIS`
   #. |checkbox| :guilabel:`QGIS LTR`
   #. |checkbox| :guilabel:`GDAL`
   #. |checkbox| :guilabel:`GRASS GIS`

#. finish the installation normally. This should install QGIS 3.22.

Installing QRichDem
-------------------

QRichDem is a plugin that makes `RichDEM <https://richdem.com>`_ available to QGIS. I
wrote it myself and will be testing it this class. Especially |osx| OSX has not been
tested yet. It will install the package using pip, which may not be available if you
first installed QGIS. If you encounter any errors, see `Manually installing pip`_

#. open up QGIS
#. Install the QRichDem plugin following the :ref:`installation instructions <plugin_installation>`

   It will take some time to install RichDEM, so do not close QGIS while installing.
#. If everything worked out, you should have the RichDEM toolbox 

   .. figure:: img/richdem_toolbox.png
      :align: center
      :alt: Richdem toolbox with depression breaching, filling, flow accumulation and terrain attributes algorithms.

Manually installing pip
-----------------------

`pip <https://pip.pypa.io/en/stable/>`_ is a tool that installs Python packages. RichDEM is a python package that is not
included in QGIS, so in order to install RichDEM, we need pip. However, 

|nix| |osx|
...........

Make sure you have not activated any environment. If you do not know what virtual
environments or conda means, that probably means you do not have them installed. QGIS
installs all its requirements in the system environment, so that is also where we want
pip installed.

in a terminal, type:

.. code-block:: sh

   python3 -m ensurepip --upgrade
   python3 -m pip install richdem

This also install richdem itself.

|win|
.....

#. Open the osgeo4w setup, again, as administrator. This time choose |radioButtonOn|
   :guilabel:`advanced install`. Follow the instructions until the Select Packages
   screen. There, search for "pip", click the + icon and click the turning arrows symbol
   to select the highest available version.

   .. figure:: img/install_pip.png
      :align: center
      :alt: the Select Packages screen, with "pip" highlighted in the search bar, as well as the turning arrows symbol

#. continue the rest of the installation and continue `Installing QRichDem`_

#. If it still does not work, open the OsGEO4W shell and type in there:

   .. code-block:: sh

      python3 -m pip install richdem

.. Substitutions definitions - AVOID EDITING PAST THIS LINE
   This will be automatically updated by the find_set_subst.py script.
   If you need to create a new substitution manually,
   please add it also to the substitutions.txt file in the
   source folder.

.. |checkbox| image:: /static/common/checkbox.png
   :width: 1.3em
.. |nix| image:: /static/common/nix.png
   :width: 1em
.. |osx| image:: /static/common/osx.png
   :width: 1em
.. |radioButtonOn| image:: /static/common/radiobuttonon.png
   :width: 1.5em
.. |unchecked| image:: /static/common/unchecked.png
   :width: 1.3em
.. |win| image:: /static/common/win.png
   :width: 1em
