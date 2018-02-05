#!/usr/bin/env python

import numpy as np
import healpy as hp

import burstsim18 as bs18



def test_GRBs():

	GRB = bs18.GRBs(1,500)

	assert GRB.Ao == 500


#more to come!