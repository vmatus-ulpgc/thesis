# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np 
import os 

main_path = 'Captures_2019_06_15/'
path = main_path + 'Captures_2019_06_15_orange/'
filenames = os.listdir(path)
header = 'fog_2019_06_15_'

# ROI = x,y w,h
x = 1575
y = 1160
w = 137
h = 229


for file in filenames:
    if (file.find(header)==0):
        img = cv2.imread(path+file)
        #cv2.imshow("Original Image", img)
        cropped_img = img[y:y+h, x:x+w]
        #cv2.imshow("Cropped Image", cropped_img)
        #cv2.waitKey(0)
        cv2.imwrite(path+"Cropped/cropped_"+file,cropped_img)