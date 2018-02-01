#!/usr/bin/env python

import os


def setPath(desiredPath = "", desiredPathName = 'BURSTCUBE'):

    '''Checks for desiredPathName path.  Returns 0 if ok, 1 if bad.'''

    if desiredPath:
        if '~' in desiredPath:
            os.environ['desiredPathName'] = os.path.expanduser(desiredPath)
            return 0
        else:
            os.environ['desiredPathName'] = desiredPath
            return 0
    elif not (desiredPathName in os.environ):
        print('Set or provide ' + desiredPathName)
        return 1
    else:
        return 0


def getFilenameFromDetails(details):

    """Takes a dictionary of details and makes a machine readible filename
    out of it.  Angle comes in radians."""

    import numpy as np

    filename = "{}_{:.3f}keV_Cos{:.3f}".format(details['base'],
                                               details['keV'],
                                               details['theta'])

    return filename


def getDetailsFromFilename(filename):

    '''Function to get the energy and angle from a filename.
    Really should be meta data.'''

    details = {}
    info = filename.split('_')

    details['base'] = info[0]

    details['keV'] = float(info[1][:-3])

    angle = info[2].split('.')
    details['Cos'] = float("{}.{}".format(angle[0][3:], angle[1]))

    return details

#def getTriggerProbability(htsimfile, test=False):
#
#    """Takes a single simFile (from bcSim.simFiles(config.yaml)) and 
#    returns the probability of hitting in each detector
#
#    Parameters
#    ----------
#    self : simFile 
#    test : run a quick test over a limited number of events (20)
#    
#    Returns
#    ----------
#    prob_det_info : 1x6 numpy array containing information about the energy, angles and probability of 
#    hitting a given detector
#    
#    """
#
#    det_vol = 0 
#    det_vol1 = 0
#    det_vol2 = 0
#    det_vol3 = 0
#
#    energy = htsimfile.energy
#    theta = htsimfile.theta
#    hits = htsimfile.getHits()
#
#    actual = 0
#    if test: dotest=20
#    else: dotest=len(hits)
#
#    print "analyzing", len(hits), "events"
#
#    for i in range(0,dotest):
#        actual+=1
#        if hits[i][0]>0:
#            if hits[i][1]>0: det_vol1+=1
#            else: det_vol3+=1
#        else:
#            if hits[i][1]>0: det_vol2+=1
#            else: det_vol+=1
#                     
#    prob_det_info=[energy, theta, det_vol1/float(actual), det_vol3/float(actual), det_vol/float(actual), det_vol2/float(actual)]
#
#    return prob_det_info

def getTriggerProbability(htsimfile, num_det=4, test=False):

    """Takes a single simFile (from bcSim.simFiles(config.yaml)) and 
    returns the probability of hitting in each detector

    Parameters
    ----------
    self : simFile 
    test : run a quick test over a limited number of events (20)
    
    Returns
    ----------
    prob_det_info : 1x6 numpy array containing information about the energy, angles and probability of 
    hitting a given detector
    
    """

    import numpy as np

    det_vol=np.zeros(num_det)

    print "test", det_vol

    energy = htsimfile.energy
    theta = htsimfile.theta
    hits = htsimfile.getHits()

    actual = 1
    if test: dotest=20
    else: dotest=len(hits)

    print "analyzing", len(hits), "events"

    for key, value in htsimfile.logDict.items():
        print hits[key], value[1]
        for i in range(num_det):
            if str(i) in value[1]:
                print i, value
                     
    prob_det_info=[energy, theta, det_vol1/float(actual), det_vol3/float(actual), det_vol/float(actual), det_vol2/float(actual)]

    return prob_det_info
    

def getAllTriggerProbability(filelist, num_detectors=4, test=False):

    """Takes a bunch of simFiles (from bcSim.simFiles(config.yaml)) and 
    returns the probability of hitting in each detector

    Parameters
    ----------
    self : simFiles 
    test : run a quick test over a limited number of files (20)
    
    Returns
    ----------
    det_prob : numpy array containing information from all the files about the energy, angles and probability of 
    hitting a given detector
    
    """

    import numpy as np
    htsims=filelist.sims

    det_prob = np.empty(len(htsims),
                        dtype={'names': ['energy', 'theta', 'prob_det_vol1',
                                         'prob_det_vol3', 'prob_det_vol', 'prob_det_vol2'],
                               'formats': ['float32', 'float32',
                                           'float32', 'float32', 'float32', 'float32']})

    if test: dotest=1
    else: dotest=len(htsims)

    print "Analyzing", len(htsims), "files"

    for j in range(dotest):
        holder=getTriggerProbability(htsims[j], num_det=num_detectors, test=test)
        det_prob[j]= np.array([tuple(holder)], dtype=det_prob.dtype)


    return det_prob
        
    
