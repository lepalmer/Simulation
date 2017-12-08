#!/usr/bin/env python

import numpy as np
from numpy.testing import assert_allclose
from astropy.tests.helper import pytest

try:
    from bcSim import bcSim
except ImportError:
    pass


@pytest.fixture(scope='module')
def create_burstcube_analysis(request, tmpdir_factory):

    from os import path

    testdir = path.expandvars('$BURSTCUBE/Simulation/MEGAlib/test/')
    bcs = bcSim(testdir+'test.inc1.id1.sim',testdir+'FarFieldPointSource_test.source')
    return bcs

def test_bcSim_setup(create_burstcube_analysis):
    bcs = create_burstcube_analysis
    bcs.printDetails()

def test_calculateAeff(create_burstcube_analysis):

    bcs = create_burstcube_analysis
    aeff = bcs.calculateAeff()

    assert (np.abs(aeff - 69.47044919706765) < 1e-7)

def test_passEres(create_burstcube_analysis):

    bcs = create_burstcube_analysis
    fractions = bcs.passEres()

    assert_allclose(fractions, (0.897,0.936), 1e-3)

