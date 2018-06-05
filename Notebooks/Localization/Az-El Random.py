from BurstCube.LocSim.GRB import *
from BurstCube.LocSim.Detector import *
from BurstCube.LocSim.Spacecraft import *
from BurstCube.LocSim.Stats import calcNorms, addErrors, calcNormsWithError

save = True

pointings = {'01': ('90:0:0','5:0:0'),
            '02': ('180:0:0','10:0:0'),
            '03': ('270:0:0','15:0:0'),
            '04': ('360:0:0','20:0:0')}

spacecraft = Spacecraft(pointings, window = 0.1)

res = (120,30)
aa,ll = np.meshgrid(np.linspace(0,360,res[0],endpoint=False),np.linspace(0,90,res[1]))

training_positions = np.vstack([aa.ravel(),ll.ravel()])

radec_array  = np.array([spacecraft._dummyDet.obs.radec_of(position[0]*np.pi/180.,position[1]*np.pi/180.) 
                         for position in training_positions.T])

exposures = np.array([[detector.exposure(position[0]*180./np.pi,position[1]*180./np.pi) 
                       for position in radec_array] 
                        for detector in spacecraft.detectors])

rr = (radec_array[:,0].reshape(res[::-1]))*180./np.pi
dd = (radec_array[:,1].reshape(res[::-1]))*180./np.pi


training_grbs = [GRB(position[0]*180./np.pi,position[1]*180./np.pi,binz=.001) 
                 for position in radec_array[exposures.sum(axis=0) > 0.]]
print("Throwing training sample")
training_counts = spacecraft.throw_grbs(training_grbs,scaled=True)


real_res = (360,100)
#real_res = (180,50)
raa,rll = np.meshgrid(np.linspace(1,361,real_res[0],endpoint=False),np.linspace(0,90,real_res[1]))
real_positions = np.vstack([raa.ravel(),rll.ravel()])

real_pos_radec  = np.array([spacecraft._dummyDet.obs.radec_of(position[0]*np.pi/180.,position[1]*np.pi/180.) 
                         for position in real_positions.T])

exposures = np.array([[detector.exposure(position[0],position[1]) for position in real_pos_radec*180./np.pi]
                      for detector in spacecraft.detectors])

real_grbs = [GRB(position[0]*180./np.pi,position[1]*180./np.pi,binz=0.001) 
             for position in real_pos_radec[exposures.sum(axis=0) > 0.]]
print("Throwing real sample")
real_counts = spacecraft.throw_grbs(real_grbs, scaled=True)

print("Calculating norms")
norms = calcNorms(real_counts,training_counts)

print("Cleaning up")
real_counts_err = addErrors(real_counts,training_counts)

norms_errp, norms_errm = calcNormsWithError(real_counts,training_counts,real_counts_err)

loc_mins = [norm.argmin() for norm in norms]
loc_mins_errm = [norm.argmin() for norm in norms_errm]
loc_mins_errp = [norm.argmin() for norm in norms_errp]

errors = [eph.separation(grb.eph,training_grbs[loc_mins[idx]].eph)*180./np.pi for idx,grb in enumerate(real_grbs)]
errors_errm = [eph.separation(grb.eph,training_grbs[loc_mins_errm[idx]].eph)*180./np.pi for idx,grb in enumerate(real_grbs)]
errors_errp = [eph.separation(grb.eph,training_grbs[loc_mins_errp[idx]].eph)*180./np.pi for idx,grb in enumerate(real_grbs)]


#hist_data = plt.hist(errors,bins=100,normed=1, histtype='step', cumulative=True)
#hist_data_errm = plt.hist(errors_errm,bins=100,normed=1, histtype='step', cumulative=True)
#hist_data_errp = plt.hist(errors_errp,bins=100,normed=1, histtype='step', cumulative=True)
#plt.plot()
#avg_stat = np.average([hist_data_errm[1][np.abs(hist_data_errm[0] - 0.68).argmin()],
#                       hist_data_errp[1][np.abs(hist_data_errp[0] - 0.68).argmin()]])

print('Average Error (uncorrected):',np.average(errors))
#print 'Systematic Error: {:,.2f}'.format(hist_data[1][np.abs(hist_data[0] - 0.68).argmin()])
#print 'Statistical Error: {:,.2f}'.format(avg_stat)
az = np.linspace(80.,10.,num=1000.)
summed = 0.
for angle in az:
    avg = np.average((np.reshape(errors,real_res[::-1]))[rll<angle])*np.sin((90.-angle)*(np.pi/180.))
    summed += avg
    #print angle,avg
print('Average Error (corrected)',summed / np.shape(az))


if save:
    print("Saving data")
    import pickle
    output = open('data/az_el_raa_hires.p', 'wb')
    pickle.dump(raa, output)
    output.close()
    output = open('data/az_el_rll_hires.p', 'wb')
    pickle.dump(rll, output)
    output.close()
    output = open('data/az_el_errors_hires.p', 'wb')
    pickle.dump(errors, output)
    output.close()




