import numpy as np
import healpy as hp
import burstfuncs as bf

class GRBs():
 

    """
    Generates an array of GRB's given 
    certains strength at different sky positions.
    
    Output should be an array. 
    """
    def __init__(self,NSIDE,strength):
        import numpy as np
        import healpy as hp
        #depending on NSIDE, there will be anywhere from 12 to infinite spots on the sky w/ GRBs
        self.Ao = strength
        self.pixels = hp.nside2npix(NSIDE)

        #want to convert these pixels into theta phi coords. 
        self.sourceangs = []
        for i in range(self.pixels):
            self.sourceangs.append(hp.pix2ang(NSIDE,i))


class BurstCube:
    def __init__(self,background):
        import numpy as np
        import healpy as hp
        import burstfuncs as bf
        self.zenith = [0 , 0]
        self.bg = background
        test = input("Are the detectors alternating? ")
        if test == "yes" or test == "Yes" or test == "y" or test == "asdlfkjawe":           
            self.tiltA = np.deg2rad(float(input("Please enter the first tilt (deg) ")))
            self.tiltB = np.deg2rad(float(input("Please enter the second tilt (deg) ")))
            self.tiltC = self.tiltA
            self.tiltD = self.tiltB
        else:
            self.tilt = np.deg2rad(float(input("Please enter the tilt (deg) ")))
            self.tiltA = self.tiltB = self.tiltC = self.tiltD = self.tilt
            
        
    @property
    def detA(self):
        return [ self.zenith[0] + self.tiltA , self.zenith[1] ]
    @property 
    def detB(self):
        return [ self.zenith[0] + self.tiltB , self.zenith[1] + np.pi/2 ]
    @property
    def detC(self):
        return [ self.zenith[0] + self.tiltC , self.zenith[1] ]
    @property 
    def detD(self):
        return [ self.zenith[0] + self.tiltD , self.zenith[1] + np.pi/2 ]
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
    
    
    
    
    def respond2GRB(self, GRB):   #is this how I inherit? 
        #first need to include the GRB.
        
        

        """
        At the moment, "GRB" is one particular instance 
        of the class GRBs, how do I do it such that 
        I can define the GRB class as generally as possible? 
        
        """
        localizationerrors = []    
        for i in range(len(GRB.sourceangs)):
            sourceAng = GRB.sourceangs[i]
           # print("Source angle is " + str(sourceAng))
           #this check passes.       

            
           # print("Testing at " + str(np.rad2deg(GRB.sourceangs)))
            sourcexyz = hp.ang2vec(sourceAng[0],sourceAng[1]) #cartesian position of the burst
            loop = 0 #I'm going to want to sample each sky position more than once,
                    #here's where I define how many times that is
            locunc = []
            while loop<3:
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
    
                   #now for the LSF method using chi squared, applies a coarse to fine refactor here. 
                   #plenty of old variable names to update as well. 
                
                   # print("after fluctuations, " + str(detactual))
                    #fixed indentation errors, uninstalled module, legacy code all fixed. Passes. 

                
                
                coarsethetaloc,coarsephiloc,coarseAo = bf.solver(detcounts,self.dets,0,90,0,360,12,self.bg)
                finethetaloc,finephiloc,fineAo = bf.solver(detcounts,self.dets,coarsethetaloc-5,coarsethetaloc+5,coarsephiloc-7,coarsephiloc+7,12,self.bg)
                
                if finethetaloc > 180:
                #    print("it recovered an unrealistic answer, skip")
                    break
                elif finethetaloc < 0:
                    #print("Same issue, there are limits to theta that are broken here. ")
                    break 
                    
                recpos = [finethetaloc,finephiloc]
                recvec = hp.ang2vec(np.deg2rad(finethetaloc),np.deg2rad(finephiloc))
                locunc.append(bf.angle(sourcexyz,recvec))
               # print("loc unc" + str(locunc))
                loop+=1
            print(np.rad2deg(s.mean(locunc)))

            localizationerrors.append(np.rad2deg(s.mean(locunc)))

           # print("obtained error of" +  str(s.mean(locunc)))
                #loc unc is the uncertainty at each sky position, localerros is for all of them
            
            #should there be more selfs? more prints? basically done so time to debug after lunch. 
        return localizationerrors
        