#!/usr/bin/env python

import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap

from BurstSim.GRB import *
from BurstSim.Detector import *
from BurstSim.Spacecraft import *
from BurstSim.Stats import calcNorms, addErrors, calcNormsWithError

def run_sims()

	pointings, exposures, spacecraft = setup_sim()
	plot_exposure(pointings,exposures)
	training_positions, training_counts, spacecraft = training_set(spacecraft)

def setup_sim():

# ## Set up
# These are actually the default pointings but I put it here to show you how to set up various detectors.  Just six, smaller detectors this time.

#Evenly spaced around azimuth
#Staggered in zenith
#Arbitrary type
	pointings = {'01': ('90:0:0','45:0:0'),
	          '02': ('180:0:0','45:0:0'),
	          '03': ('270:0:0','45:0:0'),
	          '04': ('360:0:0','45:0:0')}
	#             '05': ('200:0:0','10:0:0'),
	#             '06': ('240:0:0','10:0:0'),
	#             '07': ('280:0:0','10:0:0'),
	#             '08': ('320:0:0','10:0:0'),
	#             '09': ('360:0:0','10:0:0')}


# Set up a spacecraft object with the pointings of the detector you've decided on.  The spacecraft defaults to a position above DC at an elevation of 550 km (about the orbit of Fermi).

	spacecraft = Spacecraft(pointings, window = 0.1)


# Set up some points in RA/Dec to calculate exposures and then access the 'exposure' function of the detector objects within the spacecraft object to plot the exposure.

	res = 250
	rr,dd = np.meshgrid(np.linspace(0,360,res,endpoint=False),np.linspace(-90,90,res))
	exposure_positions = np.vstack([rr.ravel(),dd.ravel()])

	exposures = np.array([[detector.exposure(position[0],position[1]) for position in exposure_positions.T] \
		for detector in spacecraft.detectors])

	return pointings,exposures,spacecraft 

def plot_exposure(pointings,exposures):


	plt.figure(figsize=(20,len(pointings)))
	#m = Basemap(projection='moll',lon_0=180.,resolution='c')
	#x,y = m(rr,dd)
	x,y = (rr-180.)*np.pi/180.,dd*np.pi/180.
	for sp in range(len(pointings)):
		m=plt.subplot(2, len(pointings)/2+1, sp+1, projection="mollweide")
		m.axes.xaxis.set_ticklabels([])
		m.axes.yaxis.set_ticklabels([])
		m.pcolormesh(x,y,exposures[sp].reshape((res,res)))
	plt.show()

	plt.figure(figsize=(20,20))
	#m = Basemap(projection='moll',lon_0=180,resolution='c')
	#m.drawparallels(np.arange(-90.,120.,30.))
	#m.drawmeridians(np.arange(0.,420.,60.))
	#x,y = m(rr,dd)
	#x,y = (rr-180.)*np.pi/180.,dd*np.pi/180.
	m=plt.subplot(2, len(pointings)/2+1, sp+1, projection="mollweide")
	m.axes.xaxis.set_ticklabels([])
	m.axes.yaxis.set_ticklabels([])
	m.pcolormesh(x,y,exposures.sum(axis=0).reshape((res,res)))
	#plt.colorbar()
	plt.show()

	return

def training_set(spacecraft):

	rr,dd = np.meshgrid(np.linspace(0,360,100,endpoint=False),np.linspace(-90,90,100))
	training_positions = np.vstack([rr.ravel(),dd.ravel()])

	exposures = np.array([[detector.exposure(position[0],position[1]) for position in training_positions.T] \
		for detector in spacecraft.detectors])

	training_grbs = [GRB(position[0],position[1],binz=.001) for position in training_positions.T[exposures.sum(axis=0) > 0.]]

	pos = np.array([[grb.eph._ra*180./np.pi,grb.eph._dec*180./np.pi] for grb in training_grbs])
	plt.figure(figsize=(8,10))
	m=plt.subplot(111, projection="mollweide")
	x,y = (pos[:,0]-180.)*np.pi/180.,pos[:,1]*np.pi/180.
	m.scatter(x,y,3,marker='o',color='k')
	m.axes.xaxis.set_ticklabels([])
	m.axes.yaxis.set_ticklabels([])
	m.grid(linestyle=':', linewidth=2)
	#m = Basemap(projection='moll',lon_0=180,resolution='c')
	#m.drawparallels(np.arange(-90.,120.,30.))
	#m.drawmeridians(np.arange(0.,420.,60.))
	#x,y = m(pos[:,0],pos[:,1])
	#m.scatter(x,y,3,marker='o',color='k')
	plt.show()

	training_counts = spacecraft.throw_grbs(training_grbs,scaled=True)

	return training_positions, training_counts, spacecraft

