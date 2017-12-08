#!/usr/bin/env python

import numpy as np

class bcSim:

    def __init__(self, simFile, sourceFile):

        '''Stuff'''

        self.simFile = simFile
        self.srcFile = sourceFile

        print("Loading " + self.simFile)
        self.simDict = self.fileToDict(simFile,'#',None)
        self.srcDict = self.fileToDict(sourceFile,'#',None)
        self.geoDict = self.fileToDict(self.srcDict['Geometry'][0],'//',None)

    def fileToDict(self, filename, commentString = '#', termString = None):

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
                                    megaDict[lineContents[0]].append(lineContents[1:])
                                else:
                                    megaDict[lineContents[0]].append(lineContents[1])
                            else:
                                megaDict[lineContents[0]] = lineContents[1:]
                    if termString is not None:
                        if termString in line:
                            return megaDict
        return megaDict

    def printDetails(self):
        
        print('Sim File: ' + self.simFile)
        print('Source File: ' + self.srcFile)
        print('Geometry File: ' + self.srcDict['Geometry'][0])
        print('Surrounding Sphere: ' + self.geoDict['SurroundingSphere'][0])
        print('Triggers: ' + self.srcDict['FFPS.NTriggers'][0])
        print('Generated Particles: ' + self.simDict['TS'][0])

    def calculateAeff(self):
        
        from math import pi

        r_sphere = float(self.geoDict['SurroundingSphere'][0])
        triggers = int(self.srcDict['FFPS.NTriggers'][0])
        generated_particles = int(self.simDict['TS'][0])

        return r_sphere**2*pi*triggers/generated_particles

    def passEres(self, alpha = 2.57, escape = 30.0):

        '''Calculates the fraction of events that are good (fully absorbed)
        and those that escape.  The default escape photon energy is
        for CsI (30.0 keV).  An alpha of 2.57 is based on 10% energy
        resolution at 662 keV with 1/sqrt(E) scaling.'''

        ed = np.array(self.simDict['ED']).astype(np.float)
        ec = np.array(self.simDict['EC']).astype(np.float)
        ns = np.array(self.simDict['NS']).astype(np.float)
        
        tot = ed + ec + ns
        ediff = tot - ed
        ediff2 = ediff - escape
        # Sigma = FWHM (or eres)/2.35.  Returns 0 if ed is 0
        sigma = np.where(ed !=0, ed*alpha/np.sqrt(ed)/2.35, 0)
        good = np.sum(np.fabs(ediff) < sigma)
        mod = np.sum(np.fabs(ediff2) < sigma)

        frac = float(good)/float(len(ed))
        mod_frac = (float(mod)+float(good))/float(len(ed))

        return frac,mod_frac
