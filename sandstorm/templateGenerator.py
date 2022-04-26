# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:00:44 2020

@author: vmatus
"""

import cv2
import numpy as np
import scipy.signal as ss

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
font = {'family' : 'STIXGeneral',
        'size'   : 15}
matplotlib.rc('font', **font)


repo = '../../'

path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_100m/', 'XaxisComp2/', 'Sandstorm 100 m'
# path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_200m/', 'XaxisComp2/', 'Sandstorm 200 m'
# path, folder, title = repo+'Secondment2020/PreROI_R/', 'XaxisComp/', 'Emulated Fog, High Tx Power' 
# path, folder, title = repo+'Secondment2020/PreROI_L/', 'XaxisComp/', 'Emulated Fog, Low Tx Power' 

results_table = np.load(path+'Results_Table.npy')
files         = np.load(path+'Processed_Filenames.npy',allow_pickle = True)
peaks_corrs    = np.load(path+'Peaks_of_correlation.npy')

rois        = results_table[:,6:10].astype(int) #[x,y,w,h]
warnings    = results_table[:,10]
# ROW_HEIGHT = int(1/(TX_FREQUENCY*SHIFT_TIME)-0.5)-3
ROW_HEIGHT = 11
COLUMN_WIDTH = 15
WINDOW = 13
GAMMA = 1/1.2
pulseDims = (ROW_HEIGHT,COLUMN_WIDTH)

# case, file_name, title =    0  , 'template_sq_nol.npy'   , 'Square Non-overlapped' 
# case, file_name, title =    1  , 'template_sq_ol.npy'    , 'Square Overlapped' 
case, file_name, title =    2  , 'template_tr.npy'       , 'Trapezoid' 
# case, file_name, title =    3  , 'template_pic.npy'      , 'Reference Image' 


# Cases: [1 = Sq N-OL, 2 = ]

def imgShow(imgROI):
    plt.figure()
    plt.imshow(cv2.cvtColor(imgROI, cv2.COLOR_BGR2RGB))
    plt.axis('Off')
    plt.tight_layout()
    plt.show()
    
if case == 3:
    i=0
    for filename in files[5:6]:
        if not(warnings[i]):
            x,y,w,h = rois[i]
            img = cv2.imread(path+folder+filename)
            roi = img[y:y+h,x:x+w,:]            
            
            p = 0
            for peak in peaks_corrs[i]:
                if not(peak == 0):
                    y_b,h_b = peak, ROW_HEIGHT*4
                    x_b,w_b = x+2, w-2
                    beacon = img[y_b:y_b+h_b, x_b: x_b+w_b,:]
    
                    imgShow(beacon)
                    if input('[y/n]')=='y':
                        template = beacon
                        mean_temp = np.mean(beacon,axis=1)
                        template = mean_temp.repeat(COLUMN_WIDTH,axis=0).reshape((ROW_HEIGHT*4,COLUMN_WIDTH,3)).astype('uint8')
                        # template = template-np.mean(template)
                        # 
    
        
else:

    one = np.array(np.ones(pulseDims)*255,dtype='uint8')
    zero = np.zeros(pulseDims,dtype='uint8')
    
    pulse_G = np.stack((zero,one,zero),axis=2)
    pulse_R = np.stack((zero,zero,one),axis=2)
    pulse_B = np.stack((one,zero,zero),axis=2)
    pulse_K = np.stack((zero,zero,zero),axis=2)
    
    template = np.vstack((pulse_G,pulse_R,pulse_B,pulse_K))
    
    if case == 1 or case == 2:
        template_filt = np.zeros((4*ROW_HEIGHT+WINDOW-1,COLUMN_WIDTH,3))
        
        
        win_filter = np.ones(WINDOW)
        
        for col in range(COLUMN_WIDTH):
            template_filt[:,col,0] = ss.convolve(template[:,col,0],win_filter,mode='full',method='direct')
            template_filt[:,col,1] = ss.convolve(template[:,col,1],win_filter,mode='full',method='direct')
            template_filt[:,col,2] = ss.convolve(template[:,col,2],win_filter,mode='full',method='direct')
        
        # template = (template_filt*255.0/WINDOW).astype('uint8')
        template = ((template_filt*255.0/np.max(template_filt)) ** GAMMA).astype('uint8')
        
    
    if case == 1:
        template[template>0] = 255

# cv2.imwrite("beacon/template_h{}w{}.jpeg".format(ROW_HEIGHT,COLUMN_WIDTH),template)
# template_jpeg = cv2.imread("beacon/template_h{}w{}.jpeg".format(ROW_HEIGHT,COLUMN_WIDTH))


np.save(file_name, template)
np.save('template.npy',template)
# np.save('template.npy',template_jpeg)


plt.figure()
fig,ax = plt.subplots(3,1,figsize=(2.125*3,1.5*3),sharex=True,sharey=False)

SHIFT_TIME = 18.904e-6
x_axis = np.linspace(1,template.shape[0],template.shape[0])*SHIFT_TIME*1000
ax[0].plot(x_axis,template[:,0,2],color='r')
ax[1].plot(x_axis,template[:,0,1],color='g')
ax[2].plot(x_axis,template[:,0,0],color='b')

# ax[0].set_ylim([0, 299])
# ax[1].set_ylim([0, 299])
# ax[2].set_ylim([0, 299])

# ax[0].set_title('Intensity profile among center column')
ax[1].set_ylabel('Pixel values')
ax[2].set_xlabel('Time [ms]')
ax[0].set_title('Pulse shape type: \''+title+'\'')


template_image_resized = cv2.resize(template, (template.shape[1]*2,template.shape[0]*2), interpolation = cv2.INTER_AREA)

plt.figimage(cv2.cvtColor(template_image_resized, cv2.COLOR_BGR2RGB), 387, 110)

# plt.figure()
# plt.imshow(cv2.cvtColor(template, cv2.COLOR_BGR2RGB))
# plt.axis('Off')
# plt.show()
