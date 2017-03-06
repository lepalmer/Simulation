"""
------------------------------------------------------------------------
This script aims being part of the ComPair multicore analysis chain

It is a wrapper through energies and angles to create cosima source files
One only needs to define the path to the geometry file and the type of source (e.g. FarFieldPointSource)
Energies and angles may be adjusted according to the use preference

Author: Sara Buson (sara.buson@gmail.com)
------------------------------------------------------------------------
"""

from numpy import *
from math import *

#here put your geometry file and source type
geofile= '$BURSTCUBEPATH/Simulation/MEGAlib/BurstCube_1Cube.geo.setup'
OneBeam= 'FarFieldPointSource'

#define your energies and angles 
#Log_E=[1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0]
#angles  =[0]
Log_E=[2]
angles  =[0.,5.,10.,15.,20.,25.,30.,35.,40.,45.,50.,55.,60.,65.]

#gives the cosTheta array
def ang2cos(allAng):
   ang =[]
   for i in allAng:
      a= round(cos(math.radians(i)),4)
      ang.append(a) 
      #print ang
   return ang

#in keV [316,501,1000,1585, ... ]
def logE2ene(allEne):
   ene =[]
   for ee in allEne:
      a=int(10**ee)
      ene.append(a) 
   return ene


energies=logE2ene(Log_E)
cos_ang =ang2cos(angles)

for myene in energies:
   for cosTh,ang in zip(cos_ang,angles):
      
      # this is to print all the parameters combinations
      #print (geofile, OneBeam, myene, cosTh, OneBeam, ang, myene)
      
      #this is just a long string, with all the raws of the .source file, and the energies/angles values
      string= "# An example run for Cosima \n# This was created with the python wrapper --> create_source_file.py <--\n\nVersion          1 \nGeometry         %s // Update this to your path \nCheckForOverlaps 1000 0.01 \nPhysicsListEM    Livermore \n\nStoreCalibrate                 true\nStoreSimulationInfo            true\nStoreOnlyEventsWithEnergyLoss  true  // Only relevant if no trigger criteria is given! \nDiscretizeHits                 true \n\nRun FFPS \nFFPS.FileName              %s_%.3fkeV_Cos%.3f \nFFPS.NTriggers             10000 \n\n\nFFPS.Source One \nOne.ParticleType        1 \nOne.Beam                %s  %.1f 0 \nOne.Spectrum            Mono  %i\nOne.Flux                1000.0 "%(geofile, OneBeam, myene, cosTh, OneBeam, ang, myene)
      source_file='%s_%.3fkeV_Cos%.3f.source'%(OneBeam,myene,cosTh)
      sf=open(source_file,'w')
      sf.write(string)
      sf.close()
