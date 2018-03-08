.. BurstCube Documentation documentation master file, created by
   sphinx-quickstart on Wed Jan 24 13:20:15 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BurstCube's documentation!
=====================================

##################################
Introduction
##################################

This is the BurstCube's documentation page. For more information about the misson, please refer to the 
`BurstCube Website
<https://asd.gsfc.nasa.gov/burstcube/>`_.

BurstCube's documentation is built with a series of different functions and modules that allow the following:

* Creating different geometry files to allow for new arrangements of BurstCube to be subject to testing. 

* Creating source files of ranging sky locations and energies. 

* Quick manipulation of the MEGAlib Cosima function to permit quick simulations. 

* Packages such as bcSim and plotSim that grant fast and effective data processing. 


BurstCube uses a configuration-file driven workflow in which the
analysis parameters (data selection, IRFs, and ROI model) are defined
in a YAML configuration file.  Analysis is executed through a python
script.


Getting Help
------------

If you have questions about using this please open a `GitHub Issue
<https://github.com/BurstCube/Simulation/issues>`_ or email `me <mailto:nkasmanoff@gmail.com>`_ or my `boss <mailto:jeremy.s.perkins@nasa.gov>`_.



Documentation Contents
-----------------------

.. toctree::
   :includehidden:
   :maxdepth: 2

   tutorial 
   megalibstuff
   noahsims
