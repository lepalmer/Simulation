#!/usr/bin/env python

from distutils.core import setup
from BurstCube.version import get_git_version

setup(name='BurstCube',
      version=get_git_version(),
      author='Jeremy Perkins',
      author_email='jsperki1@umd.edu',
      url='https://github.com/BurstCube',
      packages=['BurstCube'],
      )
