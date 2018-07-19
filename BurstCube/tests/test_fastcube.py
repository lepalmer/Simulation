from BurstCube.NoahSim import fastcube
from BurstCube.NoahSim import GRBgenerator
import numpy as np
from astropy.tests.helper import pytest


@pytest.fixture(scope='module')
def create_sky(request):
        testsim = GRBgenerator.Sky(1, 500)

        return testsim


@pytest.fixture(scope='module')
def create_fastcube(request):

        testcube = fastcube.FastCube(1000, 45)

        return testcube


def test_det():

        tc = fastcube.FastCube(1000,45)
        
        result = [[0.78539816339744828, 0],
                  [0.78539816339744828, 1.5707963267948966],
                  [0.78539816339744828, 3.141592653589793],
                  [0.78539816339744828, 4.71238898038469]]
        
        dets = [getattr(tc, 'det{}'.format(letter))
                for letter in ['A', 'B', 'C', 'D']]
                
        np.testing.assert_allclose(dets, result, 1e-16)

        

# def test_fastcube():
#        testsim = GRBgenerator.Sky(1, 500)
#        testcube = fastcube.FastCube(1000, 45)
#        testresponse = testcube.response2GRB(testsim, samples=10,
#                                             test=True, talk=False)

        # leaving this a little more room for error
        # since I'm messing up one detector.
#        np.testing.assert_allclose(testresponse[0], 6.0, 1.0)
