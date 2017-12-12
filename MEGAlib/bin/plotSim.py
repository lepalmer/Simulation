#!/usr/bin/env python

try:
    import matplotlib.pyplot as plt

    # Set the default title font dict
    titleFormat = {'fontsize': 12,
                   'fontweight': plt.rcParams['axes.titleweight'],
                   'verticalalignment': 'baseline',
                   'horizontalalignment': 'center'}

except ImportError:
    print("\n**** Warning: matplotlib not found. " +
          "Do not try to make plots or bad things will happen! ****")
    exit()


def plotAeff(simFiles):

    aeffs = simFiles.calculateAeff()

    for angle in set(aeffs['theta']):
        mask = aeffs['theta'] == angle
        plt.figure(figsize=(8, 6))
        plt.title(r'Effective Area vs. Energy ($\theta$ = {:,.0f}$^\circ$)'
                  .format(angle))
        plt.scatter(aeffs['keV'][mask], aeffs['aeff'][mask], color='black')
        plt.plot(aeffs['keV'][mask], aeffs['aeff'][mask], color='black',
                 alpha=0.5, linestyle='--', lw=2, label='BurstCube')
        plt.scatter(aeffs['keV'][mask], aeffs['aeff_eres'][mask],
                    color='blue')
        plt.plot(aeffs['keV'][mask], aeffs['aeff_eres'][mask], color='blue',
                 alpha=0.5, linestyle='--', lw=2,
                 label='BurstCube with E$_{\mathrm{res}}$')
        plt.scatter(aeffs['keV'][mask], aeffs['aeff_eres_modfrac'][mask],
                    color='red')
        plt.plot(aeffs['keV'][mask], aeffs['aeff_eres_modfrac'][mask],
                 color='red', alpha=0.5, linestyle='--', lw=2,
                 label='BurstCube with E$_{\mathrm{res}}$ + escape')

        plt.xscale('log')
        plt.xlabel('Energy (keV)', fontsize=16)
        plt.yscale('log')
        plt.ylabel('Effective Area (cm$^2$)', fontsize=16)
        plt.legend(loc='lower center', prop={'size': 16}, numpoints=1,
                   frameon=False)

    plt.show()

    for energy in set(aeffs['keV']):
        mask = aeffs['keV'] == energy
        plt.figure(figsize=(8, 6))
        plt.title(r'Effective Area vs. Angle (E = {:,.0f} keV)'
                  .format(energy))
        plt.scatter(aeffs['theta'][mask], aeffs['aeff'][mask], color='black')
        plt.plot(aeffs['theta'][mask], aeffs['aeff'][mask], color='black',
                 alpha=0.5, linestyle='--', lw=2, label='BurstCube')
        plt.scatter(aeffs['theta'][mask], aeffs['aeff_eres'][mask],
                    color='blue')
        plt.plot(aeffs['theta'][mask], aeffs['aeff_eres'][mask], color='blue',
                 alpha=0.5, linestyle='--', lw=2,
                 label='BurstCube with E$_{\mathrm{res}}$')
        plt.scatter(aeffs['theta'][mask], aeffs['aeff_eres_modfrac'][mask],
                    color='red')
        plt.plot(aeffs['theta'][mask], aeffs['aeff_eres_modfrac'][mask],
                 color='red', alpha=0.5, linestyle='--', lw=2,
                 label='BurstCube with E$_{\mathrm{res}}$ + escape')

        plt.xlabel('Incident Angle (deg)', fontsize=16)
        plt.ylabel('Effective Area (cm$^2$)', fontsize=16)
        plt.legend(loc='lower center', scatterpoints=1, prop={'size': 16},
                   frameon=False)
        plt.grid(True)

    plt.show()
