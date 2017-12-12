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

    x = np.array([[28.64999962, 100., 71.73699951, 66.28498840, 69.65662384],
                  [28.64999962, 200., 68.58593750, 62.48178864, 64.60795593],
                  [57.29999924, 100., 56.56450653, 48.75860214, 53.67971420],
                  [57.29999924, 200., 54.40552521, 48.96497345, 50.81476212]],
                 dtype=np.float32)

    # the assert methods don't like
    # record arrays so you have to
    # convert to a regular numpy
    # array
    y = aeffs.view(np.float32).reshape(aeffs.shape + (-1,))

    assert_allclose(x, y, 1e-12)
