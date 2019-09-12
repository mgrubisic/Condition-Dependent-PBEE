# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:51:13 2019

@author: VACALDER
"""

from openseespy.opensees import *
from __main__ import *
import ReadRecord
import math
from LibUnitsMUS import *

def NLTHA_Run(MS_path,GM,PCol):
    #------------------------------------------------------------------------------ 
    #|                      IMPORTS
    #------------------------------------------------------------------------------

    infile=MS_path+"\\"+GM
    outfile=r'C:\Users\vacalder\Documents\ConditionDependent_PBEE\Condition-Dependent-PBEE\EarthquakeSelection\Mainshock_Test_g3files'+"\\"+GM+".g3"
    dt,npt = ReadRecord.ReadRecord(infile,outfile)
    print(dt)
    
    ##import the os module
    #import os
    #import math
    #import numpy as np
    #import matplotlib.pyplot as plt
    #wipe()
    #from LibUnitsMUS import *
    #import ManderCC
    
    #defining gravity loads
    timeSeries('Linear', 1)
    pattern('Plain', 1, 1)
    load(2, 0.0, -PCol, 0.0)
    
    Tol = 1e-8 # convergence tolerance for test
    NstepGravity = 10
    DGravity = 1/NstepGravity
    integrator('LoadControl', DGravity) # determine the next time step for an analysis
    numberer('Plain') # renumber dof's to minimize band-width (optimization), if you want to
    system('BandGeneral') # how to store and solve the system of equations in the analysis
    constraints('Plain') # how it handles boundary conditions
    test('NormDispIncr', Tol, 6) # determine if convergence has been achieved at the end of an iteration step
    algorithm('Newton') # use Newton's solution algorithm: updates tangent stiffness at every iteration
    analysis('Static') # define type of analysis static or transient
    analyze(NstepGravity) # apply gravity
    
    loadConst('-time', 0.0) #maintain constant gravity loads and reset time to zero
     
    #applying Dynamic Ground motion analysis
    GMdirection = 1
    GMfile = outfile
    GMfact = 1*g
    
    
    
    Lambda = eigen('-fullGenLapack', 1) # eigenvalue mode 1
    Omega = math.pow(Lambda, 0.5)
    
    betaKcomm = 2 * (0.02/Omega)
    
    xDamp = 0.02				# 2% damping ratio
    alphaM = 0.0				# M-pr damping; D = alphaM*M	
    betaKcurr = 0.0		# K-proportional damping;      +beatKcurr*KCurrent
    betaKinit = 0.0 # initial-stiffness proportional damping      +beatKinit*Kini
    
    rayleigh(alphaM,betaKcurr, betaKinit, betaKcomm) # RAYLEIGH damping
    
    # Uniform EXCITATION: acceleration input
    IDloadTag = 400			# load tag
    Dt = dt			# time step for input ground motion
    GMfatt = 1.0*g			# data in input file is in g Unifts -- ACCELERATION TH
    maxNumIter = 10
    timeSeries('Path', 2, '-dt', Dt, '-filePath', GMfile, '-factor', GMfact)
    pattern('UniformExcitation', IDloadTag, GMdirection, '-accel', 2) 
    
    wipeAnalysis()
    constraints('Transformation')
    numberer('Plain')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('ModifiedNewton')
    
    NewmarkGamma = 0.5
    NewmarkBeta = 0.25
    integrator('Newmark', NewmarkGamma, NewmarkBeta)
    analysis('Transient')
    
    DtAnalysis = dt
    TmaxAnalysis = DtAnalysis*npt
    
    Nsteps =  int(TmaxAnalysis/ DtAnalysis)
    
    ok = analyze(Nsteps, DtAnalysis)
    
    tCurrent = getTime()
    
    # for gravity analysis, load control is fine, 0.1 is the load factor increment (http://opensees.berkeley.edu/wiki/index.php/Load_Control)
    
    Atest = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    Algorithm = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}
    
    
    for i in Atest:
        
        for j in Algorithm:
            
    
            if ok != 0:
                if j < 4:
                    algorithm(Algorithm[j], '-initial')
                    
                else:
                    algorithm(Algorithm[j])
                    
                test(Atest[i], Tol, 1000)
                ok = analyze(Nsteps, DtAnalysis)                            
                print(Atest[i], Algorithm[j], ok)             
                if ok == 0:
                    break
            else:
                continue
    
    #u2 = nodeDisp(2, 1)
    #print("u2 = ", u2)
    #
    #d=open("C:\\Opensees Python\\OpenseesPy examples\\Data-2c\\DFree.out")
    #F=open("C:\\Opensees Python\\OpenseesPy examples\\Data-2c\\RBase.out")
    #linesd = d.readlines()
    #linesf = F.readlines()
    #x = [line.split()[1] for line in linesd]
    #y = [line.split()[-1] for line in linesf]
    #
    #X=[float(i) for i in x]
    #Y=[float(i) for i in y]
    #
    #    
    #plt.plot(X[0:12600],Y[0:12600])
    #plt.title('Example of Force Displacement Response for NorthRidge MS-AS Sequence')
    #plt.xlabel('Diplacement (in)')
    #plt.ylabel('BaseShear (kip)')
    #plt.grid()
    #plt.show()
    #
    #
    wipe()