#The following cell contains the "FastCube" class. This is the simulation I hope to use to be able to run quicker simulations. 
#Import dependencies
from numpy import rad2deg,deg2rad,pi,sqrt,add,array,average
from healpy import ang2vec, newvisufunc

try:
    from NoahSim import burstutils as bf
except:
    import burstutils as bf

from random import gauss
import statistics as s
import matplotlib.pyplot as plt

class FastCube():

    def __init__(self,background,dettilt,alternating=False):
        if alternating == False:
            self.tilt = deg2rad(dettilt)
            self.tiltA = self.tiltB = self.tiltC = self.tiltD = self.tilt
        
        else:
            self.tiltB = (float(input("Please enter the second tilt (deg) ")))
            self.tiltB = deg2rad(self.tiltB)
            self.tiltC = self.tiltA = deg2rad(dettilt)
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
        return [ self.zenith[0] + self.tiltB , self.zenith[1] + pi/2 ]
    @property
    def detC(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltC , self.zenith[1] + pi ]
    @property 
    def detD(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltD , self.zenith[1] + 3*pi/2 ]
    @property
    def normA(self):
        return  ang2vec(self.detA[0],self.detA[1])
    @property 
    def normB(self):
        return  ang2vec(self.detB[0],self.detB[1])
    @property
    def normC(self):
        return  ang2vec(self.detC[0],self.detC[1])
    @property 
    def normD(self):
        return  ang2vec(self.detD[0],self.detD[1])

    
    @property
    def dets(self):
        return [self.normA,self.normB,self.normC,self.normD] 
    
    def response2oneGRB(self,sourcetheta,sourcephi,sourcestrength):
        """If you wish, will allow you to examine the localization uncertainty of one sampled GRB of some given strength at some point in the sky. 
        For a full/complete simulation use the function below, "response2GRB".

        Parameters
        ----------
        sourcetheta : float
            The displacement in degrees in the zenithal direction.
        
        sourcephi : float
            The displacement in degrees in the azimuthal direction.

        sourcestrength : float 
            The stength in counts of the simulated GRB. 

        Returns
        -------
            recpos : float
                The reconstructed position of the GRB based on the detectors' response. 


        """

        #I like to visualize things in degrees, but convert to radians right away.
        sourcetheta = deg2rad(sourcetheta)
        sourcephi = deg2rad(sourcephi)
        sourcexyz = ang2vec(sourcetheta,sourcephi) #cartesian position of the burst

        print("Testing a burst @ " + str(rad2deg([sourcetheta, sourcephi])))

    #These are the values that get thrown into the solver. Basically they create an interval of possible sources of the sky, and will be used for a best fit down the line. 
        bottheta = 0
        toptheta = 90
        botphi = 0 
        topphi = 360
        botA = 0
        topA = 1000
        ntheta = 10   #over sky chi points
        nphi = 37
        nA = 100

        sepA=bf.angle(sourcexyz,self.normA)
        xA = bf.look_up_A(self.normA,sourcexyz)
                   # print("separation from A is " + str(np.rad2deg(sepA)))
                   #this check passes.  
               
        dtheoryA=GRB.Ao*bf.response(sepA,xA)  #still need to define strength, brb and gonna do that 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
        countsA = dtheoryA + self.bg
        unccountsA = sqrt(countsA)
        detactualA = gauss(countsA,unccountsA)  #there is a lot of noise present, updating it now. 
        if detactualA-self.bg < 0:
            detactualA = self.bg
                    
        detcountsA = detactualA
        sepB=bf.angle(sourcexyz,self.normB)
        xB = bf.look_up_B(self.normB,sourcexyz)

                   # print("separation from B is " + str(np.rad2deg(sepB)))
                   #this check passes.  
               
        dtheoryB=GRB.Ao*bf.response(sepB,xB)  
                    #still need to define strength, brb and gonna do that 

                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
        countsB = dtheoryB + self.bg 
        unccountsB = sqrt(countsB)
        detactualB = gauss(countsB,unccountsB)  #there is a lot of noise, present, updating it now. 
        if detactualB-self.bg < 0:
            detactualB = self.bg
                    
        detcountsB = detactualB
                


        sepC=bf.angle(sourcexyz,self.normC)
                   # print("separation from C is " + str(np.rad2deg(sepC)))
                   #this check passes.  
        xC =  bf.look_up_C(self.normC,sourcexyz)
        dtheoryC=GRB.Ao*bf.response(sepC,xC)  #still need to define strength, brb and gonna do that 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
        countsC = dtheoryC + self.bg #another artifact, incl this background effect somewhere
        unccountsC = sqrt(countsC)
        detactualC = gauss(countsC,unccountsC)  #there is a lot of noise, present, updating it now. 
        if detactualC-self.bg < 0:
                    detactualC = self.bg
                    
        detcountsC = detactualC
                
                

                
        sepD=bf.angle(sourcexyz,self.normD)
                   # print("separation from D is " + str(np.rad2deg(sepD)))
                   #this check passes.  
        xD = bf.look_up_D(self.normD,sourcexyz)
        dtheoryD=GRB.Ao*bf.response(sepD,xD)  #still need to define strength, brb and gonna do that 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
        countsD = dtheoryD + self.bg #another artifact, incl this background effect somewhere
        unccountsD = sqrt(countsD)
        detactualD = gauss(countsD,unccountsD)  #there is a lot of noise, present, updating it now. 
        if detactualD-self.bg < 0:
            detactualD = self.bg
                    
        detcountsD = detactualD
                

                
                
                #coarse to fine optimization
        chiA = bf.quad_solver(detcountsA,self.normA,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg,A=True)
        chiB = bf.quad_solver(detcountsB,self.normB,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg,B=True)
        chiC = bf.quad_solver(detcountsC,self.normC,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg,C=True)
        chiD = bf.quad_solver(detcountsD,self.normD,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg,D=True)
                
        chisquared = add(add(chiA,chiB),add(chiC,chiD)) #adds it all up for total chi2

        thetaloc, philoc, Aguess = bf.indexer(chisquared,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA)
        recvec = ang2vec(deg2rad(thetaloc),deg2rad(philoc))
        locoffset = rad2deg(bf.angle(sourcexyz,recvec))
        print("Loc offset = " + str(locoffset) + " deg")

    def response2GRB(self, GRB, samples,test=True,talk=False):   #is this how I inherit? 

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
        
        
        talk : boolean
            If desired, prints position by position results. 
        
        Returns
        ----------
        localizationerrors : array
            numpy array that contains the average localization uncertainty at each sky position. 
        
        Additionally, response2GRB will print the sky position it is currently sampling, along with the average offset of localizations at that spot. 
        
        """
        
        if test:
            sample = 1
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
            if talk:
                print("Testing " + str(rad2deg(sourceAng)))
           #this check passes.       

            
           # print("Testing at " + str(np.rad2deg(GRB.sourceangs)))
            sourcexyz = ang2vec(sourceAng[0],sourceAng[1]) #cartesian position of the burst
            loop = 0 #I'm going to want to sample each sky position more than once,
                    #here's where I define how many times that is
            locunc = []
            while loop<samples:
                sepA=bf.angle(sourcexyz,self.normA)
                xA = bf.look_up_A(self.normA,sourcexyz)
                   # print("separation from A is " + str(np.rad2deg(sepA)))
                   #this check passes.  
               
                dtheoryA=GRB.Ao*bf.response(sepA,xA)  #still need to define strength, brb and gonna do that 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsA = dtheoryA + self.bg
                unccountsA = sqrt(countsA)
                detactualA = gauss(countsA,unccountsA)  #there is a lot of noise present, updating it now. 
                if detactualA-self.bg < 0:
                    detactualA = self.bg
                    
                detcountsA = detactualA
                
                sepB=bf.angle(sourcexyz,self.normB)
                xB = bf.look_up_B(self.normB,sourcexyz)

                   # print("separation from B is " + str(np.rad2deg(sepB)))
                   #this check passes.  
               
                dtheoryB=GRB.Ao*bf.response(sepB,xB)  
                    #still need to define strength, brb and gonna do that 

                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsB = dtheoryB + self.bg 
                unccountsB = sqrt(countsB)
                detactualB = gauss(countsB,unccountsB)  #there is a lot of noise, present, updating it now. 
                if detactualB-self.bg < 0:
                    detactualB = self.bg
                    
                detcountsB = detactualB
                


                sepC=bf.angle(sourcexyz,self.normC)
                   # print("separation from C is " + str(np.rad2deg(sepC)))
                   #this check passes.  
                xC =  bf.look_up_C(self.normC,sourcexyz)
                dtheoryC=GRB.Ao*bf.response(sepC,xC)  #still need to define strength, brb and gonna do that 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsC = dtheoryC + self.bg #another artifact, incl this background effect somewhere
                unccountsC = sqrt(countsC)
                detactualC = gauss(countsC,unccountsC)  #there is a lot of noise, present, updating it now. 
                if detactualC-self.bg < 0:
                    detactualC = self.bg
                    
                detcountsC = detactualC
                
                

                
                sepD=bf.angle(sourcexyz,self.normD)
                   # print("separation from D is " + str(np.rad2deg(sepD)))
                   #this check passes.  
                xD = bf.look_up_D(self.normD,sourcexyz)
                dtheoryD=GRB.Ao*bf.response(sepD,xD)  #still need to define strength, brb and gonna do that 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsD = dtheoryD + self.bg #another artifact, incl this background effect somewhere
                unccountsD = sqrt(countsD)
                detactualD = gauss(countsD,unccountsD)  #there is a lot of noise, present, updating it now. 
                if detactualD-self.bg < 0:
                    detactualD = self.bg
                    
                detcountsD = detactualD
                

                
                
                #coarse to fine optimization
                chiA = bf.quad_solver(detcountsA,self.normA,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg,A=True)
                chiB = bf.quad_solver(detcountsB,self.normB,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg,B=True)
                chiC = bf.quad_solver(detcountsC,self.normC,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg,C=True)
                chiD = bf.quad_solver(detcountsD,self.normD,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA,self.bg,D=True)
                
                chisquared = add(add(chiA,chiB),add(chiC,chiD)) #adds it all up for total chi2
                
                #print("Chi squareds: " +str(chisquared))
                
                
                thetaloc, philoc, Aguess = bf.indexer(chisquared,bottheta,toptheta,botphi,topphi,botA,topA,ntheta,nphi,nA)
                recvec = ang2vec(deg2rad(thetaloc),deg2rad(philoc))
                locoffset = rad2deg(bf.angle(sourcexyz,recvec))
               # print("Loc offset = " + str(locoffset) + " deg")
                
                locunc.append(locoffset)
                loop +=1
            if talk:
                print("Avg loc offset = " + str(average(locunc)) + " deg.")

            self.localizationerrors.append(s.mean(locunc))
        return self.localizationerrors


    def plotSkymap(self,skyvals):
        """ Plots the TSM of the localization uncertainties for this specific version of BurstCube. 


        Parameters
        ----------
        skyvals : array
            The localiation uncertainties corresponding to each point. Comes from previous function "response2GRB".


        Returns 
        -------

        The healpy generated skymap. 

        """
        im = array(skyvals)
        newvisufunc.mollview(im,min=0, max=15,unit='Localization Accurary (degrees)',graticule=True,graticule_labels=True)
        plt.title('All Sky Localization Uncertainty for BurstCube set as ' + str(rad2deg(self.tilt)) + ' deg')  #should add something about design too! 

        plt.show()
