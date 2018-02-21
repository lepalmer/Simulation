
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


def chiresponse(stren,A,back):
    """
    Meant to imitate the actual response of a scintillator.
    Inputs 2 vectors, and responds with a cos^x dependence.
    """
    #meant to imitate the response of the detectors for effective area vs. angle, found to be around .77
 #   print(length(A),length(B))
#if cosine is negative, 

    mask = A > np.pi/2.

    A[mask] = 0
    A = np.add(np.multiply(stren,pow(abs(np.cos(A[~mask])),0.76)),back)
    
    
    return A

def response(strength,A,back):
    """
    Meant to imitate the actual response of a scintillator.
    Inputs 2 vectors, and responds with a cos^x dependence.
    """
    #meant to imitate the response of the detectors for effective area vs. angle, found to be around .77
 #   print(length(A),length(B))
#if cosine is negative, 
    if A < np.pi/2:
        R = strength*pow(abs(np.cos(A)),0.76) + back
    else: 
        R = 0
    
    
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


def solver(detsvals,detnorms,bottheta,toptheta,botphi,topphi,ntheta,nphi,bgrd):
    """Based on the given normal of a detector along with its inferred # of counts, this function identifies the strength and sky position that best matches these conditions. 
    Parameters
    ----------
    detsvals : array
        Numpy array containing the relative counts in each of the 4 BurstCube detectors.
    detnorms : array
        Numpy array containing the normal vector of each of the 4 BurstCube detectors. 
    bottheta : float
        Minimum polar angle to be tested. 
    toptheta : float
        Maximum polar angle to be tested. 
    botphi : float
        Minimum azimuthal angle to be tested. 
    topphi : float
        Maximum azimuthal angle to be tested. 
    ntheta : int
        Number of sample points between bottheta and toptheta.
    nphi : int
        Number of sample points between botphi and topphi.
    bgrd : float
        # of background counts inherent to each detector. 
    Returns 
    -------
    thetaloc : float
        The inferred polar angle of the incident GRB. 
    philoc : float
        The inferred azimuthal angle of the incident GRB.
    Aoguess : float
        The inferred strength of the incident GRB. 
    """
#this function uses a chi squared minimizer over a given range to identify the theta,phi,
#and Ao values which correspond to the minimum chi squared and thus localized source. 
    confidence = []
    chiterms = []
    thecon = []
    phicon = []
    for s in range(len(detsvals)):     
        print("Det val: " + str(detsvals[s]))
        
        oa=np.deg2rad(np.linspace(bottheta,toptheta,ntheta))  #range of thetas to sample
        ob=np.deg2rad(np.linspace(botphi,topphi,nphi)) #phi
        Aofit=np.linspace(0,1000,2)  

        
        for sa in range(len(oa)): 
            for sb in range(len(ob)):
                for sc in range(len(Aofit)):
                    #make sure it fits within the acceptable range
                    if oa[sa]>=0 and oa[sa]<=np.pi and ob[sb]>=0 and ob[sb]<=2*np.pi:
                        CHIsourceang=[oa[sa],ob[sb]]
                        CHIsourcexyz = hp.ang2vec(CHIsourceang[0],CHIsourceang[1])
                        CHIsep=angle(CHIsourcexyz,detnorms[s])                                           
                        chi=response(Aofit[sc],CHIsep,bgrd)
                            #print("Chi test angle"+str(CHIsourcexyz))
                            #print("detector"+str(dets[s]))
                            #print("chi sometiems"+str(chi))
                            #print("separation here, is it okay? " +str(np.rad2deg(CHIsep)))

                            #this produces nan error, se
                            
                       # else:
                       #     chi=0            
                        if detsvals[s]>0:   #if there is a signal in the detector 
                            chiterm=((chi-detsvals[s])**2/detsvals[s])
                        else:    #if not, just zero 
                            chiterm=1e10
                    else: 
                        chiterm=1e10 #some large #, just to note that it definitely isn't right angle 
                                                                       
                                    
                    chiterms.append(chiterm)   #this is an array of EVERY SINGLE term, need to split in pieces and add element by element...
    chisquareds=chimaker(chiterms,len(detsvals))
    chimin=np.amin(chisquareds)
    #print("The chi min is " + str(chimin))
    #is there a better way to do this? 
    chisquareds=list(chisquareds)

    thetaloc = np.rad2deg(oa[int((chisquareds.index(chimin)-(chisquareds.index(chimin) % (len(ob)*len(Aofit))))/(len(ob)*len(Aofit)))])
    philoc = np.rad2deg(ob[int(((chisquareds.index(chimin) % (len(ob)*len(Aofit)))-(chisquareds.index(chimin) % (len(Aofit))))/len(Aofit))])
    Aoguess=Aofit[int((chisquareds.index(chimin) % (len(ob)*len(Aofit)))  % len(Aofit))]
    #print(Aoguess)
    #print(thetaloc,philoc)
    
    return thetaloc,philoc,Aoguess, chisquareds



def quad_solver(detval,detnorm,bottheta,toptheta,botphi,topphi,background):
    print("Detector val: " + str(detval))
    theta = np.deg2rad(np.linspace(bottheta,toptheta,2))
    phi = np.deg2rad(np.linspace(botphi,topphi,2))
    mphi,mtheta = np.meshgrid(phi,theta)
    allthetas = np.concatenate(mtheta)
    allphis = np.concatenate(mphi)
    allvecs = hp.ang2vec(allthetas,allphis)
    As= np.linspace(0,1000,2)
    normarr = detnorm
    normarrs = []
    for garc in range((len(theta)*len(phi))):
        normarrs.append([normarr[0],normarr[1],normarr[2]])
        
    seps = findAngles(allvecs,normarrs)
    print("separation here, is it okay? " +str(np.rad2deg(seps)))

    AA,SS = np.meshgrid(As,seps)
    Aofit = np.concatenate(AA)
    chiseps = np.concatenate(SS)
    
    #this is close, but needs to be a way to go one step further and do this in the next chiR
    bg = background * np.ones(len(chiseps))
    #good = chiseps < np.pi/2
    #bad = chiseps > np.pi/2
    
    
    chiResponse = chiresponse(Aofit,chiseps,background)

    if detval > background: 
        chiterm = np.divide(np.power(np.subtract(chiResponse,detval),2),detval)
    else: 
        chiterm = 1e5 * np.ones(len(theta)*len(phi)*len(As))
    
    return chiterm


def rotate(x,y,theta):
 #   #inpute the x and y (or what components to be rotated) of the normal, and transform them by angle theta, provided in code.
    xnew=np.cos(theta)*x-np.sin(theta)*y
    ynew=np.sin(theta)*x+np.cos(theta)*y
    rotnorm=[xnew/((xnew*xnew+ynew*ynew)**.5),ynew/((xnew*xnew+ynew*ynew)**.5)]
    return rotnorm

    
    
