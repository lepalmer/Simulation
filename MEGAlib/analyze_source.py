#!/usr/bin/env python
"""
------------------------------------------------------------------------
Script to parse values from .sim files and make effective area plots:
Author: Regina Caputo (regina.caputo@nasa.gov
Date: February 17, 2017
Usage Examples:
import analyze_source
#make get effective area for a list of sim files
analyze_source.getAeff('sim/FarFieldPointSource_*Cos1.0*.sim',triggers=10000,r_sphere=300)
#This returns 3 arrays: energy, aeff and costh

#plot effective area vs. energy with or without GBM data!
analyze_source.plotAeff('sim/FarFieldPointSource_*Cos1.0*.sim',WithGBM=True,save=True)

#plot effective area vs. angle
analyze_source.plotAeffVsAngle('sim/FarFieldPointSource_100.000keV_Cos*.sim',save=True)

------------------------------------------------------------------------
"""

import os
import time
import sys
import fileinput
import numpy
import math
import glob

try:
	import matplotlib.pyplot as plot
	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.mlab as mlab
	import matplotlib.gridspec as gridspec
	from matplotlib.ticker import MultipleLocator, FormatStrFormatter
	from matplotlib.ticker import AutoMinorLocator
	from matplotlib.colors import LogNorm
	
	# Set the default title font dict
	titleFormat = {'fontsize': 12, 'fontweight' : plot.rcParams['axes.titleweight'], 'verticalalignment': 'baseline', 'horizontalalignment': 'center'}

except:
	print "\n**** Warning: matplotlib not found. Do not try to make plots or bad things will happen! ****"


def getDetailsFromFilename(filename):

    '''Function to get the energy and angle from a filename.
    Really should be meta data.'''
    
    details = {}
    info = filename.split('_')
    details['keV'] = info[1][:-3]
    
    angle = info[2].split('.')
    details['Cos'] = "{}.{}".format(angle[0][3:], angle[1])
    
    return details

def getKey(filename):
    file_text_name = os.path.splitext(os.path.basename(filename))  
    file_last_num = os.path.basename(file_text_name[0]).split('_')  
    num=file_last_num[1].split('.')
    return int(num[0])


def parse(filename, sourceTheta=None):

    #THIS DOES NOT WORK....
    
    print '\nParsing: %s' % filename

    #read all the lines in the file
    command = 'wc %s' % filename
    output = os.popen(command).read()
    totalNumberOfLines = int(output.split()[0])

    print totalNumberOfLines

    #for line in fileinput.input([filename]):
    line = filename.readline(totalNumberOfLines-1)
    print line
        
    if 'TS' in line:
        
        # Split the line
        lineContents = line.split()
        print "Total generated particles: ", lineContents[1]
        return float(lineContents[1])
    
    else:
        print filename, 'no total number of generated particles'
        return None

def getGBMData():

    filename='/data/slag2/BurstCube/BurstCube/Simulations/GEANT3/gbm_effective_area.dat'

    f=open(filename,'r')
    lines=f.readlines()
    aeff=[]
    energy=[]

    for i in range(len(lines)):
        data = lines[i].split('\t')
        if i>1:
            energy.append(float(data[0]))
            aeff.append(float(data[1]))
    
    #print energy, aeff
    return energy, aeff
    

def getGenPart(filename):
    
    f=open(filename,'r')
    lines=f.readlines()

    #print "reading:", filename, "... has: ",len(lines), " lines"
    last=lines[len(lines)-1]
    hold=last.split(' ')
    gen=hold[1].split('\n')
    #print "The last line is: ",last
    return int(gen[0])
    
        
def CalculateAeff(filename, triggers, r_sphere):

    generated_particles = getGenPart(filename)
    Aeff = r_sphere**2*math.pi*float(triggers)/generated_particles

    #print filename, ", Aeff: ", Aeff
    return Aeff
    

def getAeff(directory, triggers, r_sphere):

    filenames = sorted(glob.glob(directory),key=getKey)
    #print filenames

    full_details={}
    #lists
    energy = []
    aeff = []
    ang = []
    
    for fn in filenames:
        
        if '10.000keV' in fn:
            continue
        elif '15.000keV' in fn:
            continue

        details = getDetailsFromFilename(fn)
        details['Aeff'] = CalculateAeff(fn,triggers,r_sphere)

        #print fn

        for key, value in details.iteritems():
            #print key, value
            if key is 'keV':
                energy.append(value)
            elif key is 'Aeff':
                aeff.append(value)
            elif key is 'Cos':
                ang.append(float(value))
            else:
                print "key not found" 

    return energy, aeff, ang

def plotAeff(files, comparison=False, WithGBM=False, save=False):

    GBM_e=[]
    GBM_aeff=[]

    energy, aeff, ang=getAeff(files, 10000.,300.)
    plot.figure(figsize=(8,6))
    plot.scatter(energy, aeff, color='red')
    plot.plot(energy, aeff, color='red', alpha=0.5, linestyle='--', lw=2, label='1 of 9')

    if comparison: 
	    energy2, aeff2, ang2=getAeff('sim/9.4x9.4cmCube/FarFieldPointSource_*Cos1.0*.sim', 10000.,300.)
	    #plot.figure(figsize=(8,6))
	    plot.scatter(energy2, aeff2, color='blue')
	    plot.plot(energy2, aeff2, color='blue', alpha=0.5, linestyle='--', lw=2, label='1 of 4')

    plot.xscale('log')
    plot.xlabel('Energy (keV)', fontsize=16)
    plot.gca().set_xlim([1.,10000.])

    plot.yscale('log')
    plot.gca().set_ylim([1.,200.])
    plot.ylabel('Effective Area (cm$^2$)', fontsize=16)

    legend = plot.legend(loc='upper right')

    if WithGBM:
        print "with GBM!"
        GBM_e, GBM_aeff=getGBMData()
        plot.plot(GBM_e, GBM_aeff, color='green', alpha=0.75, linestyle='-', lw=2, label='GBM NaI')
        
    if save:
        plot.savefig('EffectiveArea_vs_E.png')
        plot.savefig('EffectiveArea_vs_E.pdf')

    plot.show()


def plotAeffVsAngle(files, comparison=False, save=False):
    
    energy, aeff, ang=getAeff(files, 10000.,300.)

    #print ang
    plot.figure(figsize=(8,6)) 
    angle=[]
    for i in range(len(ang)):
	    angle.append(round(numpy.degrees(numpy.arccos(ang[i]))))
    plot.scatter(angle, aeff, color='black',label='1 of 9')
    #plot.plot(angle, aeff, color='black', alpha=0.5, linestyle='--', lw=2)

    if comparison:
	    energy2, aeff2, ang2=getAeff('sim/9.4x9.4cmCube/FarFieldPointSource_100.000keV_Cos*.sim', 10000.,300.)

	    angle2=[]
	    for i in range(len(ang2)):
		    angle2.append(round(numpy.degrees(numpy.arccos(ang2[i]))))

	    plot.scatter(angle2, aeff2, color='blue', label='1 of 4')
	    #plot.plot(angle, aeff2, color='blue', alpha=0.5, linestyle='--', lw=2)

    plot.gca().set_xlim([0.,90.])
    plot.xlabel('Incident Angle (deg)', fontsize=16)

    #plot.yscale('log')
    plot.gca().set_ylim([1.,100.])
    plot.ylabel('Effective Area (cm$^2$)', fontsize=16)

    legend = plot.legend(loc='upper right')

    if save:
	    plot.savefig('EffectiveArea_vs_Ang.png')
	    plot.savefig('EffectiveArea_vs_Ang.pdf')

    plot.show()
    
