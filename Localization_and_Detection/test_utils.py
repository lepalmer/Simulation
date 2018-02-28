import burstutils

import numpy as np


def test_length():
	x = [0,1,0]

	testmag = burstutils.length(x)

	assert (np.abs(testmag - 1) < 1e-7)


def test_angle():
	#used to find one separation
	x = [1,0,0]
	y = [0,1,0]
	testang = burstutils.angle(x,y)

	assert (np.abs(testang - np.pi/2) < 1e-7)

def test_findAngles():
	#used to find an array of separations
	xs = [[1,0,0],[1,0,0]]
	ys = [[0,1,0],[0,1,0]]

	testangs = burstutils.findAngles(xs,ys)

	np.testing.assert_allclose(testangs, (np.pi/2, np.pi/2), 1e-3)


def test_chiresponse():
	testAs = burstutils.chiresponse(np.array([np.pi/4,7*np.pi/4]))
	
	np.testing.assert_allclose(testAs,(0.768438,0),1e-3)

def test_response():
	testA = 