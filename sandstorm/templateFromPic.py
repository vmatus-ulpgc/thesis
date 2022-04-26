# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:01:36 2020
-+9
@author: vmatus
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

a = 41+47
template = cv2.imread("C:/Users/vmatus/Desktop/Secondment2020/2020mar05/PreROI_R/XaxisComp/XaxCompd_cropped_pic00289_saved_2020mar05_Gidx210_time20h53m25s.jpeg")[a:a+48,24:25,:]
template2 = cv2.imread("C:/Users/vmatus/Desktop/Coding/Scripts2020/beacon/template_h12w5.jpeg")[:,0,:]

fig,ax = plt.subplots(3,1,figsize=(2.125*3,1.5*3),sharex=True,sharey=False)
x_ax_size = len(template[:,0])
x_axis = np.linspace(1, x_ax_size, x_ax_size)
ax[0].plot(x_axis,template[:,0,2],color='r')
ax[0].plot(x_axis,template2[:,2],color='r',linestyle='dashed')

ax[1].plot(x_axis,template[:,0,1],color='g')
ax[1].plot(x_axis,template2[:,1],color='g',linestyle='dashed')

ax[2].plot(x_axis,template[:,0,0],color='b')
ax[2].plot(x_axis,template2[:,0],color='b',linestyle='dashed')

# np.save('template.npy',template)

