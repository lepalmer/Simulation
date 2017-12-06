#!/usr/bin/env python
"""
------------------------------------------------------------------------

A Wrapper script to run the entire MEGAlib simulation on BurstCube

Author: Regina Caputo (regina.caputo@gmail.com)
Date: February 15, 2017

Usage Examples:
import SimulationWrapper
SimulatonWrapper.run(filename='simulation_file.source')

------------------------------------------------------------------------
"""

import glob
#import numpy
#import os
import subprocess


def run(filename=None, directory=None, revanConfigFile=None, seed=None):

	if filename == None and directory == None:
		print("*** No filename or directory provide ***")
		print("Please provide a  filename, a list of filenames, or a directory name")
		return


	# Check to see if the user supplied a directory.  If so, get the list of source files
	if directory != None:
		sourcefiles = glob.glob(directory + '/*.source')

	# Check if the user supplied a single file vs a list of files
	if isinstance(filename, list) == False and filename != None:
		sourcefiles = [filename]


	# Get the revan config file if one was not provided
	#if revanConfigFile == None:
	#	revanConfigFile = glob.glob(directory + '/*.cfg')[0]

	# Generate a list of seeds
	#seeds = numpy.random.random(len(sourcefiles))*100
	#seeds.astype(int)

	# Loop through each of the source files and run them through cosima and revan
	for sourcefile in sourcefiles:

		# Generate the cosima command
		#command_cosima = "cosima %s" % (sourcefile)

		# Issued the cosima command
		#print(command_cosima)
		subprocess.run(["cosima", sourcefile])
		#output = os.system(command_cosima)


		# Generate the sim filename
		#simfile = sourcefile.replace('.source','.sim')

		# Generate the revan command
		#command_revan = "revan -f %s -c %s" % (simfile, revanConfigFile)

		# Issued the revan command
		#print command_revan
		#output = os.system(command_revan)


		# Extract the number of triggered and simulated events
		#EventAnalysis.getTriggerEfficiency(filename=simfile)

		# Generate the .tra filename
		#trafile = simfile.replace('.sim', '.tra')

		# Analyze the results of the .tra file
		# EventAnalysis.performCompleteAnalysis(filename=trafile)


	return
