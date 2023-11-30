==================================
Comparison between QGIS and ArcGIS
==================================

Since the Wageningen University teaches ArcGIS by default, it may be useful to
understand the differences and similarities, such that changing from one to the
other is as smooth as possible. Apart from that both have a different user
interface, they also have made some different design choices that may take some
getting used to.

Data handling
-------------
Where ArcGIS forces you to store all data in a proprietary GeoDataBase after
every operation, QGIS uses temporary files. These are stored with random names
in :file:`/tmp/` on Linux and :file:`AppData\\local\\` in Windows. A benefit of
using temporary files is that your project directory will not get cluttered as
quickly when trying out different GIS operations.

Data sharing - Vector
.....................
Vector data can be easily shared between QGIS and ArcGIS: QGIS can read the data
from a :file:`.gdb` database and ArcGIS can read and write vector data to a
:file:`.gpkg` GeoPackage.

.. _arcgis_raster:

Data sharing - Raster
.....................
Sharing raster data is more involved and requires pre-work from either side.
Currently, the easiest way to share raster data between QGIS and ArcGIS is to
share a (zip-compressed) folder containing the relevant rasters.  
Should you get a :file:`.gdb` database containing rasters that you need to
rescue, you could try
`ArcRasterRescue <https://github.com/r-barnes/ArcRasterRescue>`_. Currently, this
involves building from source and not all datatypes are supported, but you may
be in luck! Otherwise, ask the party you received the files from to get them in
a different format.
Currently, ArcGIS only supports 8-bit color rasters in a GeoPackage. If you have
another raster in a GeoPackage, this will show up as a table. We hope ESRI will
catch up with the open standards soon.

Model building
--------------
When building models, it seems that ArcGIS focuses on quick modeling on the same
dataset and easy sharing of that dataset with the corresponding modeling tools. 
QGIS on the other hand, makes it really easy to share models, but those are not
necessarily linked to project files.  
When selecting inputs in ArcGIS, they are selected relative to the *Default
Folder*. QGIS, however, uses absolute paths. If you move a project that has some
modeling workflows that directly link to files, they will be broken.