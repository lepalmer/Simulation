
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

def solver(detsvals,detnorms,bgrd):
#this function uses a chi squared minimizer over a given range to identify the theta,phi,
#and Ao values which correspond to the minimum chi squared and thus localized source. 
    """Stray thoughts about code so far. Should be quicker, rather than 1000 use arbitrary vals, as well as top and bottom phi
    No longer need chimaker since it adds it in. 
    """
    
    chiterms = np.zeros(50)
    confidence = []
    thecon = []
    phicon = []
    for s in range(len(detsvals)): 
      #  print("Testing detector " + str(s))
        detresponse = detsvals[s]*np.ones(50)
        oa = np.deg2rad(np.linspace(0,90,50))
        ob = np.deg2rad(np.linspace(0,360,50))
        Aofit = np.linspace(0,1000,50)
        bg = bgrd*np.ones(50)
        #incorrect, will need to review later. 
        CHIsourcexyz.append(hp.ang2vec(oa,ob))  #this doesn't consider more than one option! Need to double iterate or something!

        chisep = []
        for i in range(len(CHIsourcexyz)): #all 1000 anyway
           # print(detnorms[s])
            chisep.append(angle(CHIsourcexyz[i],detnorms[s]))
        
        #If necessary,here's where I would create another array saying to ignore >pi/2 terms.
       # print(chisep)
        chisep = np.array(chisep) 
       # print("Len of chisep" + str(len(chisep)))

        chiresponse =  Aofit * response(chisep) + bg 
        for i in range(len(chiresponse)):
            if chisep[i] > np.pi/2:
                chiresponse[i] = 1e6 #arbitrarily huge number saying this number is out of the question. 
        print("chi terms: ")
        chiterms = chiterms + np.divide((chiresponse-detresponse)**2,detresponse)
       # print(chiterms)
      #  print("len of Chiterms = " + str(len(chiterms)))                                                          
        

    chimin=np.amin(chiterms)
    #print("Chi min" + str(chimin))

    chisquareds=list(chiterms)
    print("Index of theta; " + str(int((chisquareds.index(chimin)-(chisquareds.index(chimin) % (len(ob)*len(Aofit))))/(len(ob)*len(Aofit)))))
    thetaloc = np.rad2deg(oa[int((chisquareds.index(chimin)-(chisquareds.index(chimin) % (len(ob)*len(Aofit))))/(len(ob)*len(Aofit)))])
    print("Theta loc " + str(thetaloc))
    philoc = np.rad2deg(ob[int(((chisquareds.index(chimin) % (len(ob)*len(Aofit)))-(chisquareds.index(chimin) % (len(Aofit))))/len(Aofit))])
    Aoguess=Aofit[int((chisquareds.index(chimin) % (len(ob)*len(Aofit)))  % len(Aofit))]
    #print(Aoguess)
    #print(thetaloc,philoc)
    
    return thetaloc,philoc,Aoguess


def rotate(x,y,theta):
 #   #inpute the x and y (or what components to be rotated) of the normal, and transform them by angle theta, provided in code.
    xnew=np.cos(theta)*x-np.sin(theta)*y
    ynew=np.sin(theta)*x+np.cos(theta)*y
    rotnorm=[xnew/((xnew*xnew+ynew*ynew)**.5),ynew/((xnew*xnew+ynew*ynew)**.5)]
    return rotnorm

    
    
