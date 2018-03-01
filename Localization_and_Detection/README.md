Contained in this repository are the localization and detection simulations used for determining BurstCube's feasibility and optimizing performance. Attached to this readme so far is how to execute Noah's stuff. The name's of the programs pretty much sum up their purpose. 


Files
=====

GRBgenerator.py
---------------
This program allows you to generate GRBs throughout the sky. It depends on NSIDE and some given strength, where NSIDE corresponds to the # of pixels that will occupy the entire sky according to the formula npixels = 12* NSIDE^2.

fastcube.py
-----------
This program contains the simulated version of burstcube. Plenty of customizations of what this spacecraft are available, ranging from what sorts of detector tilts are possible, along with the kinds of backgrounds inherent in the detector. More nuances to be added. 

burstutils.py
-------------
All of the functions used throughout the simulations. For more information about each see the documentation. 

runnoahsims.py
--------------
How to quickly execute a simulation of a BurstCube orientation with easy control of the parameters. Further documentation provided in script. 


And in addition to all this, there are a bunch of test_*.py files. 

