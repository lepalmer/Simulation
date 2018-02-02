import healpy as hp 
import numpy as np 


class GRB():  #if this class inherits anything, it goes within these parenthasis
    """"
    A class where I define the GRB's I want to test, 
    giving them attributes such as strength and sky position. 
    
    Only action I am giving them at the moment is just print details, 
    a simple function, that you guessed it, prints details. 
		
	On second thought I'd rather not use this!

	"""

    def __init__(self,strength,theta,phi):
        self.strength = strength
        self.theta = np.deg2rad(theta)
        self.phi = np.deg2rad(phi)
    def print_details(self):
        print("This GRB will produce an effect of " + str(self.strength) + " counts, located at polar angle " + str(np.rad2deg(self.theta)) + " deg and azimuthal angle " + str(np.rad2deg(self.phi))+ " deg.") 
             
        
#not sure how else to globally define stuff, so its sitting here for now. 


################################################################################

class GRBs():
	"""
	Generates an array of GRB's given 
	certains strength at different sky positions.
	
	Output should be an array. 
	"""
	def __init__(self,NSIDE,strength):
		#depending on NSIDE, there will be anywhere from 12 to infinite spots on the sky w/ GRBs

		self.pixels = hp.nside2npix(NSIDE)
		self.strength
		#want to convert these pixels into theta phi coords. 
		self.sourceangs = []
		for i in range(self.pixels):
			self.sourceangs.append(hp.pix2ang(NSIDE,i))

		#now I want a BurstCube object to inherit these GRBs!

zenith = [0,0]
background = 1000
class BurstCube:
    def __init__(self):
        test = input("Are the detectors alternating? ")
        if test == "yes" or test == "Yes" or test == "y" or test == "asdlfkjawe":           
            self.tiltA = np.deg2rad(float(input("Please enter the first tilt (deg) ")))
            self.tiltB = np.deg2rad(float(input("Please enter the second tilt (deg) ")))
            self.tiltC = self.tiltA
            self.tiltD = self.tiltD
        else:
            self.tilt = np.deg2rad(float(input("Please enter the tilt (deg) ")))
            self.tiltA = self.tiltB = self.tiltC = self.tiltD = self.tilt
            
    
    #make the normal vectors!
        self.detA = [ zenith[0] + self.tiltA , zenith[1] ] 
        self.detB = [ zenith[0] + self.tiltB , zenith[1] + np.pi/2 ] 
        self.detC = [ zenith[0] + self.tiltC , zenith[1] + np.pi ] 
        self.detD = [ zenith[0] + self.tiltD , zenith[1] + 3*np.pi/2 ] 

        self.Anorm = hp.ang2vec(cube1.detA[0],cube1.detA[1])
		self.Bnorm = hp.ang2vec(cube1.detB[0],cube1.detB[1])
		self.Cnorm = hp.ang2vec(cube1.detC[0],cube1.detC[1])
		self.Dnorm = hp.ang2vec(cube1.detD[0],cube1.detD[1])


		self.dets = [self.Anorm,self.Bnorm,self.Cnorm,self.Dnorm] 

		#now have an array of all the detectors saved here, aka don't need to do this in sim code.

#	def response(self,A,B):

 #   	return pow(abs(np.cos(angle(A,B))),0.76)


def length(v):
    return mth.sqrt(np.dot(v, v))

def angle(v1, v2):

    return mth.acos(np.dot(v1, v2) / (length(v1) * length(v2)))

def response(A,B):
    #meant to imitate the response of the detectors for effective area vs. angle, found to be around .77
 #   print(length(A),length(B))
#if cosine is negative, 
    return pow(abs(np.cos(angle(A,B))),0.76)

def frodo(theta):
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

def solver(detsvals,bottheta,toptheta,botphi,topphi,n):
#this function uses a chi squared minimizer over a given range to identify the theta,phi,
#and Ao values which correspond to the minimum chi squared and thus localized source. 
    confidence = []
    chiterms = []
    thecon = []
    phicon = []
    for s in range(len(detsvals)):     
        oa=np.deg2rad(np.linspace(bottheta,toptheta,n))  #range of thetas to sample
        ob=np.deg2rad(np.linspace(botphi,topphi,n)) #phi
        Aofit=np.linspace(0,1000,25)  
        for sa in range(len(oa)): 
            for sb in range(len(ob)):
                for sc in range(len(Aofit)):
                    #make sure it fits within the acceptable range
                    if oa[sa]>=0 and oa[sa]<=np.pi and ob[sb]>=0 and ob[sb]<=2*np.pi:
                        CHIsourceang=[oa[sa],ob[sb]]
                        CHIsourcexyz = hp.ang2vec(CHIsourceang[0],CHIsourceang[1])
                        CHIsep=angle(CHIsourcexyz,dets[s])                                           
                        if CHIsep<np.pi: 
                            chi=Aofit[sc]*response(CHIsourcexyz,dets[s])+bg
                            #print("Chi test angle"+str(CHIsourcexyz))
                            #print("detector"+str(dets[s]))
                            #print("chi sometiems"+str(chi))
                            #print("separation here, is it okay? " +str(np.rad2deg(CHIsep)))

                            #this produces nan error, se
                            
                        else:
                            chi=0            
                        if detvals[s]>0:   #if there is a signal in the detector 
                            chiterm=((chi-detsvals[s])**2/detsvals[s])
                        else:    #if not, just zero 
                            chiterm=10000
                    else: 
                        chiterm=10000 #some large #, just to note that it definitely isn't right angle 
                                                                       
                                    
                    chiterms.append(chiterm)   #this is an array of EVERY SINGLE term, need to split in pieces and add element by element...
    chisquareds=chimaker(chiterms,len(detsvals))
    chimin=np.amin(chisquareds)
    chisquareds=list(chisquareds)
    thetaloc = np.rad2deg(oa[int((chisquareds.index(chimin)-(chisquareds.index(chimin) % (len(ob)*len(Aofit))))/(len(ob)*len(Aofit)))])
    philoc = np.rad2deg(ob[int(((chisquareds.index(chimin) % (len(ob)*len(Aofit)))-(chisquareds.index(chimin) % (len(Aofit))))/len(Aofit))])
    Aoguess=Aofit[int((chisquareds.index(chimin) % (len(ob)*len(Aofit)))  % len(Aofit))]
    #print(Aoguess)
    #print(thetaloc,philoc)
    
    return thetaloc,philoc,chisquareds,chimin,Aoguess


def rotate(x,y,theta):
 #   #inpute the x and y (or what components to be rotated) of the normal, and transform them by angle theta, provided in code.
    xnew=np.cos(theta)*x-np.sin(theta)*y
    ynew=np.sin(theta)*x+np.cos(theta)*y
    rotnorm=[xnew/((xnew*xnew+ynew*ynew)**.5),ynew/((xnew*xnew+ynew*ynew)**.5)]
    return rotnorm

    
    