def localize():

# ## Setup and throw a random sample of GRBs
# 
# Note that I'm only throwing them in the north since the Earth blocks the south.

	real_positions = np.array(zip(360.*np.random.random_sample(2000),180.*np.random.random_sample(2000)-90.))

	exposures = np.array([[detector.exposure(position[0],position[1]) for position in real_positions] \
		for detector in spacecraft.detectors])


	real_grbs = [GRB(position[0],position[1],binz=0.001) for position in real_positions[exposures.sum(axis=0) > 0.]]

#np.shape(real_grbs)

	real_counts = spacecraft.throw_grbs(real_grbs, scaled=True)


# In[ ]:

pos = np.array([[grb.eph._ra*180./np.pi,grb.eph._dec*180./np.pi] for grb in real_grbs])
plt.figure(figsize=(8,10))
m=plt.subplot(111, projection="mollweide")
m.scatter((pos[:,0]-180)*np.pi/180.,pos[:,1]*np.pi/180.,3,marker='o',color='k')
m.axes.xaxis.set_ticklabels([])
m.axes.yaxis.set_ticklabels([])
plt.grid(linestyle=':',color='k')
plt.show()


# In[ ]:

norms = calcNorms(real_counts,training_counts)


# In[ ]:

real_counts_err = addErrors(real_counts,training_counts)


# In[ ]:

norms_errp, norms_errm = calcNormsWithError(real_counts,training_counts,real_counts_err)


# Find the minimum distance of each GRB.

# In[ ]:

loc_mins = [norm.argmin() for norm in norms]
loc_mins_errm = [norm.argmin() for norm in norms_errm]
loc_mins_errp = [norm.argmin() for norm in norms_errp]


# Now, calculate the distance from the real GRB to the training one picked out from the distance measuremnt above.

# In[ ]:

errors = [eph.separation(grb.eph,training_grbs[loc_mins[idx]].eph)*180./np.pi for idx,grb in enumerate(real_grbs)]
errors_errm = [eph.separation(grb.eph,training_grbs[loc_mins_errm[idx]].eph)*180./np.pi for idx,grb in enumerate(real_grbs)]
errors_errp = [eph.separation(grb.eph,training_grbs[loc_mins_errp[idx]].eph)*180./np.pi for idx,grb in enumerate(real_grbs)]


# Plot and save the cumulative distribution of this error.

# In[ ]:

hist_data = plt.hist(errors,bins=100,normed=1, histtype='step', cumulative=True)
hist_data_errm = plt.hist(errors_errm,bins=100,normed=1, histtype='step', cumulative=True)
hist_data_errp = plt.hist(errors_errp,bins=100,normed=1, histtype='step', cumulative=True)
plt.plot()


# ## The 1-sigma error is around 68%.  Quick function to find the distance value that most closely matches 0.68.

# In[ ]:

avg_stat = np.average([hist_data_errm[1][np.abs(hist_data_errm[0] - 0.68).argmin()],
                       hist_data_errp[1][np.abs(hist_data_errp[0] - 0.68).argmin()]])


# In[ ]:

print 'Systematic Error: {:,.2f}'.format(hist_data[1][np.abs(hist_data[0] - 0.68).argmin()])


# In[ ]:

print 'Statistical Error: {:,.2f}'.format(avg_stat)


# In[ ]:

pos = np.array([[grb.eph._ra*180./np.pi,grb.eph._dec*180./np.pi] for grb in real_grbs])
plt.figure(figsize=(20,10))
m=plt.subplot(111, projection="mollweide")
m.scatter((pos[:,0]-180)*np.pi/180.,pos[:,1]*np.pi/180.,marker='o',c=errors,s=100.,cmap=plt.cm.hsv)
m.axes.xaxis.set_ticklabels([])
m.axes.yaxis.set_ticklabels([])
plt.grid(linestyle=':',color='k')

#m = Basemap(projection='moll',lon_0=180,resolution='c')
#m.drawparallels(np.arange(-90.,120.,30.))
#m.drawmeridians(np.arange(0.,420.,60.))
#x,y = m(pos[:,0],pos[:,1])
#m.scatter(x,y,marker='o',c=errors,s=100.,cmap=plt.cm.hsv)
#plt.colorbar(errors,shrink=0.5)
plt.savefig('Sky Map with Errors.pdf', transparent = True)
plt.show()


# In[ ]:




# In[ ]:




# In[ ]:



