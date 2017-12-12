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

    
def test_calculateAeff(create_simfile):

    sf = create_simfile
    aeff = sf.calculateAeff()

    assert (np.abs(aeff - 69.47044919706765) < 1e-7)

    
def test_passEres(create_simfile):

    sf = create_simfile
    fractions = sf.passEres()

    assert_allclose(fractions, (0.897, 0.936), 1e-3)

def test_calculateAeffs(create_simfiles):

    sfs = create_simfiles
    aeffs = sfs.calculateAeff()

    x = np.array([(71.73699951),
                  (68.58593750),
                  (56.56450653),
                  (54.40552521)])
    
    assert_allclose(aeffs['aeff'], x, 1e-6)
