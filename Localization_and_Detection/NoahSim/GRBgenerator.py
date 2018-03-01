
#Needs to know how to point to healpy 
import healpy as hp

class Sky():
    """
    Generates an array of GRB's given 
    certains strength at different sky positions.
    
    Output should be an array. 
    """
    def __init__(self,NSIDE,strength):

        #depending on NSIDE, there will be anywhere from 12 to infinite spots on the sky w/ GRBs
        self.Ao = strength
        self.pixels = hp.nside2npix(NSIDE)

        #want to convert these pixels into theta phi coords. 
        self.sourceangs = []
        for i in range(self.pixels):
            self.sourceangs.append(hp.pix2ang(NSIDE,i))

    def say_Ao(self):
        """
        """

        print("The GRBs being tested will be " + str(self.Ao) + " counts strong.")
        
