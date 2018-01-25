.. BurstCube Documentation documentation master file, created by
   sphinx-quickstart on Wed Jan 24 13:20:15 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BurstCube's documentation!
=====================================

##################################
Introduction
##################################

This is the BurstCube's documentation page.  More stuff will go here soon but this is mostly fluff to look nice. Here's a link to the website, I hope it works!
`BurstCube Website
<https://asd.gsfc.nasa.gov/burstcube/>`_.

BurstCube is built with a series of different functions and modules, but since I don't know all of them well enough, here's what FermiPy does to confirm this format works:

* Data and model preparation with the gt-tools (gtselect, gtmktime,
  etc.).

* Extracting a spectral energy distribution (SED) of a source.

* Generating TS and residual maps for a region of interest.

* Finding new source candidates.

* Localizing a source or fitting its spatial extension.

BurstCube uses a configuration-file driven workflow in which the
analysis parameters (data selection, IRFs, and ROI model) are defined
in a YAML configuration file.  Analysis is executed through a python
script.


Getting Help
------------

If you have questions about using this please open a `GitHub Issue
<https://github.com/BurstCube/Simulation/issues>`_ or email me at `this <mailto:nkasmanoff@gmaila.com>`_.


Acknowledging BurstCube
-------------------------

I'm assuming I won't need this section but just in case here it is!



Documentation Contents
-----------------------

.. toctree::
   :includehidden:
   :maxdepth: 3

   tutorial 
   create
   run


Indices and tables
==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`