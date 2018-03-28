#!/usr/bin/env python

import numpy as np
from utils import setPath
from simGenerator import configurator


class simFiles:

    def __init__(self, config_file):

        """Object for a multiple simulations over energy and angle."""

        if setPath():
            exit()

        self.conf = configurator(config_file)
        self.sims = self.loadFiles()

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

        for ze, az, energy in [(ze, az, energy)
                               for ze in self.conf.zebins
                               for az in self.conf.azbins
                               for energy in self.conf.ebins]:
            fname = getFilenameFromDetails({'base': basename,
                                            'keV': energy,
                                            'ze': ze,
                                            'az': az})
            sf = simFile(self.conf.config['run']['simdir']
                         + '/'+fname+'.inc1.id1.sim',
                         self.conf.config['run']['srcdir']
                         + '/'+fname+'.source',
                         self.conf.config['run']['simdir']
                         + '/'+fname+'.stdout.gz')
            sfs.append(sf)

        return sfs

    def applyEres(self):
        """Applies the energy resolution to the deposited energy in each sim
        file and returns a flattened array for plotting.

        Returns
        ----------
            null : numpy array
            numpy array that contains all of the events with eres applied.

        """

        return np.array([sf.ED_res for sf in self.sims]).flatten()
    
    def calculateAeff(self, useEres=False, sigma=2.0):

        """Calculates effective area from the information contained within the
        .sim files.

        Parameters
        ----------
        self : null

        useEres : boolean 
          Switch to use the energy resolution in the
          calculation.

        sigma : float
          Width of energy cut in sigma.  Default is 2.0.


        Returns
        ----------
        aeffs : array
            Numpy array containing effective area of detector.

        """

        aeffs = np.zeros(len(self.sims),
                         dtype={'names': ['az', 'ze', 'keV', 'aeff',
                                          'aeff_eres', 'aeff_eres_modfrac'],
                                'formats': ['float32', 'float32', 'float32',
                                            'float32', 'float32', 'float32']})

        if useEres:
            e = self.conf.config['detector']['resolution']['energy']
            w = self.conf.config['detector']['resolution']['width']
            e_interp = np.array([sf.energy for sf in self.sims])
            res_interp = np.interp(e_interp, e, w)
        else:
            res_interp = np.zeros(len(self.sims))
        
        for i, sf in enumerate(self.sims):
            frac, mod_frac = sf.passEres()
            aeff = sf.calculateAeff(useEres, res_interp[i]*sigma)
            aeffs[i] = (sf.azimuth,
                        sf.zenith,
                        sf.energy,
                        aeff, aeff*frac, aeff*mod_frac)

        return aeffs

    def getAllTriggerProbability(self, num_detectors=4, test=False):

        """Returns the probabability of hitting each detector in each simulation.

        Parameters
        ----------
            num_detectors : int
                Number of detectors in the simulation

            test : boolean
                run a quick test over a limited number of files (20)
    
        Returns
        ----------
            det_prob : numpy array
                Contains information from all the files about the energy,
                angles and probability of hitting a given detector
        """

        names = ['energy', 'az', 'ze', 'stat_err',  'prob_det_vol']
        formats = ['float32', 'float32', 'float32', 'float32', 'float32']

        for i in range(num_detectors-1):
            names = np.append(names, 'prob_det_vol%i' % (i+1))
            formats = np.append(formats, 'float32')

        print(names)
        print(formats)

        det_prob = np.empty(len(self.sims),
                            dtype={'names': names,
                                   'formats': formats})

        if test:
            dotest = 1
        else:
            dotest = len(self.sims)

        print("Analyzing", len(self.sims), "files")

        for j in range(dotest):
            holder = self.sims[j].getTriggerProbability(num_det=num_detectors,
                                                        test=test)
            det_prob[j] = np.array([tuple(holder)], dtype=det_prob.dtype)

        return det_prob
    

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
        self.eres = self.getEresFromFile(self.geoDict['Include'][1])
        
        if logFile:
            self.logDict = self.logToDict(self.logFile)
        else:
            print("Log file not provided.  Not loading.")

    @property
    def energy(self):
        return float(self.srcDict['One.Spectrum'][0][1])

    @property
    def zenith(self):
        return float(self.srcDict['One.Beam'][0][1])

    @property
    def azimuth(self):
        return float(self.srcDict['One.Beam'][0][2])

    @property
    def ED_res(self):
        try:
            self._ED_res
        except AttributeError:
            print('Applying Eres on {}'.format(self.simFile))
            self._ED_res = self._applyEres(self.eres['energy'],
                                           self.eres['sigma'])

        return(self._ED_res)
    
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

    def getEresFromFile(self, filename, commentString='//'):

        from os import path
        
        eres_lines = []
        filename = path.expandvars(filename)
        with open(filename) as f:
            for line in f:
                if commentString not in line:
                    if 'EnergyResolution' in line:
                        eres_lines.append(line)

        eres = np.zeros(len(eres_lines),
                        dtype={'names': ['energy', 'sigma'],
                               'formats': ['float32', 'float32']})
                        
        for i, res in enumerate(eres_lines):
            res_split = res.split()
            eres[i] = (res_split[-2], res_split[-1])

        return eres

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
        print('Azimuth: ' + str(self.azimuth))
        print('Zenith: ' + str(self.zenith))
        print('Energy: ' + str(self.energy))
        
    def calculateAeff(self, useEres=False, width=0.):
        """Calculates effective area of sim file.

        Parameters
        ----------
        useEres : Boolean
           Switch to either use the energy resolution in the
           calculation or not.  If you don't use this it assumes all
           of the events are good.

        width: Float
           The energy width that is used to reject events in the selection.

        Returns
        ----------
        Aeff : Float
           The effective area.

        """
        
        from math import pi

        r_sphere = float(self.geoDict['SurroundingSphere'][0][0])
        generated_particles = int(self.simDict['TS'][0])

        if useEres:
            triggers = np.where((self.ED_res >= self.energy - width)
                                & (self.ED_res <= self.energy + width))
            triggers = len(triggers[0])
        else:
            triggers = int(self.srcDict['FFPS.NTriggers'][0])

        return r_sphere**2*pi*triggers/generated_particles

    def _applyEres(self, energies, widths):
        
        """Takes the energy deposited in the detector (ED) and adds a noise
        factor on an event by event basis based on the energy resolution of
        the detector.  Does a linear interpolation between the varous energy
        measurements.  Assumes gaussian noise.

        To-do:
          * Need to make the interpolation non-linear
            (functional)
          * Need to make sure it goes above and below the
            lowest (highest) value measurements.


        Parameters
        ----------
        energies : list
           List of energies in keV at which the energy resolution
           (width) is calculated.

        widths: list
           List of energy widths (resolution) in keV.

        Returns
        ----------
        ED + noise : numpy array
          An array of energy values that have been corrected for the
          energy resolution.

        """

        ED = np.array([float(ed) for ed in self.simDict['ED']])
        e_interp = list(set(ED))
        res_interp = np.interp(e_interp, energies, widths)
        indexes = [e_interp.index(ed) for ed in ED]
        noise = [np.random.normal(0, res_interp[i], 1)[0] for i in indexes]
        return ED + noise

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

    def getTriggerProbability(self, num_det=4, test=False):

        """Takes a single simFile (from bcSim.simFiles(config.yaml)) and
        returns the probability of hitting in each detector

        Parameters
        ----------
        num_det : integer
            Number of detectors to get triggers for.

        test : boolean
            Run a quick test over a limited number of events (20)
    
        Returns
        ----------
        prob_det_info : numpy array
            Array is (energy, az, ze, error, prob1, prob2, ...)

        """

        from math import sqrt

        det_vol = np.zeros(num_det)

        hits = self.getHits()

        if test:
            dotest = 20
        else:
            dotest = len(hits)

        print("analyzing", len(hits), "events")
        # stat_err = len(hits)

        for key, value in self.logDict.items():
            for i in range(num_det):
                if str(i) in value[1]:
                    det_vol[i] += 1
                elif i == 0:
                    if '_' not in value[1]:
                        det_vol[0] += 1

        prob_det_info = [self.energy, self.azimuth, self.zenith]
        prob_det_info = np.append(prob_det_info,
                                  sqrt(len(hits))/float(len(hits)))

        for i in range(num_det):
            prob_det_info = np.append(prob_det_info,
                                      det_vol[i]/float(len(hits)))

        return prob_det_info
