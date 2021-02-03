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
parser.add_option("-t", "--type", default = "proton", help = "type")
parser.add_option("-z", "--zenithbin", default = "0", help = "zenithbin")
parser.add_option("-d", "--detectorfile", default = "test_layout.txt", help = "detector file")
#parser.add_option("-m", "--threshold", default = 1.0, help = "threshold")
#parser.add_option("-c", "--trigger_condition", default = 3, help = "trigger condition")
parser.add_option("-r", "--radius", default = 250.0, help = "max radius")
parser.add_option("-n", "--trials", default = 100, help = "number of cores per shower")


(options, args) = parser.parse_args()
energy = str(options.energybin)
typeN = str(options.type)
zenith = str(options.zenithbin)
det_file = str(options.detectorfile)
#thresh = float(options.threshold)
#trigger_condition = int(options.trigger_condition)
maxR = float(options.radius)
nTrials = int(options.trials)

########################################
array_dir='/vol/astro2/users/kmulrey/array_layout/layout/'
geant_directory='/vol/astro3/lofar/sim/kmulrey/lora/flux/all_information2/'
output_directory='/vol/astro7/lofar/kmulrey/array_design/'
em_peak=6.0

print(energy)
outdir=output_directory+det_file+'_'+str(int(maxR))+'/'
import os
if not os.path.exists(outdir):
    os.makedirs(outdir)
    

detectors=np.genfromtxt(array_dir+det_file+'.txt',skip_header=1)
nDet=len(detectors)



geantDir=geant_directory+typeN+'/'+energy+'/'+zenith+'/geant/'
print(geantDir)
print(array_dir+det_file)


files=glob.glob(geantDir+'*.geant')

core=np.zeros([nTrials,2])
event_info=np.zeros([nTrials,nDet,6])
