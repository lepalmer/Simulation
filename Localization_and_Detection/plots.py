import numpy as np
import matplotlib.pyplot as plt
import healpy as hp
from healpy import newvisufunc



def skymap(angoffset,cmin,cmax):

	#if len(angoffset) == len(npixels):	
	im = np.array(angoffset)
	hp.newvisufunc.mollview(im,min=cmin, max=cmax,unit='Localization Accurary (degrees)',graticule=True,graticule_labels=True,cmap='viridis_r')
	plt.show()

	"""
   	else:
    	blockedpart=1000*np.ones(npixels-len(angoffset))
    	im = np.concatenate((angoffset,blockedpart))

	hp.newvisufunc.mollview(im,min=0, max=30,unit='Localization Accurary (degrees)',graticule=True,graticule_labels=True,cmap='viridis_r')
    
    plt.title('All Sky Localization Uncertainty for BurstCube')

	"""            