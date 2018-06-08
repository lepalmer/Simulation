#!/usr/bin/env python

import numpy as np
from numpy.testing import assert_allclose
from astropy.tests.helper import pytest
from pkg_resources import resource_filename

try:
    from BurstCube.bcSim import simFile
except ImportError:
    pass

try:
    from BurstCube.bcSim import simFiles
except ImportError:
    pass


@pytest.fixture(scope='module')
def create_simfile(request):

    sf = simFile(resource_filename('BurstCube',
                                   'data/test.inc1.id1.sim'),
                 resource_filename('BurstCube',
                                   'data/FarFieldPointSource_test.source'),
                 resource_filename('BurstCube',
                                   'data/FarFieldPointSource_test.stdout.gz'))
    return sf


@pytest.fixture(scope='module')
def create_simfiles(request):

    sfs = simFiles(resource_filename('BurstCube', 'data/config.yaml'))

    return sfs


def test_bcSim_setup(create_simfile):
    sf = create_simfile
    sf.printDetails()


# Don't need since files are installed in package
# def test_setPath():
#    from BurstCube.utils import setPath
#    assert(not setPath())

    
def test_energy(create_simfile):

    sf = create_simfile
    energy = sf.energy

    assert (np.abs(energy - 200.0) < 1e-7)

    
def test_az(create_simfile):

    sf = create_simfile
    azimuth = sf.azimuth
    
    assert (np.abs(azimuth - 0.0) < 1e-7)

    
def test_ze(create_simfile):

    sf = create_simfile
    zenith = sf.zenith
    
    assert (np.abs(zenith - 30.0) < 1e-7)

    
def test_calculateAeff(create_simfile):

    sf = create_simfile
    aeff = sf.calculateAeff()

    assert (np.abs(aeff - 69.5) < 3.0)

    
def test_calculateAeff_Eres(create_simfile):

    sf = create_simfile
    aeff = sf.calculateAeff(True, 2*7.5)

    assert (np.abs(aeff - 64.0) < 3.0)
    

def test_passEres(create_simfile):

    sf = create_simfile
    fractions = sf.passEres()

    assert_allclose(fractions, (0.911, 0.936), 1e-2)


def test_calculateAeffs(create_simfiles):

    sfs = create_simfiles
    aeffs = sfs.calculateAeff()

    x = np.array([[0.00, 0.00, 100.00, 76.50, 70.45, 73.74],
                  [0.00, 0.00, 173.21, 81.25, 76.29, 78.81],
                  [0.00, 0.00, 300.00, 61.17, 50.22, 51.93],
                  [30.00, 0.00, 100.00, 72.12, 66.78, 70.39],
                  [30.00, 0.00, 173.21, 80.57, 74.61, 77.35],
                  [30.00, 0.00, 300.00, 63.12, 50.30, 51.82],
                  [60.00, 0.00, 100.00, 76.38, 70.04, 73.48],
                  [60.00, 0.00, 173.21, 76.02, 69.86, 72.82],
                  [60.00, 0.00, 300.00, 66.70, 54.83, 56.16],
                  [0.00, 30.00, 100.00, 74.55, 69.11, 72.54],
                  [0.00, 30.00, 173.21, 70.47, 65.25, 67.72],
                  [0.00, 30.00, 300.00, 58.44, 47.39, 48.74],
                  [30.00, 30.00, 100.00, 78.24, 71.28, 75.74],
                  [30.00, 30.00, 173.21, 71.61, 66.38, 68.31],
                  [30.00, 30.00, 300.00, 62.53, 50.46, 51.71],
                  [60.00, 30.00, 100.00, 74.76, 69.53, 72.75],
                  [60.00, 30.00, 173.21, 73.51, 68.66, 69.98],
                  [60.00, 30.00, 300.00, 58.51, 47.51, 48.80],
                  [0.00, 60.00, 100.00, 54.08, 47.26, 51.65],
                  [0.00, 60.00, 173.21, 49.26, 44.48, 46.26],
                  [0.00, 60.00, 300.00, 45.81, 35.78, 37.10],
                  [30.00, 60.00, 100.00, 55.15, 48.92, 53.27],
                  [30.00, 60.00, 173.21, 51.25, 46.33, 48.43],
                  [30.00, 60.00, 300.00, 44.65, 35.18, 36.25],
                  [60.00, 60.00, 100.00, 54.05, 47.24, 51.56],
                  [60.00, 60.00, 173.21, 51.95, 46.55, 48.57],
                  [60.00, 60.00, 300.00, 42.65, 34.29, 35.57]],
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

    assert_allclose(prob, (200.0, 0.0, 30.0, 0.0316, 1.00), 1e-3)


def test_AllTriggerProb(create_simfiles):

    sfs = create_simfiles

    probs = sfs.getAllTriggerProbability(1, False)

    x = np.array([[100.00, 0.00, 0.00, 0.0316, 1.00],
                  [173.21, 0.00, 0.00, 0.0316, 1.00],
                  [300.00, 0.00, 0.00, 0.0316, 1.00],
                  [100.00, 30.00, 0.00, 0.0316, 1.00],
                  [173.21, 30.00, 0.00, 0.0316, 1.00],
                  [300.00, 30.00, 0.00, 0.0316, 1.00],
                  [100.00, 60.00, 0.00, 0.0316, 1.00],
                  [173.21, 60.00, 0.00, 0.0316, 1.00],
                  [300.00, 60.00, 0.00, 0.0316, 1.00],
                  [100.00, 0.00, 30.00, 0.0316, 1.00],
                  [173.21, 0.00, 30.00, 0.0316, 1.00],
                  [300.00, 0.00, 30.00, 0.0316, 1.00],
                  [100.00, 30.00, 30.00, 0.0316, 1.00],
                  [173.21, 30.00, 30.00, 0.0316, 1.00],
                  [300.00, 30.00, 30.00, 0.0316, 1.00],
                  [100.00, 60.00, 30.00, 0.0316, 1.00],
                  [173.21, 60.00, 30.00, 0.0316, 1.00],
                  [300.00, 60.00, 30.00, 0.0316, 1.00],
                  [100.00, 0.00, 60.00, 0.0316, 1.00],
                  [173.21, 0.00, 60.00, 0.0316, 1.00],
                  [300.00, 0.00, 60.00, 0.0316, 1.00],
                  [100.00, 30.00, 60.00, 0.0316, 1.00],
                  [173.21, 30.00, 60.00, 0.0316, 1.00],
                  [300.00, 30.00, 60.00, 0.0316, 1.00],
                  [100.00, 60.00, 60.00, 0.0316, 1.00],
                  [173.21, 60.00, 60.00, 0.0316, 1.00],
                  [300.00, 60.00, 60.00, 0.0316, 1.00]],
                 dtype=np.float32)

    # the assert methods don't like
    # record arrays so you have to
    # convert to a regular numpy
    # array
    y = probs.view(np.float32).reshape(probs.shape + (-1,))

    assert_allclose(x, y, 1e-3)
