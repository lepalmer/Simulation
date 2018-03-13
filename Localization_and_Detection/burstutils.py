
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



def response(A):
    """
    Meant to imitate the actual response of a scintillator.
    Inputs 2 vectors, and responds with a cos^x dependence.
    """
    #meant to imitate the response of the detectors for effective area vs. angle, found to be around .77
 #   print(length(A),length(B))
#if cosine is negative, 
    return pow(abs(np.cos(A)),0.76)

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

def speedy_solver(detsvals,detnorms,bottheta,toptheta,botphi,topphi,n):
    theta = np.deg2rad(np.linspace(0,90,10))
    phi = np.deg2rad(np.linspace(0,360,37))
    mtheta,mphi = np.meshgrid(theta,phi)
    chiveco = hp.ang2vec(mtheta,mphi)
    chivecs = np.concatenate(chiveco)
    As= np.linspace(0,1000,30)
    chiterms = 0
    for s in range(len(detsvals)):
        normarr = detnorms[s]
        normarrs = []
        for garc in range((len(theta)*len(phi))):
            normarrs.append([normarr[0],normarr[1],normarr[2]])
        
        seps = findAngles(chivecs,normarrs)

        AA,SS = np.meshgrid(As,seps)

        Aofit = np.concatenate(AA)
        chiseps = np.concatenate(SS)
        bg = 1000 * np.ones(len(chiseps))
        chiResponse = np.multiply(Aofit,response(chiseps)) + bg
        chiterm = np.divide(np.power(np.subtract(chiResponse,detsvals[s]),2),detsvals[s])
        chiterms += chiterm
    chimin = min(chiterms)
    chisquareds = list(chiterms)
    thetaloc = np.rad2deg(theta[int((chisquareds.index(chimin)-(chisquareds.index(chimin) % (len(phi)*len(Aofit))))/(len(phi)*len(Aofit)))])
    philoc = np.rad2deg(phi[int(((chisquareds.index(chimin) % (len(phi)*len(Aofit)))-(chisquareds.index(chimin) % (len(Aofit))))/len(Aofit))])
    Aoguess=Aofit[int((chisquareds.index(chimin) % (len(phi)*len(Aofit)))  % len(Aofit))]
    
    return thetaloc,philoc,Aoguess

def rotate(x,y,theta):
 #   #inpute the x and y (or what components to be rotated) of the normal, and transform them by angle theta, provided in code.
    xnew=np.cos(theta)*x-np.sin(theta)*y
    ynew=np.sin(theta)*x+np.cos(theta)*y
    rotnorm=[xnew/((xnew*xnew+ynew*ynew)**.5),ynew/((xnew*xnew+ynew*ynew)**.5)]
    return rotnorm

    
    