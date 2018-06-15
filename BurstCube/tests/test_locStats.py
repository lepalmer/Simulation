#!/usr/bin/env python

import numpy as np
from numpy.testing import assert_allclose
# from astropy.tests.helper import pytest
# from pkg_resources import resource_filename

try:
    from BurstCube.LocSim import Stats
except ImportError:
    pass

a = np.array([[[5.3, 55, 91, 100, 83, 42, 0, 0, 0, 0, 0, 0],
               [0.11, 0.44, 0.63, 0.68, 0.59, 0.37, 0, 0, 0, 0, 0, 0]],
              [[68, 85, 65, 11, 0, 0, 0, 0, 0, 0, 46, 100],
               [0.57, 0.67, 0.55, 0.19, 0, 0, 0, 0, 0, 0, 0.43, 0.76]]])

b = np.array([[[60, 59, 32, 0, 0, 0, 0, 0, 0, 19, 64, 100],
               [0.48, 0.48, 0.32, 0, 0, 0, 0, 0, 0, 0.23, 0.50, 0.69]],
              [[80, 72, 34, 0, 0, 0, 0, 0, 0, 20, 69, 100],
               [0.59, 0.54, 0.33, 0, 0, 0, 0, 0, 0, 0.24, 0.53, 0.69]]])

c = np.array([[[0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]],
              [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1]]])


def test_calcNorms():

    result = np.array([[198.99520095, 207.20060328],
                       [51.33225107, 48.20788317]])
    
    norms = Stats.calcNorms(a, b)

    assert_allclose(norms, result, 1e-6)

    
def test_addErrors():
    
    errors = Stats.addErrors(a, b)

    assert_allclose(errors, c, 1e-6)

    
def test_calcNormsWithError():
    
    result = np.array([[[199.7, 207.1],
                        [52.3, 48.4]],
                       [[198.3, 207.3],
                        [50.4, 48.1]]])

    norms_err = Stats.calcNormsWithError(a, b, c)

    assert_allclose(norms_err, result, 1e-3)
