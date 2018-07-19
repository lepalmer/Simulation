from BurstCube.NoahSim import fastcube
from BurstCube.NoahSim import GRBgenerator
import numpy as np
import unittest


@unittest.skip("Skipping this test until the code is optimized.")
def test_fastcube():
        testsim = GRBgenerator.Sky(1, 500)
        testcube = fastcube.FastCube(1000, 45)
        testresponse = testcube.response2GRB(testsim, samples=10,
                                             test=True, talk=False)

        # leaving this a little more room for error
        # since I'm messing up one detector.
        np.testing.assert_allclose(testresponse[0], 6.0, 1.0)
