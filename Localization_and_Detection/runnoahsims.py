import fastcube
import GRBgenerator
import time	

NSIDE = 16
STRENGTH = 500
BACKGROUND = 1000
TILT = 45
ALTERNATING = False
TEST = True
TALK = False


sim1 = GRBgenerator.Sky(NSIDE,STRENGTH)

#run this file, and you immediately get
cube1 = fastcube.FastCube(BACKGROUND,TILT,alternating = ALTERNATING)

start = time.time()

response = cube1.response2GRB(sim1,test=TEST,talk=TALK)

end = time.time()
print(end-start)
print("Response: " + str(response))

if TEST == False: 
	cube1.plotSkymap(response)