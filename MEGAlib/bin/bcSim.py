#!/usr/bin/env python

class bcSim:

    def __init__(self, simFile, sourceFile):

        '''Stuff'''

        self.simFile = simFile
        self.srcFile = sourceFile

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
                        lineContents = line.split()
                        if len(lineContents) > 1:
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
