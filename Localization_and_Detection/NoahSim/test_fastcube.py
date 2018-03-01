import fastcube
import time 
import GRBgenerator
import numpy as np

def test_fastcube():
	testsim = GRBgenerator.Sky(1,500)

	testcube = fastcube.FastCube(1000,45)
	start = time.time()

	testresponse = testcube.response2GRB(testsim,test=True,talk=False)
	end = time.time()

	elapsed = end-start   #should be about 1 second to do 50 samples...

	#response should also be +- 1.5 degrees of 6

	stuff = np.array([elapsed, testresponse[0]])  #it returns an array, and only care about that one value so just call it like that. 

	np.testing.assert_allclose(stuff,(1,6),1.5)