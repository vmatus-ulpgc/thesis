# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:02:43 2020

@author: vmatus

"""

#from scipy.signal import find_peaks
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
font = {'family' : 'STIXGeneral',
        'size'   : 15}
matplotlib.rc('font', **font)
# matplotlib.rc('text', usetex=True)

main_path = '../res/'
path = main_path + '2020feb13/roi/'


BEACON_HEIGHT   = 44
COLUMN_WIDTH    = 5


global_corr_matrix = np.loadtxt(path+'corr_w{}_h{}.csv'.format(COLUMN_WIDTH, BEACON_HEIGHT), delimiter=',')
global_camera_gains_vector = np.empty((233,1))
avg_rxy = np.empty((233,1))

for i in range(233):
    global_camera_gains_vector[i] = 256.0/(256.0-i)
    avg_rxy[i] = np.average(global_corr_matrix[i,:])
    # avg_rxy[i] = global_corr_matrix[i,44]

plt.close('all')
fig,ax = plt.subplots(2,1,figsize=(5,7),sharex=False,sharey=False)

ax[0].plot(20*np.log10(np.flip(np.loadtxt('gain_APIread.txt'))),(avg_rxy))
ax[0].set_ylim([0.0,1.0])
ax[0].set_ylabel('Pearson\'s corr. coef. ($r_{xy}^{max}$)')
ax[0].text(19,0.05,'(a)')

main_path = '../res/'
path = main_path + '2020feb12high/roi/'


BEACON_HEIGHT   = 44
COLUMN_WIDTH    = 5




global_corr_matrix = np.loadtxt(path+'corr_w{}_h{}.csv'.format(COLUMN_WIDTH, BEACON_HEIGHT), delimiter=',')
global_camera_gains_vector = np.empty((233,1))
avg_rxy = np.empty((233,1))

for i in range(233):
    global_camera_gains_vector[i] = 256.0/(256.0-i)
    avg_rxy[i] = np.average(global_corr_matrix[i,:])
    # avg_rxy[i] = global_corr_matrix[i,44]


ax[1].plot(20*np.log10(global_camera_gains_vector),(avg_rxy))
ax[1].set_ylim([0.0,1.0])
ax[1].text(19,0.05,'(b)')
ax[1].set_ylabel('Pearson\'s corr. coef. ($r_{xy}^{max}$)')
ax[1].set_xlabel('Camera Analog Gain ($G_V$) [dB]')
plt.tight_layout()