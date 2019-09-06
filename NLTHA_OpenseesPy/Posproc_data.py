# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:23:30 2019

@author: VACALDER
"""

# PROGRAM TO ANALYZE DATA FROM BATCH RUN of NLTHA FOR TDPBEE
#   Victor A Calderon
#   PhD Student/ Research Assistant
#   NC STATE UNIVERSITY 
#   2019 (c)

# ----------------------------------------------------------------------------
#|                             IMPORTS
# ----------------------------------------------------------------------------
import os
import math
import numpy as np
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------

# Opening folder to acces data




MS_path=r'C:\Users\vacalder\Documents\TimeDependent_PBEE\EarthquakeSelection\MainShock_Test'
MSListing = os.listdir(MS_path)
icover=[4.,5.,7.5]
iTcorr= [1.1307,1.7667,3.975]
iTime= [5.,10.,15., 20., 25., 30., 35., 40., 45., 50., 55., 60., 65., 70., 75.]
iwcr= [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
rootdir=r'C:\Users\vacalder\Documents\TimeDependent_PBEE\NLTHA_OpenseesPy\data'

GM=r"RSN1231_CHICHI_CHY080-E.AT2"

#for GM in MSListing:
cover=4.0
#for cover in icover:
#for wcr in iwcr:
wcr=0.4
for Time in iTime:
    datadir=rootdir+"\\"+GM+"\\"+str(cover)+"\\"+str(wcr)+"\\"+str(Time)
   
    d=open(datadir+"\\"+"DFree.out")
    F=open(datadir+"\\"+"RBase.out")
    linesd = d.readlines()
    linesf = F.readlines()
    x = [line.split()[1] for line in linesd]
    y = [line.split()[-1] for line in linesf]
    
    X=[float(i) for i in x]
    Y=[float(i) for i in y]
    
    plt.figure(1)    
    plt.plot(X,Y)
    plt.title('Example of Force Displacement Response for ChiChi EQ w/c=0.4', fontsize=32)
    plt.xlabel('Diplacement (in)', fontsize=24)
    plt.ylabel('BaseShear (kip)', fontsize=24)
    plt.tick_params(direction='out',axis='both',labelsize=20)
    plt.grid()
    plt.show()
                    
                    
                    
                    