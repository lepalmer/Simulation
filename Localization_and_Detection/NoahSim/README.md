
Added this branch to work on creating a lookup table to simulate the potential shadowing effects that will influence certain detectors onboard BurstCube.


The work is done. Here's what I should do in front of Jeremy to make sure it doesn't get screweed up. 

Move the python files into the proper space. 

run the tests

push to master

check 

These tests should be working, I don't understand what's happening so that it doesn't read in "GRBgenerator.py etc. "








NoahSim
=======

In here is all of Noah Kasmanoff's python based simulations of BurstCube. The simulations generate GRBs of a given strength throughout the sky, and reproduce the effect in a model of BurstCube with the desired parameters (detector tilt, background, instrument shadowing, etc.) to reconstruct the GRB, and give the user a sense of how well BurstCube performs at a certain point and/or throughout the sky. TSM plotting also available. 


To run these simulations, on your terminal enter "python runnoahsims.py". Inside runnoahsims.py the parameters are designated. For more information please refer to the documentation available. 


email me at nkasmanoff@gmail.com for further questions/issues. 