#!/usr/bin/env python

try:
    import matplotlib.pyplot as plt

    # Set the default title font dict
    titleFormat = {'fontsize': 12,
                   'fontweight': 14,
                   'verticalalignment': 'baseline',
                   'horizontalalignment': 'center'}

except ImportError:
    print("\n**** Warning: matplotlib not found. " +
          "Do not try to make plots or bad things will happen! ****")
    exit()

from matplotlib import gridspec
import numpy as np


def getGBMdata(gbmfile=''):
    
    """Reads the GBM NaI effective area file and returns a numpy array
    with two columns ``energy`` and ``aeff``.

    Parameters
    ----------
    gbmfile : string
       Name of file that contains the GBM data.  If not given, will
       look in the installed location.

    Returns
    ----------
    gbmdata : array 
    numpy array with two columns ``energy`` and ``aeff``
    """
    
    from pkg_resources import resource_filename
    from numpy import genfromtxt
    from os import path

    if gbmfile is '':
        gbmfile = resource_filename('BurstCube', 'data/gbm_effective_area.dat')

    gbmfile = path.expandvars(gbmfile)
    
    return genfromtxt(gbmfile,
                      skip_header=2,
                      names=('energy', 'aeff'))

    
def plotAeffvsEnergy(energy, aeff, aeff_eres, aeff_eres_modfrac,
                     az=0, ze=0, plotGBM=False):
    
    """Plots the GBM NaI effective area against the energy of that source.
    

    Parameters
    ----------
    energy : array
       numpy array of energy in units of keV of the sources.

    aeff : array
        numpy array with GBM NaI effective area.

    aeff_eres : array
        I'll look up energy resulution later

    aeff_eres_modfrac : array
        plus escape? 

    Returns
    ----------
    a plot of the effective area vs. energy. 
    """
    
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

def plotAeffvsPhi(azimuth, aeff, aeff_eres, aeff_eres_modfrac):

    """Plots the GBM NaI effective area against the polar angle phi used
    to generate that source.
    
    Parameters
    ----------
    azimuth : array
       numpy array of the angle in deg of the source. 
    aeff : array
        numpy array with GBM NaI effective area. 
    aeff_eres : array
        I'll look up energy resulution later
    aeff_eres_modfrac : array
        plus escape? 
    Returns
    ----------
    a plot!
    """
    plt.figure(figsize=(8, 6))
    plt.title('Effective Area vs. Angle')
    plt.scatter(azimuth, aeff, color='black')
    plt.plot(azimuth, aeff, color='black', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube')
    plt.scatter(azimuth, aeff_eres, color='blue')
    plt.plot(azimuth, aeff_eres, color='blue', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube with E$_{\mathrm{res}}$')
    plt.scatter(azimuth, aeff_eres_modfrac, color='red')
    plt.plot(azimuth, aeff_eres_modfrac, color='red', alpha=0.5, linestyle='--',
             lw=2, label='BurstCube with E$_{\mathrm{res}}$ + escape')

    plt.xlabel('Azimuth Angle (deg)', fontsize=16)
    plt.ylabel('Effective Area (cm$^2$)', fontsize=16)
    plt.legend(loc='lower center', scatterpoints=1, prop={'size': 16},
               frameon=False)
    plt.axis('tight')
    plt.grid(True)

    
def plotAeffvsTheta(theta, aeff, aeff_eres, aeff_eres_modfrac,
                    energy=100., paren=''):

    """Plots the GBM NaI effective area against the polar angle theta used
    to generate that source.
    

    Parameters
    ----------
    theta : array
       numpy array of the angle in deg of the source. 

    aeff : array
        numpy array with GBM NaI effective area. 

    aeff_eres : array
        I'll look up energy resulution later

    aeff_eres_modfrac : array
        plus escape? 

    Returns
    ----------
    a plot!

    """
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

    
def plotAeff(simFiles, useEres=False, plotGBM=False):

    """Plots the GBM NaI effective area against the changing parts of the
    simulation

    Parameters
    ----------
    simFiles : list
       Simulation files generated by MEGAlib.


    Returns
    ----------
    a bunch of plots!

    """
    aeffs = simFiles.calculateAeff(useEres)

    for az in set(aeffs['az']):
        for ze in set(aeffs['ze']):
            mask = (aeffs['az'] == az) & (aeffs['ze'] == ze)
            plotAeffvsEnergy(aeffs['keV'][mask],
                             aeffs['aeff'][mask],
                             aeffs['aeff_eres'][mask],
                             aeffs['aeff_eres_modfrac'][mask],
                             az=az, ze=ze, plotGBM=plotGBM)
    
    plt.show()

    for az in set(aeffs['az']):
        for energy in set(aeffs['keV']):
            mask = (aeffs['keV'] == energy) & (aeffs['az'] == az)
            plotAeffvsTheta(aeffs['ze'][mask],
                            aeffs['aeff'][mask],
                            aeffs['aeff_eres'][mask],
                            aeffs['aeff_eres_modfrac'][mask],
                            energy, ', Az = {:,.0f} deg'.format(az))
            plt.grid(True)

    plt.show()

    
def plotAeffComparison(sims, names, useEres=False, compareTo='GBM',
                       axis='ze', elim=(1, 1e5)):

    """Makes Aeff comparison plots of two or more simulations.

    Parameters
    ----------
    sims : list
       List of simulation objects that need to be compared.

    names : list
       List of strings used to label the plots.  Should be
       the same length as the sims list.

    compareTo : string
       The curve to make the comparison to in the percent difference.
       Default is GBM.  You can pick any of the other curves in the
       `names` list.
    
    axis : string
       Either `ze` or `az` for the angle axis to plot against.

    Returns
    ----------
       Nothing

    """

    colors = plt.cm.rainbow(np.linspace(0, 1, len(sims)))

    gbmdata = getGBMdata()
    if compareTo == 'GBM':
        comp_aeff = sims[0].calculateAeff(useEres=useEres)
    else:
        i = names.index(compareTo)
        comp_aeff = sims[i].calculateAeff(useEres=useEres)

    for angle in set(comp_aeff[axis]):
        
        mask = comp_aeff[axis] == angle

        if compareTo == 'GBM':
            gbminterp = np.interp(comp_aeff['keV'][mask],
                                  gbmdata['energy'],
                                  gbmdata['aeff'])

        plt.figure(figsize=(8, 6))
        plt.subplots_adjust(hspace=0.0)
        gs = gridspec.GridSpec(2, 1,
                               height_ratios=[4, 1])
        
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])

        ax1.set_title(r'Effective Area vs. Energy ($angle$ = {:,.0f}$^\circ$)'
                      .format(angle))
        ax1.set_xscale('log')
        ax1.set_xlabel('Energy (keV)', fontsize=16)
        ax1.set_yscale('log')
        ax1.set_ylabel('Effective Area (cm$^2$)', fontsize=16)
        ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)

        ax2.set_xscale('log')
        ax2.set_xlabel('Energy (keV)', fontsize=16)
        ax2.set_ylabel('% Diff', fontsize=16)

        ax1.plot(gbmdata['energy'], gbmdata['aeff'], color='green', alpha=0.75,
                 linestyle='-', lw=2, label='GBM NaI')
        ax1.set_xlim(elim)
    
        for sim, name, color in zip(sims, names, colors):
            aeffs = sim.calculateAeff(useEres=useEres)
            energy = aeffs['keV'][mask]
            aeff = aeffs['aeff'][mask]

            ax1.scatter(energy, aeff, color=color)
            ax1.plot(energy, aeff, alpha=0.5, linestyle='--',
                     lw=2, label=name, color=color)
            ax1.legend(loc='lower center', prop={'size': 16}, numpoints=1,
                       frameon=False)
        
            if compareTo == 'GBM':
                diff = 100.*(aeff - gbminterp) / gbminterp
            else:
                diff = 100.*(aeff -
                             comp_aeff['aeff'][mask])/comp_aeff['aeff'][mask]

            ax2.scatter(energy, diff, color=color)
            ax2.set_xlim(ax1.get_xlim())
            plt.setp(ax2.get_yticklabels()[-1], visible=False)
        plt.show()

        
