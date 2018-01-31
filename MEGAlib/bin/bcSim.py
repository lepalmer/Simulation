#!/usr/bin/env python

import numpy as np
from utils import setPath
from simGenerator import configurator  #requires simGenerator


class simFiles:

    def __init__(self, config_file):  #name of the function that python uses to construct 

        """Object for a multiple simulations over energy and angle."""

        if setPath():
            exit()

        self.conf = configurator(config_file)
        self.sims = self.loadFiles()  #this is defined later down? 

    def loadFiles(self):
        """

        Parameters
        ----------
        self : null

        Returns
        ----------
        sfs : array
            numpy array containing information about each sim file. 

        """
        from utils import getFilenameFromDetails

        basename = self.conf.config['run']['basename']

        sfs = []

        for angle, energy in [(angle, energy)
                              for angle in self.conf.costhetabins
                              for energy in self.conf.ebins]:
            fname = getFilenameFromDetails({'base': basename,
                                            'keV': energy,
                                            'theta': angle})
            sf = simFile(self.conf.config['run']['simdir']
                         + '/'+fname+'.inc1.id1.sim',
                         self.conf.config['run']['srcdir']
                         + '/'+fname+'.source')
            sfs.append(sf)

        return sfs

    def calculateAeff(self):
        """Calculates effective area from the information contained within the .sim files. 

        Parameters
        ----------
        self : null

        Returns
        ----------
        aeffs : array
            Numpy array containing effective area of detector. 
    
        """

        aeffs = np.zeros(len(self.sims),
                         dtype={'names': ['theta', 'keV', 'aeff',
                                          'aeff_eres', 'aeff_eres_modfrac'],
                                'formats': ['float32', 'float32',
                                            'float32', 'float32', 'float32']})

        for i, sf in enumerate(self.sims):
            frac, mod_frac = sf.passEres()
            aeff = sf.calculateAeff()
            aeffs[i] = (sf.srcDict['One.Beam'][1],
                        sf.srcDict['One.Spectrum'][1],
                        aeff, aeff*frac, aeff*mod_frac)

        return aeffs


class simFile:

    def __init__(self, simFile, sourceFile):

        """Object for a single megalib simulation.  The main attributes are
        dictionaries associated with the simulation file, the source file, and
        the geometry file (`simDict`, `srcDict`, and `geoDict`.

        Parameters
        ----------
        simFile : string
           simulation file output from Cosima

        sourceFile: sting
           config file used as input to Cosima

        Returns
        ----------
        simFile : simFile Object

        """
        
        self.simFile = simFile
        self.srcFile = sourceFile

        if setPath():
            exit()

        print("Loading " + self.simFile)
        self.simDict = self.fileToDict(simFile, '#', None)
        self.srcDict = self.fileToDict(sourceFile, '#', None)
        self.geoDict = self.fileToDict(self.srcDict['Geometry'][0], '//', None)

    @property
    def energy(self):
        return float(self.srcDict['One.Spectrum'][1])

    @property
    def theta(self):
        return float(self.srcDict['One.Beam'][1])

    def fileToDict(self, filename, commentString='#', termString=None):

        from os import path

        '''Turn a MEGAlib file into a a python dictionary'''
        megaDict = {}
        filename = path.expandvars(filename)
        with open(filename) as f:
                for line in f:
                    if commentString not in line:
                        if ';' in line:
                            lineContents = line.split(';')
                        else:
                            lineContents = line.split()
                        if len(lineContents) > 1:
                            if lineContents[0] in megaDict:
                                if ';' in line:
                                    megaDict[lineContents[0]].append(
                                        lineContents[1:])
                                else:
                                    megaDict[lineContents[0]].append(
                                        lineContents[1])
                            else:
                                megaDict[lineContents[0]] = lineContents[1:]
                    if termString is not None:
                        if termString in line:
                            return megaDict
        return megaDict

    def getHits(self, detID=4):

        """Get the hit details of all of the events in the sim file.  Ignores
        the a,b,and c details.

        Parameters
        ----------
        detID : int
           Detector ID (usually 4)


        Returns
        ----------
        hits : numpy structured array
            Five column Structured array.  Columns are all floats and
            are `x_pos`, `y_pos`, `z_pos`, `E`, and `tobs`.

        """

        IDstr = 'HTsim {}'.format(detID)

        # Ugly hack to get first event
        first_evt = [x for x in self.simDict[IDstr] if type(x) is not list]

        dt = np.dtype([('x_pos', np.float64),
                       ('y_pos', np.float64),
                       ('z_pos', np.float64),
                       ('E', np.float64),
                       ('tobs', np.float64)])

        # Get all the rest of the events
        events = [np.array(evt[:5], dtype=np.float64)
                  for evt in self.simDict['HTsim 4'][len(first_evt):]]

        hits = np.zeros((len(events)+1,), dtype=dt)

        # First event in a numpy array.  Ignore a,b,c.
        hits[0] = np.array(first_evt[:5], dtype=np.float64)

        for i, evt in enumerate(events):
            hits[i+1] = evt

        return hits

    def printDetails(self):
        """Prints the general information about specific sim files. 
        """
        print('Sim File: ' + self.simFile)
        print('Source File: ' + self.srcFile)
        print('Geometry File: ' + self.srcDict['Geometry'][0])
        print('Surrounding Sphere: ' + self.geoDict['SurroundingSphere'][0])
        print('Triggers: ' + self.srcDict['FFPS.NTriggers'][0])
        print('Generated Particles: ' + self.simDict['TS'][0])
        print('Theta: ' + str(self.theta))
        print('Energy: ' + str(self.energy))

    def calculateAeff(self):
        """Calculates effective area of sim file. 
        """
        
        from math import pi

        r_sphere = float(self.geoDict['SurroundingSphere'][0])
        triggers = int(self.srcDict['FFPS.NTriggers'][0])
        generated_particles = int(self.simDict['TS'][0])

        return r_sphere**2*pi*triggers/generated_particles

    def passEres(self, alpha=2.57, escape=30.0):

        """Calculates the fraction of events that are good (fully absorbed)
        and those that escape.  The default escape photon energy is
        for CsI (30.0 keV).  An alpha of 2.57 is based on 10% energy
        resolution at 662 keV with 1/sqrt(E) scaling.  Sigma is
        calculated as the FWHM or eres diveded by 2.35.

        Returns
        ---------- 
        frac : float

        mod_frac : float
        
        """

        ed = np.array(self.simDict['ED']).astype(np.float)
        ec = np.array(self.simDict['EC']).astype(np.float)
        ns = np.array(self.simDict['NS']).astype(np.float)
        
        tot = ed + ec + ns
        ediff = tot - ed
        ediff2 = ediff - escape
        sigma = np.where(ed != 0, ed*alpha/np.sqrt(ed)/2.35, 0)
        good = np.sum(np.fabs(ediff) < sigma)
        mod = np.sum(np.fabs(ediff2) < sigma)

        frac = float(good)/float(len(ed))
        mod_frac = (float(mod)+float(good))/float(len(ed))

        return frac, mod_frac
