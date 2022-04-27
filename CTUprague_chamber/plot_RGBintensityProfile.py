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


def ROI_width(gammaCorrectedImg):
    width = 12
    
    return width

def intensityProfile(fileNo = 154, mean_cols = True, plot_it = True):
    
    ####################
    #### LOAD IMAGE ####
    ####################
    
    main_path = ''#'Captures_2019_06_15/'
    path = main_path + 'Captures_2019_06_15_orange/Cropped_RightLamp/'
    filenames = os.listdir(path)
    file = filenames[fileNo]
    img = cv2.imread(path+file) # Remember that openCV uses BGR, not RGB
    img = (img/255.0) ** (1.8) # gamma correction and normalization (base 255)

    # Calculate width:
    margin = int((img.shape[1]-ROI_width(img))/2)
    print(margin)
    img = img[margin:-margin,margin:-margin,:]
    
    # Remember that openCV uses BGR, not RGB
    # Remember that openCV uses BGR, not RGB
    
    channel_B = img[:,:,0]
    channel_G = img[:,:,1]
    channel_R = img[:,:,2]

    
    #INTENSITY PROFILE
    if mean_cols:
        # matrix.mean(axis=None, dtype=None, out=None)
        intProf_B = channel_B.mean(axis=1)
        intProf_G = channel_G.mean(axis=1)
        intProf_R = channel_R.mean(axis=1)
    else: 
        column = 12
        intProf_B = np.array(channel_B[:,column])
        intProf_G = np.array(channel_G[:,column])
        intProf_R = np.array(channel_R[:,column])
    
    if plot_it:
        #plt.figure()
        fig,ax = plt.subplots(3,1,figsize=(2.125*3,1.5*3),sharex=True,sharey=False)
        x_axis = np.linspace(1,len(intProf_B),len(intProf_B))
        ax[0].plot(x_axis,intProf_R,color='r')
        ax[1].plot(x_axis,intProf_G,color='g')
        ax[2].plot(x_axis,intProf_B,color='b')
        
        ax[0].set_ylim([0, 1.0])
        ax[1].set_ylim([0, 1.0])
        ax[2].set_ylim([0, 1.0])
        
        ax[0].set_title('Intensity profile among center column')
        ax[1].set_ylabel('Intensity (base 255)')
        ax[2].set_xlabel('(Vertical) Pixels')
    
    print('Intensity Profile obtained. Filename: '+file)
    
intensityProfile(13)
intensityProfile(6)
intensityProfile(8)
intensityProfile(111)