#!/usr/bin/env python

import numpy as np
from numpy.testing import assert_allclose
from astropy.tests.helper import pytest
from os import path

try:
    from bcSim import simFile
except ImportError:
    pass

try:
    from bcSim import simFiles
except ImportError:
    pass


@pytest.fixture(scope='module')
def create_simfile(request, tmpdir_factory):

    testdir = path.expandvars('$BURSTCUBE/Simulation/MEGAlib/test/')
    sf = simFile(testdir+'test.inc1.id1.sim',
                 testdir+'FarFieldPointSource_test.source')
    return sf


@pytest.fixture(scope='module')
def create_simfiles(request, tmpdir_factory):

    testdir = path.expandvars('$BURSTCUBE/Simulation/MEGAlib/test/')
    sfs = simFiles(testdir+'config.yaml')

    return sfs


def test_bcSim_setup(create_simfile):
    sf = create_simfile
    sf.printDetails()


def test_setPath():
    from utils import setPath
    assert(not setPath())

    
def test_energy(create_simfile):

    sf = create_simfile
    energy = sf.energy

    assert (np.abs(energy - 200.0) < 1e-7)

    
def test_theta(create_simfile):

    sf = create_simfile
    energy = sf.theta
    
    assert (np.abs(energy - 30.0) < 1e-7)

    
def test_calculateAeff(create_simfile):

    sf = create_simfile
    aeff = sf.calculateAeff()

    assert (np.abs(aeff - 69.5) < 3.0)


def test_passEres(create_simfile):

    sf = create_simfile
    fractions = sf.passEres()

    assert_allclose(fractions, (0.897, 0.936), 1e-2)


def test_calculateAeffs(create_simfiles):

    sfs = create_simfiles
    aeffs = sfs.calculateAeff()

    x = np.array([[28.65, 100.00, 71.74, 66.28, 69.66],
                  [28.65, 173.21, 74.40, 69.05, 72.10],
                  [28.65, 300.00, 61.25, 50.53, 52.12],
                  [42.97, 100.00, 69.51, 62.84, 67.63],
                  [42.97, 173.21, 64.46, 58.91, 61.43],
                  [42.97, 300.00, 56.34, 46.14, 47.67],
                  [57.30, 100.00, 56.56, 48.76, 53.68],
                  [57.30, 173.21, 53.26, 47.45, 49.95],
                  [57.30, 300.00, 46.63, 37.91, 38.79]],
                 dtype=np.float32)

    # the assert methods don't like
    # record arrays so you have to
    # convert to a regular numpy
    # array
    y = aeffs.view(np.float32).reshape(aeffs.shape + (-1,))

    assert_allclose(x, y, 0.1)
