# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 22:46:32 2020

@author: vmatus
"""

import numpy as np
import os


ag = np.array(range(11,161))/10
# ag = np.array(range(2,17))

for i in range(len(ag)):
    for j in range(100):
        
        # print('ag='+str(ag[i])+'\n'+
        #       # 'clock=`date \'+%Hh%Mm%Ss\'`\n'+
        #       'picname=${capname}_${clock}_ag${ag}_dg${dg}.jpeg\n'+
        #       'echo \'ag\'${ag}\'dg\'${dg}\n'+
        #       'raspistill -o $picname -ss ${sh_speed} -ag ${ag} -dg ${dg}')
        capname = 'Gv_{}_idx_{}.jpeg'.format(ag[i],j)
        
        command = 'raspistill -o {} -ss 60 -ag {} -dg 2'.format(capname,ag[i])
        os.system(command)