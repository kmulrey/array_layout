import numpy as np
import pickle
from optparse import OptionParser
import os
import matplotlib.pyplot as plt
import glob


def theta_phi(theta,phi,psi,x0,y0,z0):  # transform X0,y0,z0 to shower plane

    x1=x0*np.cos(phi)+y0*np.sin(phi)
    y1=-1*x0*np.sin(phi)+y0*np.cos(phi)
    z1=z0
    
    x2=x1*np.cos(theta)-z1*np.sin(theta)
    y2=y1
    z2=x1*np.sin(theta)+z1*np.cos(theta)

    x=x2*np.cos(psi)+y2*np.sin(psi)
    y=-1*x2*np.sin(psi)+y2*np.cos(psi)
    z=z2

    return x,y,z



def fill(file,xcore,ycore,det,em_peak):
 
    '''
    - theta is the zenith angle of the event in radians
    - phi is the aziuthal angle of the event in radians
    - xcore amd ycore are shower core positions in meters
    '''
 

    #detFile=open(detectorpath)
    
    geantfile=open(file)
    info=geantfile.readline().split()
    theta=float(info[2])
    phi=float(info[3])
    
    psi=2*np.pi-phi
 
    Aeff=det.T[2]*np.cos(theta)
    
    nDet=det.shape[0]
    
    xdet, ydet, zdet = theta_phi(theta,phi,psi,det.T[0]-xcore,det.T[1]-ycore,np.zeros([nDet]))
 
    #find radius of detectors from shower core and find bin associated with geant file binning
    rad=np.sqrt(xdet*xdet+ydet*ydet)
    radBin=(rad/5.0).astype(int)
    data=np.genfromtxt(file,skip_header=1)
    
    EM=np.zeros([nDet,6])  # equivalent muons (all sky) in each detector
 
    lenData=data.shape[0]
 
    for j in np.arange(nDet):
        if radBin[j]>=lenData:
            EM[j][0]=0.0
            EM[j][1]=0.0
        else:
            EM[j][0] = Aeff[j]*data.T[1][radBin[j]]  # select EM deposit from poisson distribution
            EM[j][1] = np.random.poisson(Aeff[j]*data.T[1][radBin[j]]/em_peak)  # select EM deposit from poisson distribution
            EM[j][2] = data.T[2][radBin[j]]
            EM[j][3] = data.T[3][radBin[j]]
            EM[j][4] = data.T[4][radBin[j]]
            EM[j][5] = data.T[5][radBin[j]]


    return info, EM, rad,data


def return_probability(event_info,trigger_condition,thresh):
    nEvents=len(event_info)
    count=0.0
    for i in np.arange(nEvents):
        trig=0
        stn_trig=len(event_info[i].T[1][event_info[i].T[1]>=thresh])
        if stn_trig>=trigger_condition:
            trig=1
            count=count+1.0
            trig_flag[i]=1
    prob=count/nEvents
    return prob, trig_flag
