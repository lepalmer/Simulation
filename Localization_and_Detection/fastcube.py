#The following cell contains the "FastCube" class. This is the simulation I hope to use to be able to run quicker simulations. 

import numpy as np
import healpy as hp
import burstutils as bf
import random as rand
import statistics as s
import time as time

class FastCube():

    def __init__(self,background,dettilt,alternating=False):
        if alternating == False:
            self.tilt = np.deg2rad(dettilt)
            self.tiltA = self.tiltB = self.tiltC = self.tiltD = self.tilt
        
        else:
            self.tiltB = (float(input("Please enter the second tilt (deg) ")))
            self.tiltB = np.deg2rad(self.tiltB)
            self.tiltC = self.tiltA = np.deg2rad(dettilt)
            self.tiltD = self.tiltB
        
        self.zenith = [0 , 0]
        self.bg = background


        
    @property
    def detA(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltA , self.zenith[1] ]
    @property 
    def detB(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltB , self.zenith[1] + np.pi/2 ]
    @property
    def detC(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltC , self.zenith[1] + np.pi ]
    @property 
    def detD(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltD , self.zenith[1] + 3*np.pi/2 ]
    @property
    def normA(self):
        return  hp.ang2vec(self.detA[0],self.detA[1])
    @property 
    def normB(self):
        return  hp.ang2vec(self.detB[0],self.detB[1])
    @property
    def normC(self):
        return  hp.ang2vec(self.detC[0],self.detC[1])
    @property 
    def normD(self):
        return  hp.ang2vec(self.detD[0],self.detD[1])

    
    @property
    def dets(self):
        return [self.normA,self.normB,self.normC,self.normD] 
    
    
    
    def response2GRB(self, GRB, test=True):   #is this how I inherit? 
        start = time.time()
        #first need to include the GRB.
       
        """
        Using least squares regression, respond2GRB will determine the sky position of an array of GRB sources assuming some inherent background noise within 
        detectors, along with fluctuations of either Gaussian or Poissonian nature. 

        Parameters
        ----------
        GRB : object
            An instance of the separately defined "GRBs" class that contains a number of evenly spaced sky positions of a given strength. 
        
        test : boolean 
            For sanity purposes, if the simulation seems to give unrealistic results, switching to test mode allows for much quicker sampling, allowing it easier to spot potential errors. 
        
        

        Returns
        ----------
        localizationerrors : array
            numpy array that contains the average localization uncertainty at each sky position. 
        
        Additionally, response2GRB will print the sky position it is currently sampling, along with the average offset of localizations at that spot. 
        
        """
        
        if test:
            sample = 1
            samples = 50  #times  per sky pos
            bottheta = 0
            toptheta = 90
            botphi = 0 
            topphi = 360
            botA = 0
            topA = 1000
            ntheta = 10   #over sky chi points
            nphi = 37
            nA = 100

        else:
            sample = len(GRB.sourceangs) 
            samples = 50 #times  per sky pos
            bottheta = 0
            toptheta = 90
            botphi = 0 
            topphi = 360
            botA = 400
            topA = 1000
            ntheta = 31   #over sky chi points
            nphi = 120
            nA = 12
        self.localizationerrors = []    
        for i in range(sample):
            sourceAng = GRB.sourceangs[i]
            print("Testing " + str(np.rad2deg(sourceAng)))
           #this check passes.       

            
           # print("Testing at " + str(np.rad2deg(GRB.sourceangs)))
            sourcexyz = hp.ang2vec(sourceAng[0],sourceAng[1]) #cartesian position of the burst
            loop = 0 #I'm going to want to sample each sky position more than once,
                    #here's where I define how many times that is
            locunc = []
            while loop<samples:
                sepA=bf.angle(sourcexyz,self.normA)
                   # print("separation from A is " + str(np.rad2deg(sepA)))
                   #this check passes.  
               
                if sepA < np.pi/2: # meaning if >90, would not be facing detector.
                    dtheoryA=GRB.Ao*bf.response(bf.angle(sourcexyz,self.normA))  #still need to define strength, brb and gonna do that 
                else: #like I was saying, has to face it!
                    dtheoryA = 0 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsA = dtheoryA + self.bg #another artifact, incl this background effect somewhere
                unccountsA = np.sqrt(countsA)
                detactualA = rand.gauss(countsA,unccountsA)  #there is a lot of noise, present, updating it now. 
                if detactualA-self.bg < 0:
                    detactualA = self.bg
                    
                detcountsA = detactualA
                
                sepB=bf.angle(sourcexyz,self.normB)
                   # print("separation from B is " + str(np.rad2deg(sepB)))
                   #this check passes.  
               
                if sepB < np.pi/2: # meaning if >90, would not be facing detector.
                    dtheoryB=GRB.Ao*bf.response(bf.angle(sourcexyz,self.normB))  #still need to define strength, brb and gonna do that 
                else: #like I was saying, has to face it!
                    dtheoryB = 0 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsB = dtheoryB + self.bg #another artifact, incl this background effect somewhere
                unccountsB = np.sqrt(countsB)
                detactualB = rand.gauss(countsB,unccountsB)  #there is a lot of noise, present, updating it now. 
                if detactualB-self.bg < 0:
                    detactualB = self.bg
                    
                detcountsB = detactualB

                sepC=bf.angle(sourcexyz,self.normC)
                   # print("separation from C is " + str(np.rad2deg(sepC)))
                   #this check passes.  
               
                if sepC < np.pi/2: # meaning if >90, would not be facing detector.
                    dtheoryC=GRB.Ao*bf.response(bf.angle(sourcexyz,self.normC))  #still need to define strength, brb and gonna do that 
                else: #like I was saying, has to face it!
                    dtheoryC = 0 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsC = dtheoryC + self.bg #another artifact, incl this background effect somewhere
                unccountsC = np.sqrt(countsC)
                detactualC = rand.gauss(countsC,unccountsC)  #there is a lot of noise, present, updating it now. 
                if detactualC-self.bg < 0:
                    detactualC = self.bg
                    
                detcountsC = detactualC
                
                sepD=bf.angle(sourcexyz,self.normD)
                   # print("separation from D is " + str(np.rad2deg(sepD)))
                   #this check passes.  
               
                if sepD < np.pi/2: # meaning if >90, would not be facing detector.q
                    dtheoryD=GRB.Ao*bf.response(bf.angle(sourcexyz,self.normD))  #still need to define strength, brb and gonna do that 
                else: #like I was saying, has to face it!
                    dtheoryD = 0 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsD = dtheoryD + self.bg #another artifact, incl this background effect somewhere
                unccountsD = np.sqrt(countsD)
                detactualD = rand.gauss(countsD,unccountsD)  #there is a lot of noise, present, updating it now. 
                if detactualD-self.bg < 0:
                    detactualD = self.bg
                    
                detcountsD = detactualD
                
                #coarse to fine optimization
                chiA = bf.quad_solver(detcountsA,self.normA,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg)
                chiB = bf.quad_solver(detcountsB,self.normB,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg)
                chiC = bf.quad_solver(detcountsC,self.normC,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg)
                chiD = bf.quad_solver(detcountsD,self.normD,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg)
                
                chisquared = np.add(np.add(chiA,chiB),np.add(chiC,chiD)) #adds it all up for total chi2
                
                #print("Chi squareds: " +str(chisquared))
                
                
                thetaloc, philoc, Aguess = bf.indexer(chisquared,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA)
                recvec = hp.ang2vec(np.deg2rad(thetaloc),np.deg2rad(philoc))
                locoffset = np.rad2deg(bf.angle(sourcexyz,recvec))
               # print("Loc offset = " + str(locoffset) + " deg")
                
                locunc.append(locoffset)
                loop +=1
            print("Avg loc offset = " + str(s.mean(locunc)) + " deg.")
            self.localizationerrors.append(s.mean(locunc))
        return self.localizationerrorsq