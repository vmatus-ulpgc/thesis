import picamera
import time

with picamera.PiCamera() as camera:
    time.sleep(1)
    camera.exposure_mode = 'off'
    camera.shutter_speed = 10
    camera.start_recording("twoarrayvideo.h264", quality = 20)
    camera.wait_recording(60)
    camera.stop_recording()
    
