#!/usr/bin/env python

import os


def setPath(desiredPath="", desiredPathName='BURSTCUBE'):

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

    filename = "{}_{:.3f}keV_{:.2f}theta".format(details['base'],
                                                 details['keV'],
                                                 details['theta'])

    return filename


def getDetailsFromFilename(filename):

    '''Function to get the energy and angle from a filename.
    Really should be meta data.

    This function will be deprecated at some point since the energy
    and angle are in the simFile object now.

    '''

    import re

    details = {}
    info = filename.split('_')

    details['base'] = info[0]
    details['keV'] = re.search('(.*)keV', info[1]).group(1)
    details['theta'] = re.search('(.*)theta', info[2]).group(1)

    return details


def getTriggerProbability(htsimfile, num_det=4, test=False):

    """Takes a single simFile (from bcSim.simFiles(config.yaml)) and
    returns the probability of hitting in each detector

    Parameters
    ----------
    self : simFile

    test : run a quick test over a limited number of events (20)
    
    Returns
    ----------
    
    prob_det_info : 1x6 numpy array containing information about the
    energy, angles and probability of hitting a given detector

    """

    import numpy as np
    from math import sqrt

    det_vol = np.zeros(num_det)

    energy = htsimfile.energy
    theta = htsimfile.theta
    hits = htsimfile.getHits()

    if test:
        dotest = 20
    else:
        dotest = len(hits)

    print("analyzing", len(hits), "events")
    stat_err = len(hits)

    for key, value in htsimfile.logDict.items():
        for i in range(num_det):
            if str(i) in value[1]:
                det_vol[i] += 1
            elif i == 0:
                if '_' not in value[1]:
                    det_vol[0] += 1

    prob_det_info = [energy, theta]
    prob_det_info = np.append(prob_det_info, sqrt(len(hits))/float(len(hits)))

    for i in range(num_det):
        prob_det_info = np.append(prob_det_info, det_vol[i]/float(len(hits)))

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
    det_prob : numpy array 
        Contains information from all the files about the energy,
        angles and probability of hitting a given detector

    """

    import numpy as np
    htsims = filelist.sims

    names = ['energy', 'theta', 'stat_err',  'prob_det_vol']
    formats = ['float32', 'float32', 'float32', 'float32']

    for i in range(num_detectors-1):
        names = np.append(names, 'prob_det_vol%i' % (i+1))
        formats = np.append(formats, 'float32')

    print(names)
    print(formats)

    det_prob = np.empty(len(htsims),
                        dtype={'names': names,
                               'formats': formats})

    if test:
        dotest = 1
    else:
        dotest = len(htsims)

    print("Analyzing", len(htsims), "files")

    for j in range(dotest):
        holder = getTriggerProbability(htsims[j],
                                       num_det=num_detectors, test=test)
        det_prob[j] = np.array([tuple(holder)], dtype=det_prob.dtype)

    return det_prob
