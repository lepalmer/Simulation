import GRBgenerator 



def test_sky():

	GRB = GRBgenerator.sky(4,500)

	assert GRB.pixels == 192
	assert GRB.Ao == 500


#more to come!