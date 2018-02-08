import numpy as np
import healpy as hp
import burstSim 
import GRBgenerator

def test_BurstCube():
	bg = 1000
	testtilt = 45
	testcube = burstSim.BurstCube(bg,testtilt)
	assert testcube.tilt == np.deg2rad(testtilt)
	assert testcube.bg == bg

#	GRB = GRBgenerator.sky(4,500)

	# make sure every value is below a certain val? 

#	assert testcube.response2GRB = 1000
