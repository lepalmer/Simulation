import fastcube
import GRBgenerator
import numpy as np


def test_fastcube():
        testsim = GRBgenerator.Sky(1, 500)
        testcube = fastcube.FastCube(1000, 45)
        testresponse = testcube.response2GRB(testsim, samples=50,
                                             test=True, talk=False)

        np.testing.assert_allclose(testresponse[0], 6, 1.5)
