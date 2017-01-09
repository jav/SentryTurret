#!/usr/bin/python

import io
import logging
import time
import picamera
import cv2
import numpy as np
import threading
import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera

logger = logging.getLogger(__name__ + '.Camera')

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
        self.resolution=(self.w, self.h)
        #for fps
        self.rawframe = None
        self.frametime = None
        self.framecount = 0
        self.stopped = False
        

    def run(self):
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = tuple(self.resolution)
        camera.framerate = 15
        rawCapture = PiRGBArray(camera, size=tuple(self.resolution))
        print "[INFO] warming up..."
        time.sleep(2)

        #loop to always get latest frame        
        # capture frames from the camera
        for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image and initialize
            # the timestamp and occupied/unoccupied text
            frame = f.array
            if self.stopped:
                return

            #if cam mounted upside down, rotate 180
            if self.upsidedown: #TODO: do this in display, but for coords with math
                M = cv2.getRotationMatrix2D((self.w/2, self.h/2), 180, 1.0)
                self.rawframe = cv2.warpAffine(frame, M, (self.w, self.h))
            else:
                self.rawframe=frame
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


