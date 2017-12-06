#!/usr/bin/env python

class bcSim:

    def __init__(self, simFile, sourceFile):

        '''Stuff'''

        self.simDict = self.fileToDict(simFile,'#','TB')
        self.srcDict = self.fileToDict(sourceFile,'#',None)
        self.geoDict = self.fileToDict(self.simDict['Geometry'][0],'//',None)


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



