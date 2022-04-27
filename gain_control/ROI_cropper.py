# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
# import numpy as np 
import os 

main_path = '../res/'
path = main_path + '2020feb12low/'
filenames = os.listdir(path)
cropFolder = path + 'roi/'

x = 150
y = 183
w = 20
h = 250

try:
    os.makedirs(cropFolder)
    
except:
    pass

for file in filenames:
    if file[-5:] == '.jpeg':
        img = cv2.imread(path+file)
        cropped_img = img[y:y+h, x:x+w]
        cv2.imwrite(cropFolder+"cropped_"+file,cropped_img)
        print(cropFolder+"cropped_"+file)
