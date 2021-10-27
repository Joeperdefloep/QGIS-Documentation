=============================================================
Geo-Information Science and Sustainable Land Management (SLM)
=============================================================

Please read :doc:`/docs/gentle_gis_introduction/introducing_gis`. For an
introduction to GIS and what the field entails. Next, read the basics of
:doc:`/docs/gentle_gis_introduction/coordinate_reference_systems`. The
further you read, the more detailed information you get, and this is very good
for your understanding (|moderate|). We will also be using a UTM projection ourselves in the
practical. However, don't get too lost on this!

Functionality of GIS
--------------------

.. note::
    This section was adapted from the manual.

GIS systems are equipped with a large set of standard functions for the analysis
of spatial data (e.g. for combining maps or buffering). However, users often
require very specific analysis. It is impossible for general-purpose
GIS producers to provide all the functionalities for all users. Simple
programming languages may solve part of the problem. In this practical we will
work with different ways of adding functionality. 

Although GIS packages may not be equipped with the standard functions required
by users, in some cases we can combine several standard functions to create new
functionality. This procedure works for example when implementing simple
parametric models. In this course we will use the raster calculator in combination
with some other GIS functions to implement the Morgan, Morgan & Finney (MMF)
model. 

Most GIS software is extensible by a programming language such as R or
:doc:`Python </docs/pyqgis_developer_cookbook/index>`,
in which the user can implement new functionality. The programming languages are
typically for the advanced user and are also often used to develop user
interfaces. The Graphical User interface in QGIS provides a
:doc:`/docs/user_manual/processing/modeler` 
framework for designing and implementing geoprocessing models that can include
tools, scripts, and data. Models are data flow diagrams that link together a
series of tools and data to create advanced procedures and work flows. In this
course, you will learn to use Graphical modeler to apply the MMF model. 

Data quality and error propagation
----------------------------------

.. note::
    this section was adapted from the manual

Dealing with data in general or with spatial data specifically, we also have to
deal with data quality and errors. Spatial data will always contain errors. The
main question is whether the errors are acceptable. The latter depends on the
use we will give our data. Dealing with complex forms of analysis we therefore
have to study the effect of errors in our input data on the results of a
particular analysis.

Although people tend to treat error as an embarrassing issue, it is very useful
to make errors explicit. In ideal cases we do not represent absolute values as
the outcome of an analysis, but we represent, for example, the risk of exceeding
a certain value. Different techniques do exist to study error propagation. We
can study the effect of changes on a particular attribute on our model outcome,
but in reality, all the input parameters will include a certain degree of error.
A more advanced method is called the Monte Carlo Simulation in which the
distribution of all input parameters are determined. The simulation model will
run many times and each time a new set of attributes will be drawn from their
respective distribution in our model outcome. 

During the practical you will be working on the creation of a Precipitation map
based on a variable number of measurement points in which you will discuss and
determine errors evident within the results.

New techniques have become available to avoid certain errors. Although many
changes on the earth surface are continuous, we tend to classify characteristics
and represent them as homogeneous objects on our maps. With fuzzy
classifications, we are able to capture more of this variability. Instead of
classifying a certain position to a certain class it is expressed as a
continuous membership function having values between 0 and 1. A position can be
a member of overlapping classes to different degrees. However, very few GIS
packages already provide capabilities to deal with fuzzy classifications.

Finally, many characteristics of the earth surface are not constant as they vary
temporally. We monitor these variables over time and introduce a new fourth
dimension to our database: time. GIS that are capable to deal with this fourth
dimension of time are called temporal GIS.


.. todo: add more things