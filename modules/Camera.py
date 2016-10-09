#!/usr/bin/python

import io
import time
import picamera
import cv2
import numpy as np
import threading
import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera


resolution=(320, 240)
framerate=32

class Capture(threading.Thread) :

    def __init__(self, cfg):
        threading.Thread.__init__(self)
        self.upsidedown = int(cfg['camera']['upsidedown'])  
        self.w = int(cfg['camera']['width']) 
        self.h = int(cfg['camera']['height'])    
        #for faster processing
        self.scaledown = float(cfg['camera']['scaledown']) 
        self.w = int(self.w / self.scaledown)
        self.h = int(self.h / self.scaledown)
        #for fps
        self.rawframe = None
        self.frametime = None
        self.framecount = 0
        self.stopped = False
        

    def run(self):
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = tuple(resolution)
        camera.framerate = 15
        rawCapture = PiRGBArray(camera, size=tuple(resolution))
        print "[INFO] warming up..."
        time.sleep(2)

        #loop to always get latest frame        
        # capture frames from the camera
        for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image and initialize
            # the timestamp and occupied/unoccupied text
            self.rawframe = f.array
            if self.stopped:
                return

            #self.rawframe = self.rawframe[:, :, ::-1]
            self.frametime = datetime.datetime.now()        
            rawCapture.truncate(0)

        
    def getFrame(self):
        frame = self.rawframe
        self.framecount = self.framecount + 1
        return frame
    
    def getFPS(self): 
        return str(self.framecount / (self.starttime - datetime.datetime.now()).total_seconds())
    
    def resetFPS(self): 
        self.starttime = datetime.datetime.now()
        self.framecount = 0
			
    def quit(self):
		self.stopped = True
	        #TODO - i think we still need to release the stream..	
                #self.capture.release()


