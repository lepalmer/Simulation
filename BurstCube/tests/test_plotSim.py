#!/usr/bin/env python

import numpy as np
from numpy.testing import assert_allclose

try:
    from BurstCube.plotSim import getGBMdata
except ImportError:
    pass


def test_getGBMdata():

    gbmdata = getGBMdata()

    aeff = np.array([6.043869, 7.1733994, 9.051345, 11.009052,
                     13.555708, 17.315489, 23.22683, 30.780512,
                     43.367252, 58.89598, 80.0014, 97.346825,
                     106.105095, 120.00855, 102.37214, 123.06248,
                     132.68503, 131.2247, 75.82555, 42.783394,
                     30.818037, 32.459995])

    assert_allclose(aeff, gbmdata['aeff'], 1e-3)
