
import numpy as np
import matplotlib.pyplot as plt
import math as mth
import random as rand
import statistics as s
import healpy as hp


def length(v):
    """
    Finds the length of a vector
    
    Parameters
    ----------
    
    v : array
        numpy array representative of the vector you want to find the magnitude of. 
    
    Returns
    -------
    
    magv : float
        magnitude of v.
    """
    magv = mth.sqrt(np.dot(v, v))
    return magv

def angle(v1, v2):
    """"
    Finds the angle between 2 vectors
    
    Parameters
    ----------
    
    v1 : array
    v2 : array
        The arrays representing the vectors who's angle is to be calculated.
        
    Returns
    -------
    
    ang : float
        Angle between the 2 vectors. 
        
    """

    ang = np.arccos(np.dot(v1, v2) / (length(v1) * length(v2)))
    return ang

def findAngles(v1s, v2s):
    dot = np.einsum('ijk,ijk->ij',[v1s,v1s,v2s],[v2s,v1s,v2s])
    return np.arccos(dot[0,:]/(np.sqrt(dot[1,:])*np.sqrt(dot[2,:])))


def chiresponse(A):
    """
    Meant to imitate the actual response of a scintillator.
    Inputs 2 vectors, and responds with a cos^x dependence.
    """
    #meant to imitate the response of the detectors for effective area vs. angle, found to be around .77
 #   print(length(A),length(B))
#if cosine is negative, 

    mask = A > np.pi/2.

    A[mask] = 0
    A[~mask] = pow(abs(np.cos(A[~mask])),0.76)
    
    
    return A

def response(A):
    """
    Meant to imitate the actual response of a scintillator.
    Inputs 2 vectors, and responds with a cos^x dependence.
    """
    #meant to imitate the response of the detectors for effective area vs. angle, found to be around .77
 #   print(length(A),length(B))
#if cosine is negative, 

    R = pow(abs(np.cos(A)),0.76)
    
    
    return R         

def bilbo(theta):
    #getting the weighted average of the area of various parts along the unit sphere. Current simulation targets azimuth many more times than the rest of the sphere, so have to account for this being in a significantly smaller area
    #keep in mind this 5 has to do with the # of test theta, 5 works best since it is splits the rings perfectly between evenly spaced points of 10 (used)
    if theta==0: 
        #have to treat this slightly differently
        A=abs(2*np.pi*(np.cos(theta)-np.cos(np.deg2rad(5)))) 
    else:
        A=abs(2*np.pi*(np.cos(theta+np.deg2rad(5))-np.cos(theta-np.deg2rad(5))))
    return A

def chimaker(chiterms,Ndets): 
    	
    	#Unfortunately when you separate the detectors in an array the total chi squared is turned into a giant one
    	#need to add all of them instead. 
 
    a,b,c,d=np.array_split(chiterms,Ndets)
    ab=np.add(a,b)
    cd=np.add(c,d)
    chisquareds=(np.add(ab,cd)) 
 
    return chisquareds


def indexer(chisquareds,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA):
    chimin = min(chisquareds)
    chisquareds = list(chisquareds)
    oa = np.deg2rad(np.linspace(bottheta,toptheta,ntheta))
    ob = np.deg2rad(np.linspace(botphi,topphi,nphi))
    Aofit = np.deg2rad(np.linspace(botA,topA,nA))
    thetaloc = np.rad2deg(oa[int((chisquareds.index(chimin)-(chisquareds.index(chimin) % (len(ob)*len(Aofit))))/(len(ob)*len(Aofit)))])
    philoc = np.rad2deg(ob[int(((chisquareds.index(chimin) % (len(ob)*len(Aofit)))-(chisquareds.index(chimin) % (len(Aofit))))/len(Aofit))])
    Aoguess=Aofit[int((chisquareds.index(chimin) % (len(ob)*len(Aofit)))  % len(Aofit))]
    
    return thetaloc, philoc, Aoguess

def quad_solver(detval,detnorm,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,background):
    #Need a fix for fine opt,  can't handle subtractions from 0..
    theta = np.deg2rad(np.linspace(bottheta,toptheta,ntheta))
    phi = np.deg2rad(np.linspace(botphi,topphi,nphi))
    #theta = [0 if o<0 else o for o in theta]
    #theta = [np.pi if o>np.pi else o for o in theta]
   # phi = [0 if p<0 else p for p in phi]
   # phi = [2*np.pi if p>2*np.pi else p for p in phi]
    mphi,mtheta = np.meshgrid(phi,theta)
    allthetas = np.concatenate(mtheta)
    allphis = np.concatenate(mphi)
    allvecs = hp.ang2vec(allthetas,allphis)
    As= np.linspace(botA,topA,nA)
  #alternate approach to the one below, doesn't really make a difference?   
  #  normarrs = np.zeros(int(len(theta)*len(phi)))
   # normarrs = [[detnorm[0],detnorm[1],detnorm[2]] if o==0 else o for o in normarrs]
    normarr = detnorm
    
    normarrs = []
    for garc in range((len(theta)*len(phi))):
        normarrs.append([normarr[0],normarr[1],normarr[2]])
        
    seps = findAngles(allvecs,normarrs)
    AA,SS = np.meshgrid(As,seps)
    Aofit = np.concatenate(AA)
    chiseps = np.concatenate(SS)
    
    #this is close, but needs to be a way to go one step further and do this in the next chiR
    bg = background * np.ones(len(chiseps))
    #good = chiseps < np.pi/2
    #bad = chiseps > np.pi/2
    
    #probs that, don't want to include bg 
    chiResponse = np.multiply(Aofit,chiresponse(chiseps)) + bg
    #chiResponse = [1e5 if i <= background else i for i in chiResponse]
    if detval > background: 
        chiterm = np.divide(np.power(np.subtract(chiResponse,detval),2),detval)
    else: 
        chiterm = 1e5 * np.ones(len(theta)*len(phi)*len(As))
    
    return chiterm



    
