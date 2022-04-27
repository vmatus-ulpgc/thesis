# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:36:08 2020


EDITED MAY2020 for revised version
@author: vmatus
"""

import cv2
import numpy as np 
import os 
import matplotlib.pyplot as plt

main_path = '../res/'
path = main_path + '2020feb13/roi/'
filenames = os.listdir(path)

TX_FREQUENCY    = 3600
RESOLUTION      = (2592,1952)
# SHIFT_TIME      = 18.904e-6
SHIFT_TIME      = 18.904e-6
ROW_HEIGHT      = int(1/(TX_FREQUENCY*SHIFT_TIME)-0.5)-3
#ROW_HEIGHT       = 6
COLUMN_WIDTH    = 5
NUM_GAINS       = 233
NUM_CORRS       = 50 


def gen_beacon_template(row_height, number_of_rows, column_width, for_packets, offset):
        
        template_g = np.repeat(np.array([[[0, 255, 0]]]), row_height, axis=0)
        template_r = np.repeat(np.array([[[0, 0, 255]]]), row_height, axis=0)
        template_b = np.repeat(np.array([[[255, 0, 0]]]), row_height, axis=0)
        template_n = np.repeat(np.array([[[0, 0, 0]]]), row_height, axis=0)
        templates = np.array([template_g,template_r,template_b,template_n])
        template_concat = templates[0]
        
        for i in range(1, for_packets*number_of_rows+offset):
            j = i % 4
            template_concat = np.concatenate((template_concat,templates[j]),axis=0)

        template = np.repeat(template_concat, column_width, axis=1)
        return template

BEACON_TEMPLATE = gen_beacon_template(row_height=ROW_HEIGHT,
                                column_width=COLUMN_WIDTH,
                                number_of_rows=4,
                                for_packets=1,
                                offset=0).astype(dtype=np.uint8)

def find_beacon(img, template):
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc

global_corr_matrix = np.empty((NUM_GAINS,NUM_CORRS))
                              
if __name__ == "__main__":
    
    for file in filenames:
        if file[-5:] == '.jpeg':
            roi = cv2.imread(path+file)
            if file[:7] == 'cropped':
                pic_gidx = int(file[-8:-5])
                pic_rxyidx = int(file[3+8:8+8])%NUM_CORRS
            else:
                pic_gidx = int(file[-8:-5])
                pic_rxyidx = int(file[3:8])%NUM_CORRS
            corr, loc = find_beacon(roi, BEACON_TEMPLATE)
            
            # plt.figure(), plt.imshow(roi), plt.axis('Off'), plt.tight_layout(), plt.show()
            
            print(file, '\t' ,corr)
            global_corr_matrix[pic_gidx, pic_rxyidx] = corr
    
    # np.savetxt(path+'corr_w{}_h{}.csv'.format(COLUMN_WIDTH, BEACON_TEMPLATE.shape[0]) ,global_corr_matrix,delimiter=',')
             
      
