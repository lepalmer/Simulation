#!/usr/bin/env python

import numpy as np
from numpy.testing import assert_allclose
import unittest
import os
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt


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

    
@unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
                 "Skipping this test on Travis CI.")
@image_comparison(baseline_images=['spines_axes_positions'],
                  extensions=['png'])
def test_spines_axes_positions():
    # SF bug 2852168
    fig = plt.figure()
    x = np.linspace(0,2*np.pi,100)
    y = 2*np.sin(x)
    ax = fig.add_subplot(1,1,1)
    ax.set_title('centered spines')
    ax.plot(x,y)
    ax.spines['right'].set_position(('axes',0.1))
    ax.yaxis.set_ticks_position('right')
    ax.spines['top'].set_position(('axes',0.25))
    ax.xaxis.set_ticks_position('top')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')

    
@unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
                 "Skipping this test on Travis CI.")
@image_comparison(baseline_images=['plotAeffvsEnergy'],
                  extensions=['png'])
def test_plotAeffvsEnergy():
    '''Makes a test of the effective area versus energy
    with a zenith of 15 degrees and an azimuth of 0 degrees
    (6 bins)'''
                  
    energy = np.array([25, 52.28198, 109.336205, 228.65253, 478.17624, 1000])
    aeff = np.array([29.357716, 72.52194, 75.67477,
                     70.827415, 49.87035, 35.3552])
    aeff_eres = np.array([29.240286, 60.483303,
                          70.75591, 62.753094, 30.02195, 12.551097])
    aeff_eres_modfrac = ([29.240286, 71.0715, 73.858574,
                          64.665436, 30.670265, 25.102194])
    az = 0
    ze = 0
    plotGBM = True
    
    plt.figure(figsize=(8, 6))
    plt.title(r'Effective Area vs. Energy ' +
              '($zenith$ = {:,.0f}$^\circ$, '.format(ze) +
              '$azimuth$ = {:,.0f}$^\circ$)'.format(az))
    plt.scatter(energy, aeff, color='black')
    plt.plot(energy, aeff, color='black', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube')
    plt.scatter(energy, aeff_eres, color='blue')
    plt.plot(energy, aeff_eres, color='blue', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube with E$_{\mathrm{res}}$')
    plt.scatter(energy, aeff_eres_modfrac, color='red')
    plt.plot(energy, aeff_eres_modfrac, color='red', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube with E$_{\mathrm{res}}$ + escape')

    if plotGBM:
        gbmdata = getGBMdata()
        plt.plot(gbmdata['energy'], gbmdata['aeff'], color='green', alpha=0.75,
                 linestyle='-', lw=2, label='GBM NaI')

    plt.xscale('log')
    plt.xlabel('Energy (keV)', fontsize=16)
    plt.yscale('log')
    plt.ylabel('Effective Area (cm$^2$)', fontsize=16)
    plt.legend(loc='lower center', prop={'size': 16}, numpoints=1,
               frameon=False)

    
@unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
                 "Skipping this test on Travis CI.")
@image_comparison(baseline_images=['plotAeffvsTheta'],
                  extensions=['png'])
def test_plotAeffvsTheta():
    '''Makes a test of the effective area versus the incidence
    angle with an energy of 1000 keV and azimuth of 0 degrees
    (3 bins)'''
                  
    theta = np.array([1000, 1000, 1000])
    aeff = ([35.314983, 33.65521, 31.056171])
    aeff_eres = ([13.560953, 12.385118, 10.776491])
    aeff_eres_modfrac = ([27.192537, 24.8712, 21.646152])
    energy = 1000
    paren = ''

    plt.figure(figsize=(8, 6))
    plt.title(r'Effective Area vs. Angle (E = {:,.0f} keV{})'
              .format(energy, paren))
    plt.scatter(theta, aeff, color='black')
    plt.plot(theta, aeff, color='black', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube')
    plt.scatter(theta, aeff_eres, color='blue')
    plt.plot(theta, aeff_eres, color='blue', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube with E$_{\mathrm{res}}$')
    plt.scatter(theta, aeff_eres_modfrac, color='red')
    plt.plot(theta, aeff_eres_modfrac, color='red', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube with E$_{\mathrm{res}}$ + escape')

    plt.xlabel('Incident Angle (deg)', fontsize=16)
    plt.ylabel('Effective Area (cm$^2$)', fontsize=16)
    plt.legend(loc='lower center', scatterpoints=1, prop={'size': 16},
               frameon=False)
    plt.grid(True)

@unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
                 "Skipping this test on Travis CI.")
@image_comparison(baseline_images=['plotAeffvsPhi'],
                  extensions=['png'])
def test_plotAeffvsPhi():
    '''Makes a test of the effective area versus the azimuth
    angle with an energy of 1000 keV a zenith of 15 degrees
    (3 bins)'''

    azimuth = ([0, 30, 60])
    aeff = ([35.314983, 33.65521, 31.056171])
    aeff_eres = ([13.560953, 12.385118, 10.776491])
    aeff_eres_modfrac = ([27.192537, 24.8712, 21.646152])
    
    plt.figure(figsize=(8, 6))
    plt.title('Effective Area vs. Angle')
    plt.scatter(azimuth, aeff, color='black')
    plt.plot(azimuth, aeff, color='black', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube')
    plt.scatter(azimuth, aeff_eres, color='blue')
    plt.plot(azimuth, aeff_eres, color='blue', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube with E$_{\mathrm{res}}$')
    plt.scatter(azimuth, aeff_eres_modfrac, color='red')
    plt.plot(azimuth, aeff_eres_modfrac, color='red',
             alpha=0.5, linestyle='--',
             lw=2, label='BurstCube with E$_{\mathrm{res}}$ + escape')

    plt.xlabel('Azimuth Angle (deg)', fontsize=16)
    plt.ylabel('Effective Area (cm$^2$)', fontsize=16)
    plt.legend(loc='lower center', scatterpoints=1, prop={'size': 16},
               frameon=False)
    plt.axis('tight')
    plt.grid(True)
