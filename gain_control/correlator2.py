# -*- coding: utf-8 -*-
"""
Created on Wed May 20 22:12:05 2020

@author: vmatus
"""


"""
Created on Mon Feb 10 16:36:08 2020


EDITED MAY2020 for revised version
@author: vmatus
"""

import cv2
import numpy as np 
import os 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
font = {'family' : 'STIXGeneral',
        'size'   : 15}
matplotlib.rc('font', **font)
from scipy.signal import find_peaks

main_path = '../res/'
path = main_path + '2020feb12high/roi/'
# path = main_path + '2020feb12low/roi/'
# path = main_path + '2020feb13/roi/'

filenames = os.listdir(path)

TX_FREQUENCY    = 3600
RESOLUTION      = (2592,1952)
# SHIFT_TIME      = 18.904e-6
SHIFT_TIME      = 18.904e-6
ROW_HEIGHT      = int(1/(TX_FREQUENCY*SHIFT_TIME))-3
#ROW_HEIGHT       = 6
COLUMN_WIDTH    = 15
NUM_GAINS       = 233
NUM_CORRS       = 50 


def gen_beacon_template(row_height, number_of_rows, column_width, for_packets, offset): #By Cristo JV
        
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

def find_beacon(img, template): #By Cristo JV
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val

def find_beacon2(img,template):
    corr_frame = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(corr_frame)
    peaks,_ = find_peaks(corr_frame[:,max_loc[0]],distance=template.shape[0]-3)
    
    if len(peaks)<1:
        peaks = [max_loc[1],max_loc[1]+template.shape[0]]
    # peaks-= 7
    return corr_frame, max_val, max_loc, peaks

def SNR(pulse_matrix,bg_level): #By Victor G
    samples = pulse_matrix.flatten()-bg_level
    var = np.var(samples)
    if var == 0:
        var = 0.0001
    mean_sq = np.mean(samples**2)
    snr_db = 10*np.log10(mean_sq/var)
    if np.isnan(snr_db):
        return -100
    else:
        return 10*np.log10(mean_sq/var)


def graphRxSignal(img, pic_gdb, snr, corr_frame, corr, max_loc, peaks):
    plt.figure()
    ww = BEACON_TEMPLATE.shape[0] #window width
    t = np.linspace(1,ww,ww)*SHIFT_TIME*1000
    
    ms = np.mean(img,axis=1) #mean signal
    nf = 256.0
    
    p = max_loc[1]
    
    plt.plot(t,ms[p:p+ww,2]/nf,c='r')
    plt.plot(t,ms[p:p+ww,1]/nf,c='g')
    plt.plot(t,ms[p:p+ww,0]/nf,c='b')
    
    plt.plot(t,np.mean(BEACON_TEMPLATE,axis=1)[:,1]/256.0,c='g',linestyle='--')
    plt.plot(t,np.mean(BEACON_TEMPLATE,axis=1)[:,2]/256.0,c='r',linestyle='--')
    plt.plot(t,np.mean(BEACON_TEMPLATE,axis=1)[:,0]/256.0,c='b',linestyle='--')
    # plt.plot(t,np.flip(np.mean(BEACON_TEMPLATE,axis=1)[:,1])/256.0,c='k',linestyle='--')
    
    # plt.legend(['$s_R$','$s_G$','$s_B$','$t_G$','$t_R$','$t_B$','$t_K$'],loc=(1.04,0))
    
    # plt.title('$r_{xy}^{max}$ = '+str(round(corr,2))
    #           +', $G_V$ = '+str(round(pic_gdb,2))+' dB'
    #           +'\n $SNR_R$ = '+str(round(snr[0],2))+' dB'
    #           +', $SNR_G$ = '+str(round(snr[1],2))+' dB'
    #           +', $SNR_B$ = '+str(round(snr[2],2))+' dB')
    
    # plt.title('$r_{xy}^{max}$ = '+str(round(corr,2))
    #           +', $G_V$ = '+str(round(pic_gdb,1))+' dB'
    #           +', $SNR$ = '+str(round(np.mean(snr),1))+' dB')
    plt.xlabel('Time [ms]')
    plt.ylabel('Normalized signal [·]')
    plt.tight_layout()
    plt.show()
    # imROIshow(img,[max_loc[0],max_loc[1],COLUMN_WIDTH,ROW_HEIGHT*4])
    
    

def imROIshow(img,roi=[0,0,5,5]):
    x,y,w,h = roi
    # img = img[y:y+h,x:x+w,:]
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('Off')
    plt.tight_layout()
    if roi != [0,0,0,0]:
        print('ROI=',str(roi))
        plt.gca().add_patch(patches.Rectangle((0,y),img.shape[1]-1,h,linewidth=3,edgecolor='r',facecolor='none',linestyle='--'))
    plt.show()

# global_corr_matrix = np.zeros((NUM_GAINS,NUM_CORRS))



