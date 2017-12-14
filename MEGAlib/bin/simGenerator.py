#!/usr/bin/env python

import numpy as np
from os import path


def createSourceString(config, energy, angle):

    '''Creates a source file from a configurator object and a specific
    angle and energy.'''

    from utils import getFilenameFromDetails

    fname = getFilenameFromDetails({'base': config['run']['basename'],
                                    'keV': energy,
                                    'Cos': angle})

    srcstr = ''

    for key in config['general']:
        srcstr += str(key) + ' ' + str(config['general'][key])
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
    srcstr += str(np.round(np.rad2deg(angle), decimals=2)) + ' 0'
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

        import yaml

        with open(path, 'r') as f:
            config = yaml.load(f)

        return config

    @property
    def costhetabins(self):
        return np.linspace(self.config['run']['costhetamin'],
                           self.config['run']['costhetamax'],
                           self.config['run']['costhetanumbins'])

    @property
    def thetabins(self):
        return np.round(np.rad2deg(self.costhetabins), decimals=2)
    
    @property
    def ebins(self):
        return np.logspace(np.log10(self.config['run']['emin']),
                           np.log10(self.config['run']['emax']),
                           self.config['run']['enumbins'])

    def createSourceFiles(self, dir=''):

        from utils import getFilenameFromDetails
        
        for angle, energy in [(angle, energy)
                              for angle in self.costhetabins
                              for energy in self.ebins]:
            srcstr = createSourceString(self.config, energy, angle)

            basename = self.config['run']['basename']
            fname = getFilenameFromDetails({'base': basename,
                                            'keV': energy,
                                            'Cos': angle})
            if dir:
                fname = dir + '/' + fname + '.source'
            else:
                fname = self.config['run']['srcdir'] + '/' + fname + '.source'

            fname = path.expandvars(fname)
            f = open(fname, 'w')
            f.write(srcstr)
            f.close()
