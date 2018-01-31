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
                                               np.cos(np.deg2rad(
                                                   details['theta'])))

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

def getTriggerProbability(htsimfile, test=False):

    '''Takes a single simFile (from bcSim.simFiles(config.yaml)) and 
    returns the probability of hitting in each detector '''

    det_vol = 0 
    det_vol1 = 0
    det_vol2 = 0
    det_vol3 = 0

    actual = 0
    if test: dotest=20
    else: dotest=len(htsims)

    siminfo=htsimfile.simDict['HTsim 4']
    energy = htsimfile.energy
    theta = htsimfile.theta
    print energy, theta
    
    for i in range(0,dotest):
        if isinstance(siminfo[i],list): 
            actual+=1
            if float(siminfo[i][0])> 0.:
                if float(siminfo[i][1])>0.:
                    det_vol1+=1
                else:
                    det_vol3+=1
            else:
                if float(siminfo[i][1])>0.:
                    det_vol2+=1
                else:
                    det_vol+=1
                     
    prob_det_info=[energy, theta, det_vol1/float(actual), det_vol3/float(actual), det_vol/float(actual), det_vol2/float(actual)]

    print prob_det_info

    return prob_det_info
    

def getAllTriggerProbability(filelist, test=False):
    
    htsims=filelist.sims
    
    if test: dotest=1
    else: dotest=len(htsims)

    print "Analyzing", len(htsims), "files"

    for j in range(dotest):
        det_prob = getTriggerProbability(htsims[j], test=test)


    return det_prob[2:4]
        
    