def analyzePic(path,file,do_graphRxSignal=False):
    img = cv2.imread(path+file)
    if file[:7] == 'cropped':
        pic_gidx = int(file[-8:-5])
        pic_rxyidx = int(file[3+8:8+8])%NUM_CORRS
    else:
        pic_gidx = int(file[-8:-5])
        pic_rxyidx = int(file[3:8])%NUM_CORRS
    
    corr_frame, corr, max_loc, peaks =  find_beacon2(img, BEACON_TEMPLATE)
    # img = img*255/np.max(img)
    
    
    p = peaks[np.random.randint(0, len(peaks))]
    # imROIshow(img, [max_loc[0], p , BEACON_TEMPLATE.shape[1],BEACON_TEMPLATE.shape[0]])


    # snraccu_R, snraccu_G, snraccu_B = 0.0, 0.0, 0.0
    
    #BEACON IS GRBK
    peak = max_loc[1]
    pulse_G = img[peak:peak+ROW_HEIGHT,:,:] * np.array([0,1,0],dtype='uint8')
    pulse_R = img[peak+ROW_HEIGHT:peak+2*ROW_HEIGHT,:,:] * np.array([0,0,1],dtype='uint8')
    pulse_B = img[peak+2*ROW_HEIGHT:peak+3*ROW_HEIGHT,:,:] * np.array([1,0,0],dtype='uint8')
    
    pulse_K = img[peak-10:peak-1,:,:]
    
    bg_G = np.mean(pulse_K[:,:,1].flatten())
    bg_R = np.mean(pulse_K[:,:,2].flatten())
    bg_B = np.mean(pulse_K[:,:,0].flatten())
    
    # imROIshow(pulse_G)
    # imROIshow(pulse_R)
    # imROIshow(pulse_B)
    
    m = 4 #margin
    
    #RESULTS IN RGB ORDER
    snr_R = SNR(pulse_R[m:-m,m:-m,2],bg_R)
    snr_G = SNR(pulse_G[m:-m,m:-m,1],bg_G)
    snr_B = SNR(pulse_B[m:-m,m:-m,0],bg_B)
    
    snr = [snr_R,snr_G,snr_B]
    
    pic_gdb = 20*np.log10(256/(256-pic_gidx))
    if do_graphRxSignal:
        graphRxSignal(img, pic_gdb, snr, corr_frame, corr, max_loc, peaks)
    
    return img, pic_gdb, snr, corr_frame, corr, peaks

# filenames = np.array(filenames)[np.random.randint(0, len(filenames),3).astype(int)]

hand_picked = np.array([9002,1046])
filenames = np.array(filenames)
filenames = filenames[(hand_picked).astype(int)]

gdb_vals = np.zeros(len(filenames)) 
rxy_vals = np.zeros(len(filenames)) 
snr_vals = np.zeros((len(filenames),3))

# if __name__ == "__main__":
i=0
# for file in np.array(filenames)[np.random.randint(0, len(filenames),10).astype(int)]:
for file in filenames:
    if file[-5:] == '.jpeg':
        if len(filenames)<20:
            do_graphRxSignal = True
        else:
            do_graphRxSignal = False
        img, pic_gdb, snr, corr_frame, corr, peaks = analyzePic(path,file,do_graphRxSignal)
        
        gdb_vals[i] = pic_gdb
        rxy_vals[i] = corr
        snr_vals[i,:] = snr
        i+=1
        # global_idx = np.argmax(os.listdir(path) == file)
        
        print(file, snr)
        # global_corr_matrix[pic_gidx, pic_rxyidx] = corr
        plt.figure()
        plt.imshow(img), plt.axis('Off')
        plt.show()
        plt.figure()
        plt.imshow(corr_frame), plt.axis('Off')
        plt.show()
        

    
if len(filenames)>=20:
    # graphRxSignal(img)
    plt.figure()
    plt.subplot(1,2,1)
    plt.scatter(gdb_vals,rxy_vals)
    plt.ylim(0.0,1.0)
    plt.xlabel('Analog gain ($G_V$) [dB]')
    plt.ylabel('Corr. coef')
    # plt.show()
    
    # plt.figure()
    # plt.scatter(gdb_vals,snr_vals[:,0],c='r')
    # plt.scatter(gdb_vals,snr_vals[:,1],c='g')
    # plt.scatter(gdb_vals,snr_vals[:,2],c='b')
    plt.subplot(1,2,2)
    plt.scatter(gdb_vals,np.mean(snr_vals[:],axis=1),c='k')
    
    plt.ylabel('SNR [dB]')
    plt.xlabel('Analog gain ($G_V$) [dB]')
    plt.ylim(-1,50)
    # plt.yscale('log')
    plt.tight_layout()
    plt.show()
    
    


    # plt.plot(np.max(global_corr_matrix,axis=1))    
    # np.savetxt(path+'corr_w{}_h{}.csv'.format(COLUMN_WIDTH, BEACON_TEMPLATE.shape[0]) ,global_corr_matrix,delimiter=',')
         
        
        
# imROIshow(BEACON_TEMPLATE)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        