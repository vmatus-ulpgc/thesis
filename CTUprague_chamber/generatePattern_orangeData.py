# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:20:53 2019

@author: vicen
"""

import numpy as np
import cv2

def generateTemplate(rowHeight = 7, columnWidth = 23):
    # Pattern is G-R-B-K ("grab key")
    
    # Remember that openCV uses BGR, not GRB
    b_block = np.repeat([[[255,   0,      0   ]]], rowHeight, axis=0)
    g_block = np.repeat([[[0,     255,    0   ]]], rowHeight, axis=0)
    r_block = np.repeat([[[0,     0,      255 ]]], rowHeight, axis=0)
    k_block = np.repeat([[[0,     0,      0   ]]], rowHeight, axis=0)
    
    #"grab key"
    template = np.concatenate((g_block, r_block, b_block, k_block),axis=0)
    template = np.concatenate((template,template,template,template,template,template,template,template), axis=0)
    template = np.repeat(template,columnWidth,axis=1)
    return template.astype(np.float32)


rowHeight = 75
columnWidth = 70
template = generateTemplate(rowHeight,columnWidth)
cv2.imwrite('tests/template_rh'+str(rowHeight)+'cw'+str(columnWidth)+'_8times.jpeg',template)