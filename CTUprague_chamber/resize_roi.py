# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 18:58:46 2019

@author: vicen
"""

import cv2
import numpy as np 
import os 


main_path = 'Captures_2019_06_15/'
path = main_path + 'Captures_2019_06_15_orange/Cropped_RightLamp/'
filenames = os.listdir(path)

#for file in filenames:
file = filenames[88]
img = cv2.imread(path+file)
#cv2.imshow('',img)
#cv2.waitKey(0)
#img = (img/255.0) ** (1.8) # gamma correction and normalization (base 255)
repeats = 12
img = np.repeat(img, repeats, axis=0)
img = np.repeat(img, repeats, axis=1)
cv2.imwrite('tests/test_'+str(repeats)+'repeats_'+file+'.jpeg',img)
