#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:38:20 2019

@author: VICENTE MATUS (vmatus@idetic.eu)
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os

#### RECICLABLE VARIABLES ####
# path      (main_path + FOLDER_NAME)
# filenames

main_path = '/home/matusvic/Documents/RaspiCamMsmt/'
path = main_path + ''
filenames = os.listdir(path)

plt.close('all')
global_power = np.array([])
global_time = np.array([])

#### MEASUREMENT SOURCES ####
# THORLABS P100D
# "ORANGE" CAMERA
# "BLUE" CAMERA

##########
####  ####
##########

##############################
#### THORLABS P100D FILES ####
##############################
path = main_path + 'Captures_2019_06_15_Thorlabs_P100D/'
#filenames = ['DATA42.CSV','DATA43.CSV','DATA44.CSV']
filenames = os.listdir(path)
filenames  = ['DATA42.CSV','DATA43.CSV'] # ONLY WANT TO PROCESS THESE

#MANUALLY FROM CSVS:
start_times_ms = [(6*3600+23*60+56)*1000,(7*3600+40*60+3)*1000,(9*3600+46)*1000]

#### VARIABLES IN CHAIN: ####
# TIME (SYNCHRONIZED IN ALL DEVICES)
# POWER (MEASURED BY THORLABS P100D)


for i in range(len(filenames)):
    power,time = np.transpose(np.array(pd.read_csv(path+filenames[i],
                                               sep='\t',
                                               dtype={'range':float, 'AUTO':int},
                                               skiprows=3)))
    time += start_times_ms[i]
    global_time = np.append(global_time,time)
    global_power = np.append(global_power,power)

global_time -= start_times_ms[0]

#### "ORANGE" CAMERA FILES ####
path = main_path + 'Captures_2019_06_15_orange/'
filenames = os.listdir(path)
header = 'fog_2019_06_15_'

#TIME STRING:
hours =     np.array([])
minutes =   np.array([])
seconds =   np.array([])

analog_gains    = np.array([])
digital_gains   = np.array([])

pic_cap_indexes = np.array([])

for file in filenames:
    if (file.find(header)==0):
        #### PARSE TIMES:
        hours   =   np.append(hours,int(file[15:17]))
        minutes =   np.append(minutes,int(file[18:20]))
        seconds =   np.append(seconds,int(file[21:23]))
        #### GLOBAL TIME VALUE:
        time = (3600*hours[-1]+60*minutes[-1]+seconds[-1])*1000-start_times_ms[0]
        #### FIND THE NEAREST TIME
        pic_cap_indexes = np.append(pic_cap_indexes,
                                    (np.abs(global_time - time)).argmin())
        #PARSE ANALOG AND DIGITAL GAINS:
        dg_pos      = file.find('_dg')
        analog_gains    = np.append(analog_gains,int(file[27:dg_pos]))
        digital_gains   = np.append(digital_gains,int(file[dg_pos+3:-5]))

pic_cap_times = 3600*hours+60*minutes+seconds
pic_cap_times*=1000
pic_cap_times-=start_times_ms[0]
#### FROM LOG (log_orange.txt)
cap_inits = np.array([6*3600+49*60+24,6*3600+58*60+2,7*3600+6*60+24,
             7*3600+14*60+47,7*3600+23*60+34,7*3600+56*60+2,
             8*3600+8*60+17,8*3600+16*60+35,8*3600+24*60+58])
cap_inits*=1000
cap_inits-=start_times_ms[0]

plt.figure()
plt.plot(global_time/1000,global_power*1000)

plt.xlabel('Time [s]')
plt.ylabel('Power [mW]')






# TODO: 3D

#for pic_time in pic_cap_times:
#    plt.axvline(x=pic_time/1000, color='b', linestyle=':')
#    

powerVals_captured = np.array([])

for index in pic_cap_indexes:
    power_captured = global_power[int(index)]
    powerVals_captured = np.append(powerVals_captured,power_captured)
    plt.scatter(global_time[int(index)]/1000,power_captured*1000,
                            color='b')
    

#for cap_init in cap_inits:
#    plt.axvline(x=cap_init/1000, color='g', linestyle=':')
 
   
for i in range(len(pic_cap_indexes)):
    index = int(pic_cap_indexes[i])
    text = str(int(hours[i]))+'h'+str(int(minutes[i]))+'m'+str(int(seconds[i]))+'s_ag'+str(int(analog_gains[i]))+'dg'+str(int(digital_gains[i]))
    plt.text(global_time[index]/1000,global_power[index]*1000,
             text,rotation=45)
    
plt.show()



powerVals_captured = np.array([])

for index in pic_cap_indexes:
    power_captured = global_power[int(index)]
    powerVals_captured = np.append(powerVals_captured,power_captured)
    plt.scatter(global_time[int(index)]/1000,power_captured*1000,
                            color='b')
    

for cap_init in cap_inits:
    plt.axvline(x=cap_init/1000, color='g', linestyle=':')
    
plt.show()


plt.figure()
plt.scatter(powerVals_captured*1000,analog_gains)
plt.scatter(powerVals_captured*1000,digital_gains,color='r')
plt.show()

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(powerVals_captured*1000, analog_gains, digital_gains)
plt.xlabel('Power [mW]')
plt.show()


#### CROSS CORRELATION IN BETWEEN ####