def plotThetaComparison(sims, names, axis='ze', compareTo='',
                        useEres=False, energy=100):

    """Makes Theta comparison plots of two or more simulations.

    Parameters
    ----------
    sims : list
       List of simulation objects that need to be compared.

    names : list
       List of strings used to label the plots.  Should be
       the same length as the sims list.

    compareTo : string
       The curve to make the comparison to in the percent difference.
       Default is the first in the list.  You can pick any of the
       other curves in the `names` list.

    energy : float
       The energy bin (in keV) to plot.

    Returns
    ----------
       Nothing

    """

    colors = plt.cm.rainbow(np.linspace(0, 1, len(sims)))

    if compareTo == '':
        i = 0
    else:
        i = names.index(compareTo)
    comp_aeff = sims[i].calculateAeff(useEres=useEres)

    for energy in set(comp_aeff['keV']):
        mask = comp_aeff['keV'] == energy
        
        plt.figure(figsize=(8, 6))
        plt.subplots_adjust(hspace=0.0)
        gs = gridspec.GridSpec(2, 1,
                               height_ratios=[4, 1])
        
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])

        ax1.set_title(r'Effective Area vs. Angle (E = {:,.0f} keV)'
                      .format(energy))

        ax1.set_xlabel('Incident Angle (deg)', fontsize=16)
        ax1.set_ylabel('Effective Area (cm$^2$)', fontsize=16)
        ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)

        ax2.set_xlabel('Incident Angle (deg)', fontsize=16)
        ax2.set_ylabel('% Diff', fontsize=16)

        for sim, name, color in zip(sims, names, colors):
            aeffs = sim.calculateAeff(useEres=useEres)
            aeff = aeffs['aeff'][mask]
            theta = aeffs['ze'][mask]
       
            ax1.scatter(theta, aeff, color=color)
            ax1.plot(theta, aeff, color=color, alpha=0.5, linestyle='--',
                     lw=2, label=name)
            ax1.legend(loc='lower center', scatterpoints=1, prop={'size': 16},
                       frameon=False)
            ax1.grid(True)
    
            diff = 100.*(aeff -
                         comp_aeff['aeff'][mask])/comp_aeff['aeff'][mask]
    
            ax2.scatter(theta, diff, color=color)
            ax2.set_xlim(ax1.get_xlim())
            plt.setp(ax2.get_yticklabels()[-1], visible=False)
        plt.show()
