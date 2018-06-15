from BurstCube.NoahSim import fastcube
from BurstCube.NoahSim import GRBgenerator
import numpy as np

def test_GRBgenerator():

        testsim = GRBgenerator.Sky(1, 500)
        
        assert ((testsim.Ao == 500) & (testsim.pixels == 12))
        
def test_GRBgeneratorSourceAngs():

        testsim = GRBgenerator.Sky(1, 500)

        result = [(0.84106867056793033, 0.78539816339744828),
                  (0.84106867056793033, 2.3561944901923448),
                  (0.84106867056793033, 3.926990816987241),
                  (0.84106867056793033, 5.497787143782138),
                  (1.5707963267948966, 0.0),
                  (1.5707963267948966, 1.5707963267948966),
                  (1.5707963267948966, 3.1415926535897931),
                  (1.5707963267948966, 4.7123889803846897),
                  (2.3005239830218631, 0.78539816339744828),
                  (2.3005239830218631, 2.3561944901923448),
                  (2.3005239830218631, 3.926990816987241),
                  (2.3005239830218631, 5.497787143782138)]

        assert (testsim.sourceangs == result)
        

def test_fastcube():
        testsim = GRBgenerator.Sky(1, 500)
        testcube = fastcube.FastCube(1000, 45)
        testresponse = testcube.response2GRB(testsim, samples=10,
                                             test=True, talk=False)

        # leaving this a little more room for error
        # since I'm messing up one detector.
        np.testing.assert_allclose(testresponse[0], 6.0, 1.0)
