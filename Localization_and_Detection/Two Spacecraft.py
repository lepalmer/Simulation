from BurstSim.GRB import *
from BurstSim.Detector import *
from BurstSim.Spacecraft import *
from BurstSim.Stats import calcNorms, addErrors, calcNormsWithError, distance, halfway, distance2

save = True

pointings = {'01': ('90:0:0','5:0:0'),
            '02': ('180:0:0','10:0:0'),
            '03': ('270:0:0','15:0:0'),
            '04': ('360:0:0','20:0:0')}

sc0 = Spacecraft(pointings,window=0.1,lon="10:0:0")
sc1 = Spacecraft(pointings,window=0.1,lat="40:0:0")

res = 125
rr,dd = np.meshgrid(np.linspace(0,360,res,endpoint=False),np.linspace(-90,90,res))
exposure_positions = np.vstack([rr.ravel(),dd.ravel()])

exposures0 = np.array([[detector.exposure(position[0],position[1]) for position in exposure_positions.T] 
                      for detector in sc0.detectors])
exposures1 = np.array([[detector.exposure(position[0],position[1]) for position in exposure_positions.T] 
                      for detector in sc1.detectors])

rr,dd = np.meshgrid(np.linspace(0,360,85,endpoint=False),np.linspace(-90,90,85))
training_positions = np.vstack([rr.ravel(),dd.ravel()])

exposures0 = np.array([[detector.exposure(position[0],position[1]) for position in training_positions.T] 
                      for detector in sc0.detectors])
exposures1 = np.array([[detector.exposure(position[0],position[1]) for position in training_positions.T] 
                      for detector in sc1.detectors])

mask = (exposures0.sum(axis=0) > 0) & (exposures1.sum(axis=0) > 0)

training_grbs = [GRB(position[0],position[1],binz=0.001) for position in training_positions.T[mask]]

print 'Throwing training sets'

training_counts0 = sc0.throw_grbs(training_grbs,scaled=True)
training_counts1 = sc1.throw_grbs(training_grbs,scaled=True)


real_positions = np.array(zip(360.*np.random.random_sample(20000),180.*np.random.random_sample(20000)-90.))
exposures0 = np.array([[detector.exposure(position[0],position[1]) for position in real_positions] 
                      for detector in sc0.detectors])
exposures1 = np.array([[detector.exposure(position[0],position[1]) for position in real_positions] 
                      for detector in sc1.detectors])
mask = (exposures0.sum(axis=0) > 0) & (exposures1.sum(axis=0) > 0)
real_grbs = [GRB(position[0],position[1],binz=0.001) for position in real_positions[mask]]

print "Throwing real grbs"

real_counts0 = sc0.throw_grbs(real_grbs, scaled=True)
real_counts1 = sc1.throw_grbs(real_grbs, scaled=True)


print 'Cleaning up'

norms0 = calcNorms(real_counts0, training_counts0)
norms1 = calcNorms(real_counts1, training_counts1)

real_counts_err0 = addErrors(real_counts0,training_counts0)
real_counts_err1 = addErrors(real_counts1,training_counts1)

norms_errp0, norms_errm0 = calcNormsWithError(real_counts0,training_counts0,real_counts_err0)
norms_errp1, norms_errm1 = calcNormsWithError(real_counts1,training_counts1,real_counts_err1)

loc_mins0 = [norm.argmin() for norm in norms0]
loc_mins_errm0 = [norm.argmin() for norm in norms_errm0]
loc_mins_errp0 = [norm.argmin() for norm in norms_errp0]
loc_mins1 = [norm.argmin() for norm in norms1]
loc_mins_errm1 = [norm.argmin() for norm in norms_errm1]
loc_mins_errp1 = [norm.argmin() for norm in norms_errp1]

errors0 = distance(training_grbs,real_grbs,loc_mins0)
errors_errm0 = distance(training_grbs,real_grbs,loc_mins_errm0)
errors_errp0 = distance(training_grbs,real_grbs,loc_mins_errp0)
errors1 = distance(training_grbs,real_grbs,loc_mins1)
errors_errm1 = distance(training_grbs,real_grbs,loc_mins_errm1)
errors_errp1 = distance(training_grbs,real_grbs,loc_mins_errp1)


np.sum(np.array(loc_mins0) - np.array(loc_mins1) != 0)

avg_positions = halfway(zip([training_grbs[loc] for loc in loc_mins0],
                            [training_grbs[loc] for loc in loc_mins1]))
avg_positions_p = halfway(zip([training_grbs[loc] for loc in loc_mins_errp0],
                            [training_grbs[loc] for loc in loc_mins_errp1]))
avg_positions_m = halfway(zip([training_grbs[loc] for loc in loc_mins_errm0],
                            [training_grbs[loc] for loc in loc_mins_errm1]))

avg_errors = distance2(avg_positions,real_grbs)
avg_errors_p = distance2(avg_positions_p,real_grbs)
avg_errors_m = distance2(avg_positions_m,real_grbs)

print 'Average:{:,.2f}'.format(np.average(avg_errors))

if save:
    import pickle
    output = open('data/twosats_errors.p', 'wb')
    pickle.dump(avg_errors, output)
    output.close()




