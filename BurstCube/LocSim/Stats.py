#!/usr/bin/env python

import numpy as np

def calcNorms(real_counts, training_counts):

   return np.array([[np.linalg.norm(rec[0] - test[0],2) for rec in training_counts] for test in real_counts])

def addErrors(real_counts, training_counts):

   return np.round(np.sqrt([[test + rec for rec in training_counts[:,1]**2] 
                                    for test in real_counts[:,1]**2])).astype('int32')

def calcNormsWithError(real_counts, training_counts, real_counts_with_error):

   norms_errp = np.array([[np.linalg.norm(rec[0] - (test[0] + real_counts_with_error[idx,jdx]),2) 
                        for jdx,rec in enumerate(training_counts)] 
                           for idx,test in enumerate(real_counts)])


   norms_errm = np.array([[np.linalg.norm(rec[0] - (test[0] - real_counts_with_error[idx,jdx]),2) 
                        for jdx,rec in enumerate(training_counts)] 
                           for idx,test in enumerate(real_counts)])


   return norms_errp, norms_errm

def distance(training_grbs,real_grbs,mins):

	import ephem as eph

	return [eph.separation(grb.eph,training_grbs[mins[idx]].eph)*180./np.pi for idx,grb in enumerate(real_grbs)]   

def halfway(grbs):
    return [(np.average([grb[idx].eph._ra for idx in np.arange(len(grb))]),
             np.average([grb[idx].eph._dec for idx in np.arange(len(grb))])) for grb in grbs]

def distance2(positions, real_grbs):

	import ephem as eph

	return [eph.separation((position[0],position[1]),(real_grbs[idx].eph._ra,real_grbs[idx].eph._dec))*180/np.pi 
				for idx,position in enumerate(positions)]




