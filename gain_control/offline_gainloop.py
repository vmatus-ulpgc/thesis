# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 17:24:58 2020

@author: vmatus
"""

# import time
# import io
import numpy as np
from scipy import stats

# import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
font = {'family' : 'STIXGeneral',
        'size'   : 15}
matplotlib.rc('font', **font)
# matplotlib.rc('text', usetex=True)

plt.close('all')

MAX_GAIN = 10.66 #(Voltage ratio)
MIN_GAIN = 1.0
MAX_INDEX_GAIN_NUMBER = 232
STEP = (MAX_GAIN-MIN_GAIN)/(MAX_INDEX_GAIN_NUMBER+1)

# ROW_HEIGHT = int(1/(TX_FREQUENCY*SHIFT_TIME)-0.5)-3
#ROW_HEIGHT = 6
COLUMN_WIDTH = 25

WEIGHT_STEP = 0.02
MIN_STEP = 1
SLOPE_TH = 0.01


EPSILON = 0.002
SAMPLES = 4
gain_vector = []
correlation_vector = []


def get_next_gain(gain_vector, correlation_vector, current_gain_idx, current_corr, weight_step=WEIGHT_STEP, min_step=0.5):
    global MAX_GAIN, MIN_GAIN, SLOPE_TH, SAMPLES
    
    current_gain = (256.0/(256.0 - current_gain_idx))
    # correlation_vector.append(current_corr)
    correlation_vector.append(np.log(1-current_corr))
    gain_vector.append(current_gain)
    slope = min_step
    
    if len(gain_vector)>SAMPLES:
        correlation_vector.pop(0)
        gain_vector.pop(0)
        
        #Least Squares - Moor Penrose (Use scipy)
        #aux = np.hstack((np.array(gain_vector).reshape((SAMPLES,1)), np.ones((SAMPLES,1))))
        #slope,_ = np.linalg.lstsq(aux, np.array(correlation_vector))[0]
        
        slope, _, _, _, _ = stats.linregress(np.array(gain_vector).T,np.array(correlation_vector).T)
        if (np.isnan(slope)):
            slope = 1000
        # step = weight_step * (1-correlation_vector[-1]) / (slope+0.00001)
        step = weight_step / slope
        # next_gain = current_gain +  step
        next_gain = current_gain - step
    else:
        step = min_step
        next_gain = current_gain + min_step  #+ slope

    if next_gain > MAX_GAIN:
        next_gain = MAX_GAIN
    elif next_gain < MIN_GAIN:
        next_gain = MIN_GAIN
        
    if np.isnan(next_gain):
        gidx = 10
    else:
        gidx = int(256.0-256.0/next_gain) 
    
    # print(gidx, next_gain)
    return gidx if gidx < 233 else 232 , step
        
# FILENAME    = ''
GAIN_SEED_IDX   = 180
GAIN_MAX_IDX    = 232
global_current_gain_idx = GAIN_SEED_IDX
global_current_corr = 0
BEACON_HEIGHT   = 44
COLUMN_WIDTH    = 5

main_path = '../res/'
path = main_path + '2020feb12high/roi/'

range_iterations = 300

historic_corr = np.empty((range_iterations,1))
historic_gain = np.empty((range_iterations,1))
iterations = np.array(range(range_iterations))


if __name__ == "__main__":
    corr_matrix = np.loadtxt(path+'corr_w{}_h{}.csv'.format(COLUMN_WIDTH, BEACON_HEIGHT), delimiter=',')

    for iteration in iterations:
    # while True:
        
        #CORRELATION
        
        
        global_current_corr = corr_matrix[global_current_gain_idx,np.random.randint(0,corr_matrix.shape[1],1)]
        
        global_current_gain_idx, printstep = get_next_gain(gain_vector,
                              correlation_vector,
                              global_current_gain_idx,
                              global_current_corr)
        
        historic_corr[iteration] = global_current_corr
        historic_gain[iteration] = 256.0/(256.0-global_current_gain_idx)
        print(global_current_corr,'\t',256.0/(256.0-global_current_gain_idx), '\t', printstep)

plt.figure()
# for iteration in iterations:
plt.scatter(iterations,20*np.log10(historic_gain))
plt.xlabel('Iterations')
plt.ylabel('Camera Analog Gain ($G_V$) [dB]')
plt.ylim([0.0, 20.565])
plt.show()