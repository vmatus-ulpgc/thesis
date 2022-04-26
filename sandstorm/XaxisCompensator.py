# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#ROIcropper.py

import os
import cv2
import numpy as np

path, folder, dx, dy = '../../Calima/2020feb23_calima/2020feb23_100m/', 'PreROI/', 31.4482, 10.7796
# path, folder, dx, dy = '../../Calima/2020feb23_calima/2020feb23_200m/', 'PreROI/', 19.5673, 10.5789
# path, folder, dx, dy = '../../Secondment2020/2020mar05/', 'PreROI_R/', 5.6480, 33.1089
# path, folder, dx, dy = '../../Secondment2020/2020mar05/', 'PreROI_L/', 6.0074, 31.1283

dx = int(dx)
dy = int(dy)

newShape = (339,97+dx,3)
# newShape = (207,90+int(dx),3)
# newShape = (187,39+int(dx),3)
############ newShape = (187,78+int(dx),3)



files = os.listdir(path+folder)

for filename in files:
    if filename[-4:] == 'jpeg':
        img = cv2.imread(path+folder+filename)
        h = img.shape[0]
        w = img.shape[1]
        compImg = np.zeros(newShape)
        for i in range(h-1):
            # compImg[dy*i:dy*(i+1), dx-i:dx-i+w,:] = img[dy*i:dy*(i+1),:,:]
            displace = int(i/dy)
            for j in range(w-1):
                compImg[i,-j-displace,:] = img[i,-j,:]
                # compImg[i,j+displace,:] = img[i,j,:]
        
        # Save with black triangles:
        # cv2.imwrite(path+"XaxisComp/XaxCompd_"+filename,compImg)
        
        # Save without black triangles:
        cv2.imwrite(path+"XaxisComp2/XaxCompd_"+filename,compImg[:-1,int(h/dy)+1:-1-int(h/dy),:])
        print(filename)
        
        
        
