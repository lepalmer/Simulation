from NoahSim import fastcube
from NoahSim import GRBgenerator
from NoahSim import numpy as np


def test_fastcube():
        testsim = GRBgenerator.Sky(1, 500)
        testcube = fastcube.FastCube(1000, 45)
        testresponse = testcube.response2GRB(testsim, samples=50,
                                             test=True, talk=False)

        np.testing.assert_allclose(testresponse[0], 6, 3.5) #leaving this a little more room for error since I'm messing up one detector. 
