# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 10:05:33 2020

@authors: vmatus, vguerra, cjurado
"""

from __future__ import print_function

import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray
from picamera import mmal, mmalobj, exc
from picamera.mmalobj import to_rational
#from scipy import stats

import time
import io

import numpy as np
import cv2

from fractions import Fraction

MMAL_PARAMETER_ANALOG_GAIN = mmal.MMAL_PARAMETER_GROUP_CAMERA + 0x59
MMAL_PARAMETER_DIGITAL_GAIN = mmal.MMAL_PARAMETER_GROUP_CAMERA + 0x5A

MAX_GAIN = 10.66 #(Voltage ratio)
MIN_GAIN = 1.0
MAX_INDEX_GAIN_NUMBER = 232
STEP = (MAX_GAIN-MIN_GAIN)/(MAX_INDEX_GAIN_NUMBER+1)

# TX_FREQUENCY = 3600
RESOLUTION = (2592,1952)
# # SHIFT_TIME = 18.904e-6
# SHIFT_TIME = 18.904e-6
# ROW_HEIGHT = int(1/(TX_FREQUENCY*SHIFT_TIME)-0.5)-3
#ROW_HEIGHT = 6
# COLUMN_WIDTH = 25

def set_gain(camera, gain, value):
    """Set the analog gain of a PiCamera.
    
    camera: the picamera.PiCamera() instance you are configuring
    gain: either MMAL_PARAMETER_ANALOG_GAIN or MMAL_PARAMETER_DIGITAL_GAIN
    value: a numeric value that can be converted to a rational number.
    """
    if gain not in [MMAL_PARAMETER_ANALOG_GAIN, MMAL_PARAMETER_DIGITAL_GAIN]:
        raise ValueError("The gain parameter was not valid")
    ret = mmal.mmal_port_parameter_set_rational(cam._camera.control._port, 
                                                    gain,
                                                    to_rational(value))
    if ret == 4:
        raise exc.PiCameraMMALError(ret, "Are you running the latest version of the userland libraries? Gain setting was introduced in late 2017.")
    elif ret != 0:
        raise exc.PiCameraMMALError(ret)

def set_analog_gain(camera, value):
    """Set the gain of a PiCamera object to a given value."""

    
    set_gain(camera, MMAL_PARAMETER_ANALOG_GAIN, value)
    
def set_analog_gain_from_idx(camera, index):
    """Set the gain of a PiCamera object to a given value."""
    
    value = Fraction(int(256),int(256-index))
    rational = mmal.MMAL_RATIONAL_T(value.numerator, value.denominator)
    ret = mmal.mmal_port_parameter_set_rational(cam._camera.control._port, 
                                                    MMAL_PARAMETER_ANALOG_GAIN,
                                                    rational)
    if ret == 4:
        raise exc.PiCameraMMALError(ret, "Are you running the latest version of the userland libraries? Gain setting was introduced in late 2017.")
    elif ret != 0:
        raise exc.PiCameraMMALError(ret)

def set_digital_gain(camera, value):
    """Set the digital gain of a PiCamera object to a given value."""
    set_gain(camera, MMAL_PARAMETER_DIGITAL_GAIN, value)

def capture(_camera, _stream):
    _camera.capture(_stream, format='bgr')
    image = _stream.array
    _stream.truncate()
    _stream.seek(0)
    return image



if __name__ == "__main__":

    gains = np.arange(MIN_GAIN,MAX_GAIN,STEP)
    # gains = gains/10.0
    # gains_anal_log = []
    # gains_digital_log = []
    cam = PiCamera()
    # resolution = (3296,2512) 
    resolution = RESOLUTION
    cam.resolution = resolution
    g = cam.awb_gains
    cam.awb_mode = 'off'
    cam.awb_gains = (Fraction(166,100),Fraction(150,100))
    cam.shutter_speed = 300

    print("Current a/d gains: {}, {}".format(cam.analog_gain, cam.digital_gain))
    set_analog_gain(cam, 1)
    set_digital_gain(cam, 2)

    time.sleep(2)

    stream = PiRGBArray(cam, size=resolution)
    
    pic_counter = 0

    for gain_idx in range(233):
        set_analog_gain_from_idx(cam, gain_idx)
        time.sleep(0.25)
        print(float(cam.analog_gain))
        
        for i in range(50): 
            frame = capture(cam, stream)
            filename = './2020feb10/pic{0:05d}_saved_2020feb10_Gidx{1:03d}_rxyidx{2:03d}.jpeg'.format(pic_counter, gain_idx,i)
            print('Attempting to save image ', filename)
            if cv2.imwrite(filename, frame):
                pic_counter+=1
                print('success')
            else:
                print('fail')


    cv2.destroyAllWindows()
    cam.release()
