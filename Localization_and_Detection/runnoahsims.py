import fastcube
import GRBgenerator

NSIDE = 16
STRENGTH = 500
BACKGROUND = 1000
TILT = 45
SAMPLES = 5
ALTERNATING = False
TEST = False
TALK = False

"""
Parameters
----------

NSIDE : int
	A power of 2, corresponding to the number of pixels to occupy TSM (ie NSIDE = 8 => 768 pixels, etc.)

STRENGTH : float
	The desired strength of the incident GRBs. 

BACKGROUND : float 
	The desired background in the detectors. 


TILT : float
	Angle in degrees to bend the detectors. Optimal range is somewhere between 30 and 45 degrees. 

ALTERNATING : bool
	Condition on whether or not you want to alternate the tilt pattern of the detectors. 

TEST : bool
	Condition on whether or not you are testing over the entire sky, or just one for testing purposes. 

TALK : bool  
	Condition on whether or not you want simulation to tell you the sky localization for every point, as it is running. 
"""


sim1 = GRBgenerator.Sky(NSIDE,STRENGTH)

#run this file, and you immediately get
cube1 = fastcube.FastCube(BACKGROUND,TILT,alternating = ALTERNATING)


response = cube1.response2GRB(sim1,samples=SAMPLES,test=TEST,talk=TALK)
print("Response: " + str(response))

if TEST == False: 
	cube1.plotSkymap(response)