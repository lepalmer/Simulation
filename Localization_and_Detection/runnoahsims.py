import fastcube
import GRBgenerator


NSIDE = 16
STRENGTH = 500
BACKGROUND = 1000
TILT = 45
ALTERNATING = False
TEST = False


sim1 = GRBgenerator.Sky(NSIDE,STRENGTH)

#run this file, and you immediately get
cube1 = fastcube.FastCube(BACKGROUND,TILT,alternating = ALTERNATING)


response = cube1.response2GRB(sim1,test=TEST)
print("Response: " + str(response))


cube1.plotSkymap(response)