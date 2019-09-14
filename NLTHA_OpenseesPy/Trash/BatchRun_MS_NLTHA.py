# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:32:05 2019

@author: VACALDER
"""

#------------------------------------------------------------------------------
#|      PROGRAM TO CHECK TIME DEPENDENT PROPERTIES EFFECTS ON STRUCTURES      |
#|      
#|
#|          Victor A Calderon
#|          PhD Student/ Research Assistant
#|          NC STATE UNIVERSITY 
#|          2019 (c)
#|
#|
#------------------------------------------------------------------------------


# ----------------------------------------------------------------------------
#|                             IMPORTS
# ----------------------------------------------------------------------------

#import the os module
import os
import math
import numpy as np
from LibUnitsMUS import *
import Build_RC_Column
import math
import NLTHA_Run

# ----------------------------------------------------------------------------
#| VARIABLES THAT CHANGE WITH TIME
# ----------------------------------------------------------------------------
#
#
# *cover = Cover of concrete in cm
# *Tcorr = Time to corrosion in yrs
# *Time  = Different times that are being analyzed
# *wcr   = Water to cement ratio
# *dbi   = Initial longitudinal bar diameter
# *dti   = Initial transverse steel diameter



icover=[4.,5.,7.5]
iTcorr= [1.1307,1.7667,3.975]
iTime= [5.,10.,15., 20., 25., 30., 35., 40., 45., 50., 55., 60., 65., 70., 75.]
iwcr= [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
dbi= 0.75   
dti= 0.375  
MS_path=r'C:\Users\vacalder\Documents\TimeDependent_PBEE\EarthquakeSelection\MainShock_Test'
MSListing = os.listdir(MS_path)
rootdir=r'C:\Users\vacalder\Documents\TimeDependent_PBEE\NLTHA_OpenseesPy'
PCol = 2000.0*kip

# ----------------------------------------------------------------------------
#|                             BATCH RUN
# ----------------------------------------------------------------------------



for GM in MSListing:
    i=-1
    for cover in icover:
        i=i+1
        for Time in iTime:
            for wcr in iwcr:
                #set Functions for Fiber Model and NLTHA
                Tcorr=iTcorr[i]
                
                
                dblc  = dbi*25.4-(1.0508*(1-wcr)**1.64)*(Time-Tcorr)**0.71
                Ablc  = 0.25*math.pi*dblc**2
                Ablcm = Ablc/(1000.**2)
                Mcorr = Ablcm*7800.
                CLl   = (1-Ablcm*7800./2.223179)*100
                
                
                dbtc  = dti*25.4-(1.0508*(1-wcr)**1.64)*(Time-Tcorr)**0.71
                Atc  = 0.25*math.pi*dbtc**2
                Atcm = Atc/(1000.**2)
                CLt   = (0.55795-Atcm*7800./0.55795)*100
                datadir=rootdir+"\\"+"data"+"\\"+GM+"\\"+str(cover)+"\\"+str(wcr)+"\\"+str(Time)
                
#               if not os.path.exists(datadir):
#               os.makedirs(datadir)
                
                Build_RC_Column.Build_RC_Column(CLl,dblc,cover,Ablc,CLt,Atc,dbtc,datadir)
                NLTHA_Run.NLTHA_Run(MS_path,GM,PCol)
                    
                    
print("ALL ANALYSIS COMPLETE")