# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:16:08 2019

@author: VACALDER
"""

# PROGRAM TO GENERATE MAINSHOCK - AFTERSHOCK RECORD SEQUENCES


import math  as math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import fnmatch
import shutil

dirListing = os.listdir(r'C:\Users\vacalder\Documents\TimeDependent_PBEE\EarthquakeSelection\Mainshocks')
editFiles = []
for i in dirListing:
    editFiles.append(i)
    