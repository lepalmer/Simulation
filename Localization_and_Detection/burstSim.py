import numpy as np
import healpy as hp
import burstutils as bf
import random as rand
import statistics as s

class BurstCube():

    def __init__(self,background,dettilt,alternating=False):
        if alternating == False:
            self.tilt = np.deg2rad(dettilt)
            self.tiltA = self.tiltB = self.tiltC = self.tiltD = self.tilt
        
        else:
            self.tiltB = np.deg2rad(float(input("Please enter the second tilt (deg) ")))
        
            self.tiltC = self.tiltA = dettilt
            self.tiltD = self.tiltB
        self.zenith = [0 , 0]
        self.bg = background

            
    
    #make the normal vectors!
        #self.detA = [ zenith[0] + self.tiltA , zenith[1] ] 
        #self.detB = [ zenith[0] + self.tiltB , zenith[1] + np.pi/2 ] 
       # self.detC = [ zenith[0] + self.tiltC , zenith[1] + np.pi ] 
        #self.detD = [ zenith[0] + self.tiltD , zenith[1] + 3*np.pi/2 ] 

        #self.Anorm = hp.ang2vec(self.detA[0],self.detA[1])
        #self.Bnorm = hp.ang2vec(self.detB[0],self.detB[1])
        #self.Cnorm = hp.ang2vec(self.detC[0],self.detC[1])
        #self.Dnorm = hp.ang2vec(self.detD[0],self.detD[1])

    
       # self.dets = [self.Anorm,self.Bnorm,self.Cnorm,self.Dnorm] 
        
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
    
    
    
    def response2GRB(self, GRB):   #is this how I inherit? 
        #first need to include the GRB.
       
        """
        Using least squares regression, respond2GRB will determine the sky position of an array of GRB sources assuming some inherent background noise within 
        detectors, along with fluctuations of either Gaussian or Poissonian nature. 

        Parameters
        ----------
        GRB : object
        
        An instance of the separately defined "GRBs" class that contains a number of evenly spaced sky positions of a given strength. 

        Returns
        ----------
        localizationerrors : array

        numpy array that contains the average localization uncertainty at each sky position. 

        
        """
        
        self.localizationerrors = []    
        for i in range(len(GRB.sourceangs)):
            sourceAng = GRB.sourceangs[i]
            print("Testing " + str(np.rad2deg(sourceAng)))
           #this check passes.       

            
           # print("Testing at " + str(np.rad2deg(GRB.sourceangs)))
            sourcexyz = hp.ang2vec(sourceAng[0],sourceAng[1]) #cartesian position of the burst
            loop = 0 #I'm going to want to sample each sky position more than once,
                    #here's where I define how many times that is
            locunc = []
            while loop<10:
                detcounts = []  #number of counts incident in each detector. 
                for j in range(len(self.dets)):
                    sep=bf.angle(sourcexyz,self.dets[j])
                   # print("separation is " + str(np.rad2deg(sep)))
                   #this check passes.  
               
                    if sep < np.pi/2: # meaning if >90, would not be facing detector.
                        dtheory=GRB.Ao*bf.response(sourcexyz,self.dets[j])  #still need to define strength, brb and gonna do that 
                    else: #like I was saying, has to face it!
                        dtheory = 0 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                    counts = dtheory + self.bg #another artifact, incl this background effect somewhere
                    unccounts = np.sqrt(counts)
                    detactual = rand.gauss(counts,unccounts)  #there is a lot of noise, present, updating it now. 
                    if detactual-self.bg < 0:
                        detactual = 0
                    
                    detcounts.append(detactual)
                
                
                coarsethetaloc,coarsephiloc,coarseAo = bf.solver(detcounts,self.dets,0,90,0,360,10,37,self.bg)
                finethetaloc,finephiloc,fineAo = bf.solver(detcounts,self.dets,coarsethetaloc-6,coarsethetaloc+6,coarsephiloc-6,coarsephiloc+6,5,5,self.bg)
                
                if finethetaloc > 180:
                #    print("it recovered an unrealistic answer, skip")
                    break
                elif finethetaloc < 0:
                    #print("Same issue, there are limits to theta that are broken here. ")
                    break 
                recpos = [finethetaloc,finephiloc]
              #  print("Recovered position at " + str(recpos))
                
                recvec = hp.ang2vec(np.deg2rad(finethetaloc),np.deg2rad(finephiloc))
                locunc.append(bf.angle(sourcexyz,recvec))
              #   print("loc unc: " + str(np.rad2deg(bf.angle(sourcexyz,recvec))) + " deg")
                loop+=1
          #  print("Obtained avg loc unc of " + np.rad2deg(s.mean(locunc)) + "")
            if len(locunc)>0:
                self.localizationerrors.append(np.rad2deg(s.mean(locunc)))
            else:
                self.localizationerrors.append(1000)
                #some big # signifying that it can't catch it 

            print("avg loc unc  " +  str(s.mean(np.rad2deg(locunc))))

        return self.localizationerrors
