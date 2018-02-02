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
