import numpy as np
import pickle
from optparse import OptionParser
import os
import matplotlib.pyplot as plt
import glob
import sys
from optparse import OptionParser
import random

sys.path.insert(1, 'array_layout/')
import particle_function as pf


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

outdir=output_directory+det_file+'_'+str(int(maxR))+'/'
if not os.path.exists(outdir):
    os.makedirs(outdir)
    

detectors=np.genfromtxt(array_dir+det_file+'.txt',skip_header=1)
nDet=len(detectors)



geantDir=geant_directory+typeN+'/'+energy+'/'+zenith+'/geant/'


files=glob.glob(geantDir+'*.geant')
nFiles=len(files)

core=np.zeros([nTrials*nFiles,2])
event_info=np.zeros([nTrials*nFiles,nDet,6])


count=0
for f in np.arange(len(files)):
    for i in np.arange(nTrials):
        a=random.uniform(0, 1)*2.0*np.pi
        r=random.uniform(0, 1)
        xcore = np.sqrt(r*maxR**2) * np.cos(a)
        ycore = np.sqrt(r*maxR**2) * np.sin(a)
        hold,EMdep,radius,dep_data=pf.fill(files[f], xcore, ycore, detectors,em_peak)
        event_info[count]=EMdep
        core[count][0]=xcore
        core[count][1]=ycore
        count=count+1

info={'event_info':event_info,'core':core}

PIK = outdir+typeN+'_'+energy+'_'+zenith+'.dat'
with open(PIK, "wb") as f:
    pickle.dump(info, f)
