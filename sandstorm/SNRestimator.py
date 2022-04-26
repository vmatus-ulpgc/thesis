# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:53:33 2020

@author: vmatus


"""
import Loess
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture as GM
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
font = {'family' : 'STIXGeneral',
        'size'   : 15}
matplotlib.rc('font', **font)
plt.close('all')

repo = '../../'

path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_100m/', 'XaxisComp2/', 'Sandstorm 100 m'
# path, folder, title = repo+'Calima/2020feb23_calima/2020feb23_200m/', 'XaxisComp2/', 'Sandstorm 200 m'
# path, folder, title = repo+'Secondment2020/PreROI_R/', 'XaxisComp/', 'Emulated Fog, High Tx Power' 
# path, folder, title = repo+'Secondment2020/PreROI_L/', 'XaxisComp/', 'Emulated Fog, Low Tx Power' 

results_table = np.load(path+'Results_Table.npy')
files         = np.load(path+'Processed_Filenames.npy',allow_pickle = True)
peaks_corrs    = np.load(path+'Peaks_of_correlation.npy')

column_names = 'Gidx \t G dB \t max_rxy \t BG lev \t Thresh \t ON lev \t ROI_x \t ROI_y \t ROI_w \t ROI_h \t warning'
gidx_vals   = results_table[:,0].astype(int)
gdb_vals    = results_table[:,1]
r_max_vals  = results_table[:,2]
bg_levels   = results_table[:,3]
thr_levels  = results_table[:,4]
on_levels   = results_table[:,5]
rois        = results_table[:,6:10].astype(int) #[x,y,w,h]
warnings    = results_table[:,10]

def imgShow(imgROI):
    plt.figure()
    plt.imshow(cv2.cvtColor(imgROI, cv2.COLOR_BGR2RGB))
    plt.axis('Off')
    plt.tight_layout()
    plt.show()

h_beacon = 46.4

def SNR(pulse_matrix,bg_level):
    samples = pulse_matrix.flatten()-bg_level
    var = np.var(samples)
    mean_sq = np.mean(samples**2)
    
    return mean_sq/var

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def twoGaussThres(GM_signal,a = 0.75):
    
    
    fitter = GM(2)
    _ = fitter.fit(GM_signal.reshape(-1,1))
    # print(fitter.get_params())
    weights =   fitter.weights_
    means =     fitter.means_
    covs =      fitter.covariances_.flatten()
    # print('Precisions: ', fitter.precisions_)
    # print('Converged: ', fitter.converged_)
    # print("Means: ",means)
    # print("Covs: ", covs)
    # print("Weights: ", weights)

    
    index = np.argmax(means)
    # print('\tMeans: ',means)
    
    k = 2 * np.log(weights[index-1]/weights[index] * np.sqrt(covs[index]/covs[index-1]) * a/(1-a)) * (covs[index]/covs[index-1])
    
    # coefs = [k-1, 2*means[index]-2*means[index-1]*k, k*means[index-1]**2 - means[index]**2]
    coefs = [covs[index]-covs[index-1], -2*means[index-1]*covs[index]+2*means[index]*covs[index-1], means[index-1]**2*covs[index] - means[index]**2*covs[index-1]-k]

    
    roots = np.roots(coefs)
    thresh = roots[np.logical_and(roots>means[index-1],roots<means[index])]
    
    plt.figure(figsize=[6,3.2])
    # x_values = np.linspace(0, 250, 250)
    # plt.plot(x_values, gaussian(x_values, means[0], covs[0])*200)
    # plt.plot(x_values, gaussian(x_values, means[1], covs[1])*200)
    
    x = np.linspace(0, 250, 1000).reshape(1000,1)
    logprob = fitter.score_samples(x)
    
    responsibilities = fitter.predict_proba(x)#.reshape(-1, 1))
    pdf = np.exp(logprob)
    pdf_individual = responsibilities * pdf[:, np.newaxis]
    #print np.max(pdf) -> 19.8409464401 !?
    # plt.plot(x, pdf, '-k')
    

    
    # weights_histogram = np.max(GM_signal[3000:5000])/GM_signal[3000:5000]
    
    # histogram = np.histogram(GM_signal,bins=30)
    # plt.hist((histogram[0]/np.max(np.array(histogram[0]).flatten()),histogram[1]))
    plt.hist(GM_signal,bins=30,normed=True)
    plt.plot(x, pdf_individual[:,0])#, '-g')
    plt.plot(x, pdf_individual[:,1])#, '-r')
    # plt.plot(x, pdf, '--k')
    # plt.ylim(0,1)
    plt.xlabel('Pixel values [·]')
    plt.xlim(50,250)
    plt.axvline(x=thresh,color='k',linestyle='dashed')
    # plt.hist(tG_channel[chan_mask],bins=15)
    # plt.title(filename)
    plt.ylabel("PDF [·]")
    plt.tight_layout()
    plt.legend(['Background', 'Signal', 'Threshold'])
    plt.show()
    
    if(len(thresh) == 2):
        thresh = np.mean(thresh)
    
    # print('Threshold: ', thresh)
    return thresh, np.min(means), np.max(means)

i = 0

SNRs = np.zeros((3,files.shape[0])) # [SNR_R, SNR_G, SNR_B]

idx_i, qty = 10, 20
# files = files[idx_i:idx_i+qty]

for filename in files[13:14]:
    if not(warnings[i]):
        x,y,w,h = rois[i]
        img = cv2.imread(path+folder+filename)
        roi = img[y:y+h,x:x+w,:]
        
        # SNR_R_accu, SNR_G_accu, SNR_B_accu = 0.0, 0.0, 0.0
        
        
        
        # p = 0
        # for peak in peaks_corrs[i]:
        #     if not(peak == 0):
        #         y_b,h_b = peak, int(round(h_beacon))
        #         x_b,w_b = x+2, w-2
        #         beacon = img[y_b:y_b+h_b, x_b: x_b+w_b,:]

        #         imgShow(beacon)
                

        #         beacon -= int(bg_levels[i])
                
        #         pulse_G = beacon[0:11,:,1]
        #         pulse_R = beacon[11:22,:,2]
        #         pulse_B = beacon[22:33,:,0]
                
        #         SNR_R_accu += SNR(pulse_R.astype(float))
        #         SNR_G_accu += SNR(pulse_G.astype(float))
        #         SNR_B_accu += SNR(pulse_B.astype(float))
                
        #         p += 1
                
                
        #         # print(SNR(pulse_R.astype(float)))
        #         # print(np.mean(pulse_G))
        #         # pulse_K = beacon[]
                
        
        # SNR_R_accu /= p
        # SNR_G_accu /= p
        # SNR_B_accu /= p

        # SNRs[:,i] = [SNR(pulse_R.astype(float)), SNR(pulse_G.astype(float)), SNR(pulse_B.astype(float))]
        # SNRs[:,i] = [SNR_R_accu, SNR_G_accu, SNR_B_accu]


        for c in range(3):        
            tG_channel = roi[:,:,c].flatten()
            thresh, bg, pulse_lev = twoGaussThres(tG_channel, a = 0.999)
        

            # plt.plot(tG_channel)
            # plt.axhline(y=thresh)
            chan_mask = np.array(tG_channel>thresh)
            chan_level = np.mean(tG_channel[chan_mask]-bg)
            
            print(filename,'\t',c,'\t',chan_level)
            SNR(tG_channel[chan_mask],bg)
            
            SNRs[c,i] = SNR(tG_channel[chan_mask],bg)
            
            # plt.figure()
            # plt.plot(tG_channel[chan_mask])
            # plt.show()
            
        
        #print(round(bg,2),'\t[', round(thresh[0],2),']\t', round(pulse_lev,2))

        # print(str(round(SNR_R_accu,2)),'\t',str(round(SNR_G_accu,2)),'\t',str(round(SNR_B_accu,2)))

        for k in range(int(round(h/h_beacon))):
            y_b,h_b = int(round(k*h_beacon)), int(round(h_beacon))
            x_b,w_b = x+2, w-2
            beacon = img[y_b:y_b+h_b, x_b: x_b+w_b,:]
            # imgShow(beacon)
        # Separate pulses
        # Calculate var
    i+=1

reg_deg = 0.5

chan_r = 10*np.log10(SNRs[2,:])
chan_g = 10*np.log10(SNRs[1,:])
chan_b = 10*np.log10(SNRs[0,:])

rmax_r = r_max_vals[np.argsort(chan_r)]
rmax_g = r_max_vals[np.argsort(chan_g)]
rmax_b = r_max_vals[np.argsort(chan_b)]

chan_r = np.sort(chan_r)
chan_g = np.sort(chan_g)
chan_b = np.sort(chan_b)


loess_obj_r = Loess.Loess(chan_r,rmax_r)
loess_obj_g = Loess.Loess(chan_g,rmax_g)
loess_obj_b = Loess.Loess(chan_b,rmax_b)


y_r = np.zeros_like(rmax_r)
y_g = np.zeros_like(rmax_g)
y_b = np.zeros_like(rmax_b)

for i in range(chan_r.shape[0]):
    y_r[i] = loess_obj_r.estimate(chan_r[i], window=42, use_matrix=False, degree=reg_deg)
    y_g[i] = loess_obj_g.estimate(chan_g[i], window=42, use_matrix=False, degree=reg_deg)
    y_b[i] = loess_obj_b.estimate(chan_b[i], window=42, use_matrix=False, degree=reg_deg)



plt.figure(figsize=[4.5,3.5])

plt.scatter(10*np.log10(SNRs[2,:]),r_max_vals , color = 'r', alpha=0.2)
# plt.plot(chan_r,y_r,color='r')

plt.scatter(10*np.log10(SNRs[1,:]),r_max_vals , color = 'g', alpha=0.2)
# plt.plot(chan_g,y_g,color='g')
# 
plt.scatter(10*np.log10(SNRs[0,:]),r_max_vals , color = 'b', alpha=0.2)
# plt.plot(chan_b,y_b,color='b')

plt.ylabel('Correlation')
plt.xlabel('SNR [dB]')
plt.title(title)
plt.tight_layout()
plt.ylim(0.92,1.0)
plt.show()

# plt.figure()
# plt.scatter(r_max_vals,10*np.log10(SNRs[0,:]), color = 'r')
# plt.scatter(r_max_vals,10*np.log10(SNRs[1,:]) , color = 'g')
# plt.scatter(r_max_vals,10*np.log10(SNRs[2,:]) , color = 'b')
# plt.xlabel('Correlation')
# plt.ylabel('SNR')
# plt.title(title)
# plt.show()

plt.figure(figsize=[4.8,4])
plt.scatter(gdb_vals,10*np.log10(SNRs[2,:]), color = 'r', alpha=0.25, marker='o')
plt.scatter(gdb_vals,10*np.log10(SNRs[1,:]) , color = 'g', alpha=0.25, marker='^')
plt.scatter(gdb_vals,10*np.log10(SNRs[0,:]) , color = 'b', alpha=0.25, marker='s')
plt.ylim(0,14)
plt.xlabel('Gain [dB]')
plt.ylabel('SNR [dB]')
plt.legend(['R','G','B'])
# plt.title(title)
plt.tight_layout()
plt.show()







plt.figure(figsize=[4.8,3.5])#plt.figure(figsize=[4.5,3.5])
plt.scatter(gdb_vals,r_max_vals ,alpha=0.25)
plt.ylabel('Correlation')
plt.xlabel('Gain [dB]')
# plt.title(title)
plt.tight_layout()
plt.ylim(0.92,1.0)
plt.show()



# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')


# ax.scatter(10*np.log10(SNRs[0,:]), 10*np.log10(SNRs[2,:]), r_max_vals)

