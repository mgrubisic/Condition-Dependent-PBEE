# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:30:08 2019

@author: VACALDER
"""

# PROGRAM TO READ GROUND MOTION FILES
#   Victor A Calderon
#   PhD Student/ Research Assistant
#   NC STATE UNIVERSITY 
#   2019 (c)

def readrecord(inFile, outFile):

    with open(inFile) as GMi:
        head1  = [next(GMi) for x in range(4)]
        Data1 = GMi.read()
        GMi.close
    #print(head)
    
    EQ_DataLine1 = head1[3]
    dt_pos1      = EQ_DataLine1.find("DT=")
    
    # Read from i to i+5 in line 3
    
    dt  = float(EQ_DataLine1[dt_pos1+5:dt_pos1+11])
    a1   = Data1.split()
    A1   = [float(i) for i in a1]
    npt = len(A1)
    
    #        plt.plot(t1,A1)
    #        plt.plot(t2,A2)
    #        plt.plot(t2_new,A2_new)
    
    
    with open(outFile, 'w') as f:
        for item in A1:
            f.write("%s\n" % item)
    
    f.close
    return dt,npt