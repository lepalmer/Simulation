import burstSim
import GRBgenerator



sim1 = GRBgenerator.Sky(4,500)


cube1 = burstSim.BurstCube(1000,40)


cube1.response2GRB(sim1)