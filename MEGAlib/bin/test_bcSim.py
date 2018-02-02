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
                 testdir+'FarFieldPointSource_test.source',
                 testdir+'FarFieldPointSource_test.stdout.gz',)
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

    assert_allclose(fractions, (0.911, 0.936), 1e-2)


def test_calculateAeffs(create_simfiles):

    sfs = create_simfiles
    aeffs = sfs.calculateAeff()

    x = np.array([[60.00, 100.00, 56.04, 48.92, 53.23],
                  [60.00, 173.21, 51.66, 46.18, 48.51],
                  [60.00, 300.00, 47.99, 39.16, 40.02],
                  [41.41, 100.00, 69.02, 62.67, 66.53],
                  [41.41, 173.21, 67.04, 61.61, 64.03],
                  [41.41, 300.00, 56.55, 45.75, 46.82],
                  [0.00, 100.00, 76.69, 71.63, 75.08],
                  [0.00, 173.21, 76.60, 71.93, 73.62],
                  [0.00, 300.00, 64.48, 52.68, 54.23]],
                 dtype=np.float32)
    
    # the assert methods don't like
    # record arrays so you have to
    # convert to a regular numpy
    # array
    y = aeffs.view(np.float32).reshape(aeffs.shape + (-1,))

    assert_allclose(x, y, 0.1)

    
def test_TriggerProb(create_simfile):

    sf = create_simfile
    prob = sf.getTriggerProbability(1, False)

    assert_allclose(prob, (200.0, 30.0, 0.0316, 1.00), 1e-3)


def test_AllTriggerProb(create_simfiles):

    sfs = create_simfiles

    probs = sfs.getAllTriggerProbability(1, False)

    x = np.array([[100.00, 60.00, 0.03162277, 1.],
                  [173.21, 60.00, 0.03162277, 1.],
                  [300.00, 60.00, 0.03162277, 1.],
                  [100.00, 41.41, 0.03162277, 1.],
                  [173.21, 41.41, 0.03162277, 1.],
                  [300.00, 41.41, 0.03162277, 1.],
                  [100.00,  0.00, 0.03162277, 1.],
                  [173.21,  0.00, 0.03162277, 1.],
                  [300.00,  0.00, 0.03162277, 1.]],
                 dtype=np.float32)

    # the assert methods don't like
    # record arrays so you have to
    # convert to a regular numpy
    # array
    y = probs.view(np.float32).reshape(probs.shape + (-1,))

    assert_allclose(x, y, 1e-3)
