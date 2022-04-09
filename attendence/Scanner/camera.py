import cv2 ,os,urllib.request
from django.shortcuts import render
from pyzbar.pyzbar import decode
import pyzbar
import time
import cv2
import numpy as np
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,440)
        self.cap.set(4,280)
        self.s,self.frame1=self.cap.read()
        self.used=[]
        self.var2=0
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        ret, frame = self.cap.read()
        frame_flip = cv2.flip(frame, 1)
        ret, frame = cv2.imencode('.jpg', frame_flip)
        return frame.tobytes()
    def get(self):
        return self.cap
    def getuse(self):
        return self.used
    def var1(self):
        return self.var2
    
        
    

