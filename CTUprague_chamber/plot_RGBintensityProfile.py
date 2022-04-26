# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 11:22:02 2019

@author: vicen
"""
import cv2
import numpy as np 
import os 
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
font = {'family' : 'STIXGeneral',
        'size'   : 15}
matplotlib.rc('font', **font)

main_path = 'Captures_2019_06_15/'
path = main_path + 'Captures_2019_06_15_orange/Cropped_RightLamp/'
filenames = os.listdir(path)

#for file in filenames:
file = filenames[12]
img = cv2.imread(path+file)
#cv2.imshow('',img)
#cv2.waitKey(0)
img = (img/255.0) ** (1.8) # gamma correction and normalization (base 255)
discard = 10
channel_B = img[:,discard:-discard,0]
channel_G = img[:,discard:-discard,1]
channel_R = img[:,discard:-discard,2]


x_axis = np.linspace(1,229,229)

intProf_B = np.array(channel_B[:,12])
intProf_G = np.array(channel_G[:,12])
intProf_R = np.array(channel_R[:,12])


#plt.figure()
fig,ax = plt.subplots(3,1,figsize=(2.125*3,1.5*3),sharex=True,sharey=False)
ax[0].plot(x_axis,intProf_R,color='r')
ax[1].plot(x_axis,intProf_G,color='g')
ax[2].plot(x_axis,intProf_B,color='b')

ax[0].set_ylim([0, 1.0])
ax[1].set_ylim([0, 1.0])
ax[2].set_ylim([0, 1.0])

ax[0].set_title('Intensity profile among center column')
ax[1].set_ylabel('Intensity (base 255)')
ax[2].set_xlabel('(Vertical) Pixels')

print('Filename: '+file)
