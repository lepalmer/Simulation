import healpy as hp
import numpy as np
import random as rand
import statistics as s
import burstfuncs as bf

class GRBs():
   #this produces an error, deal with soon!
    """
    Generates an array of GRB's given 
    certains strength at different sky positions.
    
    Output should be an array. 
    """
    
  #  import numpy as np
   # import healpy as hp
    def __init__(self,NSIDE,strength):
        from healpy import nside2npix
        from healpy import pix2ang
        #depending on NSIDE, there will be anywhere from 12 to infinite spots on the sky w/ GRBs
        self.Ao = strength
        self.pixels = nside2npix(NSIDE)

        #want to convert these pixels into theta phi coords. 
        self.sourceangs = []
        for i in range(self.pixels):
            self.sourceangs.append(pix2ang(NSIDE,i))

    def say_Ao(self):
        print("The GRBs being tested will be " + str(self.Ao) + " counts strong.")
        
        

class BurstCube():

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
        return [ self.zenith[0] + self.tiltC , self.zenith[1] ]
    @property 
    def detD(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
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
        for i in range(len(GRB.sourceangs/4)):
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
                recpos = [0,0]    
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
                #loc unc is the uncertainty at each sky position, localerros is for all of them
            
            #should there be more selfs? more prints? basically done so time to debug after lunch. 
        
        maybe = input("All done with the simulation, want to make the skymap too? ")
        
        if maybe == "yes" or maybe == "Yes" or maybe == "y": 
            import matplotlib.pyplot as plt
            from healpy import newvisufunc
            if len(self.localizationerrors) == len(GRB.sourceangs):
                im = np.array(self.localizationerrors)
            else:
                blockedpart=1000*np.ones(GRB.pixels-len(self.localizationerrors))
                im = np.concatenate((self.localizationerrors,blockedpart))
            hp.newvisufunc.mollview(im,min=0, max=30,unit='Localization Accurary (degrees)',graticule=True,graticule_labels=True,cmap='viridis_r')
            plt.title('All Sky Localization Uncertainty for BurstCube')
        else:
            print("Ok, maybe next time!")

        return self.localizationerrors
            
    
    

    
    """   
    def plot_skymap(self,GRB):
        import numpy as np
        import matplotlib.pyplot as plt
        import healpy as hp
        from healpy import newvisufunc
        if len(self.localizationerrors) == len(GRB.sourceangs):  #if the function successfully was able to catch all the spots (meaning nothing went wrong!)
            im = np.array(self.localizationerrors) 
        else:
            blockedpart=1000*np.ones(GRB.pixels-len(angoffset))
            im=np.concatenate((self.localizationerrors,blockedpart))
        hp.newvisufunc.mollview(im,min=0, max=30,unit='Localization Accurary (degrees)',graticule=True,graticule_labels=True,cmap='viridis_r')
        plt.title('All Sky Localization Uncertainty for BurstCube')
 
    """       
        