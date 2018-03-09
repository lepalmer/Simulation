#!/usr/bin/env python

import numpy as np
from os import path


def createSourceString(config, energy, ze, az):

    """Creates a source file from a configurator object with a specific
    angle and energy

    Parameters
    ----------
    config : string
       The .yaml file the imposes the conditions for the source files desired.

    Returns
    ----------
    srcstr : string
       A sring which can be used to create a source file for cosima.
    """

    from utils import getFilenameFromDetails

    fname = getFilenameFromDetails({'base': config['run']['basename'],
                                    'keV': energy,
                                    'ze': ze,
                                    'az': az})

    srcstr = 'Version ' + str(config['general']['Version'])
    srcstr += '\n'
    srcstr += 'Geometry ' + str(config['general']['Geometry'])
    srcstr += '\n'
    srcstr += 'CheckForOverlaps ' + str(config['general']['CheckForOverlaps'])
    srcstr += '\n'
    srcstr += 'PhysicsListEM ' + str(config['general']['PhysicsListEM'])
    srcstr += '\n'
    srcstr += 'StoreCalibrate ' + str(config['general']['StoreCalibrate'])
    srcstr += '\n'
    srcstr += 'StoreSimulationInfo '
    srcstr += str(config['general']['StoreSimulationInfo'])
    srcstr += '\n'
    srcstr += 'StoreOnlyEventsWithEnergyLoss '
    srcstr += str(config['general']['StoreOnlyEventsWithEnergyLoss'])
    srcstr += '\n'
    srcstr += 'DiscretizeHits ' + str(config['general']['DiscretizeHits'])
    srcstr += '\n'
    srcstr += '\n'
    srcstr += 'Run ' + config['source']['name']
    srcstr += '\n'
    srcstr += config['source']['name']+'.Filename '
    srcstr += config['run']['simdir'] + fname
    srcstr += '\n'
    srcstr += config['source']['name']+'.NTriggers '
    srcstr += str(config['source']['NTriggers'])
    srcstr += '\n'
    srcstr += config['source']['name']+'.Source One'
    srcstr += '\n'
    srcstr += 'One.ParticleType ' + str(config['source']['ParticleType'])
    srcstr += '\n'
    srcstr += 'One.Beam ' + config['source']['Beam'] + ' '
    srcstr += str(np.round(ze, decimals=2)) + ' '
    srcstr += str(np.round(az, decimals=2))
    srcstr += '\n'
    srcstr += 'One.Spectrum Mono '
    srcstr += str(energy)
    srcstr += '\n'
    srcstr += 'One.Flux ' + str(config['source']['Flux'])
    srcstr += '\n'

    return srcstr


class configurator():

    def __init__(self, path):

        self.config = self.loadConfig(path)

    def loadConfig(self, path):
        """
        """
        import yaml

        with open(path, 'r') as f:
            config = yaml.load(f)

        if config['run']['simdir'][-1] != '/':
            config['run']['simdir'] += '/'
        if config['run']['srcdir'][-1] != '/':
            config['run']['srcdir'] += '/'

        return config

    def saveConfig(self, path):
        """
        """

        import yaml

        with open(path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    @property
    def azbins(self):

        """Creates increments of azimuth angle to be sampled by individual
        source files.

        """
        
        return np.linspace(self.config['run']['azmin'],
                           self.config['run']['azmax'],
                           self.config['run']['aznumbins'])
    
    @property
    def zebins(self):

        """Creates increments of zenith angle to be sampled by individual
        source files.

        """

        return np.linspace(self.config['run']['zemin'],
                           self.config['run']['zemax'],
                           self.config['run']['zenumbins'])

    @property
    def ebins(self):

        """Creates increments of energy (keV) to be sampled by individual
        source files.

        """

        return np.logspace(np.log10(self.config['run']['emin']),
                           np.log10(self.config['run']['emax']),
                           self.config['run']['enumbins'])

    def createSourceFiles(self, dir=''):

        """Creates a source file from a configurator object with a specific
        angle and energy

        Parameters
        ----------

        dir : string 
        the desired directory of the output

        Returns
        ----------
        
        In your directory all of the source files with specific angles
        and energies.

        """
        
        from utils import getFilenameFromDetails
        
        for ze, az, energy in [(ze, az, energy)
                               for ze in self.zebins
                               for az in self.azbins
                               for energy in self.ebins]:
            srcstr = createSourceString(self.config, energy, ze, az)

            basename = self.config['run']['basename']
            fname = getFilenameFromDetails({'base': basename,
                                            'keV': energy,
                                            'ze': ze,
                                            'az': az})
            if dir:
                fname = dir + '/' + fname + '.source'
            else:
                fname = self.config['run']['srcdir'] + '/' + fname + '.source'

            f = open(path.expandvars(fname), 'w')
            f.write(srcstr)
            f.close()

