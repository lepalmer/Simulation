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
                         + '/'+fname+'.source',
                         self.conf.config['run']['simdir']
                         + '/'+fname+'.stdout.gz')
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
            aeffs[i] = (sf.srcDict['One.Beam'][0][1],
                        sf.srcDict['One.Spectrum'][0][1],
                        aeff, aeff*frac, aeff*mod_frac)

        return aeffs


class simFile:

    def __init__(self, simFile, sourceFile, logFile=''):

        """Object for a single megalib simulation.  The main attributes are
        dictionaries associated with the simulation file, the source file, and
        the geometry file (`simDict`, `srcDict`, `geoDict`, and `logDict`.).

        Parameters
        ----------
        simFile : string
           simulation file output from Cosima

        sourceFile: sting
           config file used as input to Cosima

        logFile: string
           stdout from Cosima.  Optional. 

        Returns
        ----------
        simFile : simFile Object

        """
        
        self.simFile = simFile
        self.srcFile = sourceFile
        self.logFile = logFile
        
        if setPath():
            exit()

        print("Loading " + self.simFile)
        self.simDict = self.fileToDict(simFile, '#', None)
        self.srcDict = self.fileToDict(sourceFile, '#', None)
        self.geoDict = self.fileToDict(self.srcDict['Geometry'][0],
                                       '//', None)
        if logFile:
            self.logDict = self.logToDict(self.logFile)
        else:
            print("Log file not provided.  Not loading.")

    @property
    def energy(self):
        return float(self.srcDict['One.Spectrum'][0][1])

    @property
    def theta(self):
        return float(self.srcDict['One.Beam'][0][1])

    def fileToDict(self, filename, commentString='#', termString=None):

        from os import path

        '''Turn a MEGAlib file into a a python dictionary'''
        megaDict = {}
        filename = path.expandvars(filename)
        with open(filename) as f:
                for line in f:
                    if commentString not in line:
                        if ';' in line:
                            contents = line.split(';')
                        else:
                            contents = line.split()
                        if len(contents) > 1:
                            if contents[0] in megaDict:
                                if ';' in line:
                                    megaDict[contents[0]].append(
                                        contents[1:])
                                else:
                                    megaDict[contents[0]].append(
                                        contents[1])
                            else:
                                if len(contents[1:]) > 1:
                                    megaDict[contents[0]] = [contents[1:]]
                                else:
                                    megaDict[contents[0]] = contents[1:]
                    if termString is not None:
                        if termString in line:
                            return megaDict
        return megaDict

    def logToDict(self, filename):

        """Reads a gzipped log file and populates a dictionary with information about
        the events.  Returns this dictionary.

        Parameters
        ----------
        filename: string or byte like object
            Name of log file to read.

        Returns
        ---------
        eventDict : dictionary
            
        Dictionary with the key being the trigger number (int).  Each
        value is a tuple of the event number (int) and the detector
        (str) that was hit.

        """
        
        import gzip
        import re
        from os import path

        filename = path.expandvars(filename)

        # Try to read the gzip and fallback to normal if it doesn't exist.
        try:
            f = gzip.open(filename, 'rb')
        except FileNotFoundError:
            filename = filename[:-3]
            f = open(filename, 'rb')
        file_content = f.read()
        f.close()

        eventDict = {}

        lines = file_content.splitlines()
        for i, line in enumerate(lines):
            if 'Storing event' in str(line):
                evtnums = [int(s) for s in str(line).split() if s.isdigit()]
                detname = re.search('\"(.*)\"', str(lines[i-1]))
                eventDict[evtnums[0]] = (evtnums[1], detname.group(1))

        return eventDict
    
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

        dt = np.dtype([('x_pos', np.float64),
                       ('y_pos', np.float64),
                       ('z_pos', np.float64),
                       ('E', np.float64),
                       ('tobs', np.float64)])

        # Get all the rest of the events
        events = [np.array(evt, dtype=np.float64)
                  for evt in self.simDict[IDstr]]

        hits = np.zeros((len(events),), dtype=dt)

        for i, evt in enumerate(events):
            hits[i] = evt

        return hits

    def printDetails(self):
        """Prints the general information about specific sim files. 
        """
        print('Sim File: ' + self.simFile)
        print('Source File: ' + self.srcFile)
        print('Geometry File: ' + self.srcDict['Geometry'][0][0])
        print('Surrounding Sphere: ' + self.geoDict['SurroundingSphere'][0][0])
        print('Triggers: ' + self.srcDict['FFPS.NTriggers'][0])
        print('Generated Particles: ' + self.simDict['TS'][0])
        print('Theta: ' + str(self.theta))
        print('Energy: ' + str(self.energy))

    def calculateAeff(self):
        """Calculates effective area of sim file. 
        """
        
        from math import pi

        r_sphere = float(self.geoDict['SurroundingSphere'][0][0])
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
