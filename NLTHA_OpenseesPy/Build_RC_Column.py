# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:12:06 2019

@author: pchi893
"""

from openseespy.opensees import *
#import the os module
#    import os
import math
#    import numpy as np
#    import matplotlib.pyplot as plt
from LibUnitsMUS import *
import ManderCC
from __main__ import *

def Build_RC_Column(CLl,dblc,cover,Ablc,CLt,Atc,dbtc,datadir):
    
    # -----------------------------------------------------------------------------
    #	OpenSees (Tcl) code by:	Silvia Mazzoni & Frank McKenna, 2006
    
    #
    #    ^Y
    #    |
    #    2       __ 
    #    |          | 
    #    |          |
    #    |          |
    #  (1)       LCol
    #    |          |
    #    |          |
    #    |          |
    #  =1=      _|_  -------->X
    #
    
    #------------------------------------------------------------------------------ 
    #|                      IMPORTS
    #------------------------------------------------------------------------------
    wipe()

    
    #------------------------------------------------------------------------------
    #                           GENERATE GEOMETRY
    #------------------------------------------------------------------------------
    
    
    model('basic', '-ndm', 2, '-ndf', 3) 
    LCol = 36.0*ft # column length
    Weight = 2000.0*kip # superstructure weight
    
    # define section geometry
    DCol = 40.0*inch # Column Diameterepth
    
    
    PCol =Weight  # nodal dead-load weight per column
    Mass =  PCol/g
    
    ACol = 0.25*math.pi*DCol**2  # cross-sectional area, make stiff
    IzCol = 0.25*math.pi*DCol**4  # Column moment of inertia
    
    node(1, 0.0, 0.0)
    node(2, 0.0, LCol)
    
    fix(1, 1, 1, 1)
    
    mass(2, Mass, 1e-9, 0.0)
    
    ColSecTag = 1			# assign a tag number to the column section
    coverCol = 5.0   # Column cover to reinforcing steel NA.
    numBarsCol = 16  # number of longitudinal-reinforcement bars in column. (symmetric top & bot)
    barAreaCol = 2.25  # area of longitudinal-reinforcement bars
    
    # MATERIAL parameters
    IDconcC = 1      # material ID tag -- confined cover concrete
    IDconcU = 2 		# material ID tag -- unconfined cover concrete
    IDreinf = 3 	   # material ID tag -- reinforcement
    
    # Define materials for nonlinear columns
    # ------------------------------------------
    #Longitudinal steel properties
    Fy=60.0*ksi*(1-0.021*CLl)        # STEEL yield stress
    Es=29000.0*ksi     # modulus of steel
    Bs=0.01            # strain-hardening ratio 
    R0=18.0            # control the transition from elastic to plastic branches
    cR1=0.925          # control the transition from elastic to plastic branches
    cR2=0.15           # control the transition from elastic to plastic branches
    c=cover*cm         # Column cover to reinforcing steel NA.
    numBarsSec= 16     # number of uniformly-distributed longitudinal-reinforcement bars
    barAreaSec= Ablc*mm2   # area of longitudinal-reinforcement bars
    dbl=dblc*mm    
    
    # Transverse Steel Properties
    fyt=60.0*ksi*(1-0.021*CLt)               # Yield Stress of Transverse Steel
    Ast=Atc*mm2               # Area of transverse steel
    dbt=dbtc*mm             # Diameter of transverse steel
    st=2.0*inch                # Spacing of spiral
    Dprime=DCol-2*c-dbt        # Inner core diameter
    Rbl=Dprime*0.5-dbt-dbl*0.5 # Location of longitudinal bar
    
    # nominal concrete compressive strength
    fpc= 5.0*ksi       # CONCRETE Compressive Strength, ksi   (+Tension, -Compression)
    Ec=57.0*ksi*math.sqrt(fpc/psi) # Concrete Elastic Modulus
    
    # unconfined concrete
    fc1U=-fpc;                 # UNCONFINED concrete (todeschini parabolic model), maximum stress
    eps1U=-0.003               # strain at maximum strength of unconfined concrete
    fc2U=0.2*fc1U              # ultimate stress
    eps2U=-0.01                # strain at ultimate stress
    lambdac=0.1                # ratio between unloading slope at $eps2 and initial slope $Ec
    
    
    mand=ManderCC.ManderCC(fpc,Ast,fyt,Dprime,st)
    
    fc=mand[0]
    eps1=mand[1]
    fc2=mand[2]
    eps2=mand[3]
    
    # CONCRETE                  tag   f'c        ec0   f'cu        ecu
    # Core concrete (confined)
    uniaxialMaterial('Concrete01',IDconcC, fc, eps1,fc2,eps2)
    
    # Cover concrete (unconfined)
    uniaxialMaterial('Concrete01',IDconcU, fc1U,eps1U,fc2U,eps2U)
    
    # STEEL
    # Reinforcing steel 
    params=[R0,cR1,cR2]
    #                        tag  fy E0    b
    uniaxialMaterial('Steel02', IDreinf, Fy, Es, Bs,R0,cR1,cR2)
    
    # FIBER SECTION properties -------------------------------------------------------------
    # Define cross-section for nonlinear columns
    # ------------------------------------------
    
    # set some paramaters
    SecTag1=1
    ri=0.0
    ro=DCol/2.0
    nfCoreR=8
    nfCoreT=8
    nfCoverR=2
    nfCoverT=8
    rc=ro-c
    theta=360.0/numBarsSec
    
    section('Fiber', SecTag1)
    
    # Create the concrete fibers
    patch('circ',1,nfCoreT,nfCoreR,0.0,0.0,ri,rc,0.0,360.0) # Define the core patch
    patch('circ',2,nfCoverT,nfCoverR,0.0,0.0,rc,ro,0.0,360.0) #Define Cover Patch
    
    # Create the reinforcing fibers
    layer('circ',3,numBarsSec,barAreaSec,0.0,0.0,rc,theta,360.0)
    
    ColTransfTag = 1
    geomTransf('Linear', ColTransfTag)
    numIntgrPts = 5
    eleTag = 1
    
    #import InelasticFiberSection
    
    element('nonlinearBeamColumn', eleTag, 1, 2, numIntgrPts, ColSecTag, ColTransfTag)
    
    recorder('Node', '-file', datadir+'/DFree.out','-time', '-node', 2, '-dof', 1,2,3, 'disp')
    recorder('Node', '-file', datadir+'/DBase.out','-time', '-node', 1, '-dof', 1,2,3, 'disp')
    recorder('Node', '-file', datadir+'/RBase.out','-time', '-node', 1, '-dof', 1,2,3, 'reaction')
    #recorder('Drift', '-file', datadir+'Data-2c/Drift.out','-time', '-node', 1, '-dof', 1,2,3, 'disp')
    recorder('Element', '-file', datadir+'/FCol.out','-time', '-ele', 1, 'globalForce')
    recorder('Element', '-file', datadir+'/ForceColSec1.out','-time', '-ele', 1, 'section', 1, 'force')
    #recorder('Element', '-file', datadir+'Data-2c/DCol.out','-time', '-ele', 1, 'deformations') 

