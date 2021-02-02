import numpy as np
import pickle
from optparse import OptionParser
import os
import matplotlib.pyplot as plt
import glob
import sys
from optparse import OptionParser

sys.path.insert(1, 'array_layout/')
import particle_function


parser = OptionParser()
parser.add_option("-e", "--energybin", default = "6", help = "energybin")
parser.add_option("-t", "--type", default = "6", help = "type")
parser.add_option("-z", "--zenithbin", default = "0", help = "zenithbin")


(options, args) = parser.parse_args()
energy = str(options.energybin)
typeN = str(options.type)

########################################
array_dir='/vol/astro2/users/kmulrey/array_layout/layout/'
geant_directory='/vol/astro3/lofar/sim/kmulrey/lora/flux/all_information2/'
output_directory='/vol/astro7/lofar/kmulrey/array_design/'
print(energy)



detectors=np.genfromtxt(array_dir+'test_layout.txt',skip_header=1)
nDet=len(detectors)

#typeN='proton'
#energy='6'


#zenith='0'

geantDir=geant_directory+typeN+'/'+energy+'/'+zenith+'/geant/'
print(geantDir)
'''
thresh=1.0
trigger_condition=3
em_peak=6.0

maxR=250
nTrials=100

geantDir=geant_directory+typeN+'/'+energy+'/'+zenith+'/geant/'
files=glob.glob(geantDir+'*.geant')

core=np.zeros([nTrials,2])
event_info=np.zeros([nTrials,nDet,6])
'''
