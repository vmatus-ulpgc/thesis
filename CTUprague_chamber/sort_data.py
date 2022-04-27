#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:38:20 2019

@author: VICENTE MATUS (vmatus@idetic.eu)
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
font = {'family' : 'STIXGeneral',
        'size'   : 15}
matplotlib.rc('font', **font)
import os
import datetime as dt

#### RECICLABLE VARIABLES ####
# path      (main_path + FOLDER_NAME)
# filenames

main_path = 'Captures_2019_06_15/'
path = main_path + ''
filenames = os.listdir(path)

global_power = np.array([])
global_time = np.array([])