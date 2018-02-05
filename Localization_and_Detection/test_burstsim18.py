#!/usr/bin/env python

import numpy as np
from numpy.testing import assert_allclose

from astropy.tests.helper import pytest

try:
	from burstsim18 import GRBs
except ImportError:
	pass

try:
	from burstsim18 import BurstCube
except ImportError:
	pass

@pytest.fixture(scope='module')


def test_GRBs():

	GRB = GRBs(1,500)


	assert_allclose(500, GRB.Ao(), 1e-3)
