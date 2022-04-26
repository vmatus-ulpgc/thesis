# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#ROIcropper.py

import os
import cv2

# path = '../../Calima/2020feb23_calima/2020feb23_100m/'
# path = '../../Calima/2020feb23_calima/2020feb23_200m/'
path = '../../Secondment2020/2020mar05/'

# roi = [1232, 730, 97, 339]
# roi = [1264, 855, 90, 207]
# roi = [281, 200, 39, 187]
roi = [281+39, 200, 39, 187]

files = os.listdir(path)

for filename in files:
    if filename[-4:] == 'jpeg':
        img = cv2.imread(path+filename)
        cropped_img = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
        cv2.imwrite(path+"PreROI/cropped_"+filename,cropped_img)
        # cv2.imwrite(path+"PreROI_L/cropped_"+filename,cropped_img)
        # cv2.imwrite(path+"PreROI_R/cropped_"+filename,cropped_img)
        
        