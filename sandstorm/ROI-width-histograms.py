# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:53:33 2020

@author: vmatus


"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
font = {'family' : 'STIXGeneral',
        'size'   : 15}
matplotlib.rc('font', **font)
plt.close('all')

repo = '../../'

path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_100m/', 'XaxisComp/', 'Sandstorm 100 m'
# path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_200m/', 'XaxisComp/', 'Sandstorm 200 m'
# path, folder, title = repo+'Secondment2020/PreROI_R/', 'XaxisComp/', 'Emulated Fog, High Tx Power' 
# path, folder, title = repo+'Secondment2020/PreROI_L/', 'XaxisComp/', 'Emulated Fog, Low Tx Power' 

results_table = np.load(path+'Results_Table.npy')
column_names = 'Gidx \t G dB \t max_rxy \t BG lev \t Thresh \t ON lev \t ROI_x \t ROI_y \t ROI_w \t ROI_h \t warning'

# gidx_vals   = results_table[:,0]
# gdb_vals    = results_table[:,1]
# r_max_vals  = results_table[:,2]
# bg_levels   = results_table[:,3]
# thr_levels  = results_table[:,4]
# on_levels   = results_table[:,5]
rois        = results_table[:,6:10] #[x,y,w,h]
# warnings    = results_table[:,10]

w100 = rois[:,2]

# import matplotlib.pyplot as plt

xlabel = 'ROI width (w)' 
ylabel = 'Counts [%]' 



plt.figure(figsize=[5,3])
plt.hist(w100,normed=True,bins=12)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.axvline(x=np.mean(w100),color='red', linestyle='dashed')
plt.text(np.mean(w100)-1,0.4,'${\mu}_w^{100}\approx 19$',color='red')
# plt.text(np.mean(w100)+1,0.2,'${\mu}_w^{100}$',color='red')
plt.ylim(0,0.5)
plt.tight_layout()
plt.show()


mean_100 = np.mean(w100)

path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_100m/', 'XaxisComp/', 'Sandstorm 100 m'
path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_200m/', 'XaxisComp/', 'Sandstorm 200 m'
# path, folder, title = repo+'Secondment2020/PreROI_R/', 'XaxisComp/', 'Emulated Fog, High Tx Power' 
# path, folder, title = repo+'Secondment2020/PreROI_L/', 'XaxisComp/', 'Emulated Fog, Low Tx Power' 

results_table = np.load(path+'Results_Table.npy')
column_names = 'Gidx \t G dB \t max_rxy \t BG lev \t Thresh \t ON lev \t ROI_x \t ROI_y \t ROI_w \t ROI_h \t warning'

gidx_vals   = results_table[:,0]
gdb_vals    = results_table[:,1]
r_max_vals  = results_table[:,2]
bg_levels   = results_table[:,3]
thr_levels  = results_table[:,4]
on_levels   = results_table[:,5]
rois        = results_table[:,6:10] #[x,y,w,h]
warnings    = results_table[:,10]



xlabel = 'ROI width (w)' 
ylabel = 'Counts [%]' 

w200 = rois[:,2]

plt.figure(figsize=[5,3])
plt.hist(w200,normed=True,bins=12)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.axvline(x=1/2*mean_100,color='red', linestyle='dashed')
plt.text(0.5*mean_100+0.5,0.4,'$H_0$',color='red')

plt.axvline(x=np.mean(w200),color='red', linestyle='dashed')
# plt.text(np.mhistean(w200)-1,0.2,'${\mu}_w^{200}\approx 19$',color='red')
plt.text(np.mean(w200)+1,0.4,'${\mu}_w^{200}$',color='red')
plt.xlim(10,30)
plt.ylim(0,0.5)
plt.tight_layout()
plt.show()

mean_200 = np.mean(w200)
# path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_200m/', 'XaxisComp/', 'Sandstorm 20


























#############
#### OLD ####
#############

# def read_folder(path,folder,rois):
#     files = os.listdir(path+folder)
#     gidx_vals = np.zeros(len(files))
#     r_max_vals = np.zeros(len(files))
    
#     i = 0
#     for filename in files:
#         if filename[-4:] == 'jpeg':
#             # [x,y,w,h]
#             img = cv2.imread(path+folder+filename)[rois[i,1]:rois[i,1]+rois[i,3],rois[i,0]:rois[i,0]+rois[i,2],:]
#             # corr_frame = np.load(path+'corrMatrix/'+filename[:-5]+'.npy')
#             # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(corr_frame)
#             print(filename)
#             # r_max_vals[i] = max_val
#             gidx_pos = filename.find('Gidx')
#             gidx_vals[i] = int(filename[gidx_pos+4:gidx_pos+7])
#             i+=1
#     gain_vals = 20*np.log10(256/(256-gidx_vals))
    
#     return gain_vals, r_max_vals

# gains1, rmaxs1 = read_folder(path1,folder1,rois1)
# gains2, rmaxs2 = read_folder(path2,folder2,rois2)


# plt.imshow(corr_frame)
# plt.plot([max_loc[0]], [max_loc[1]], '.', color = 'r')
# plt.text(max_loc[0]+5,max_loc[1],'R = {0:.2f}'.format(max_val),color='r')
# plt.axis('off')

# plt.figure()
# plt.scatter(gains1, rmaxs1)
# plt.scatter(gains2, rmaxs2)
# plt.legend((title1,title2))
# plt.xlabel('Gain [dB]')
# plt.ylabel('Correlation coef.')
