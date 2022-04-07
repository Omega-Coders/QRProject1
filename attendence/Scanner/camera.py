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
    
        
        """used=[]
        camera=True
        while camera==True:
            
            for code in decode(frame):
                if(code.data.decode('utf-8') not in used):
                    #print('approved')
                    #print(code.type)
                    #print(decode(code))
                    used.append(code.data.decode('utf-8'))
                    
                    messages.info(code.data.decode('utf-8'))
                    
                    time.sleep(5)
                elif(code.data.decode('utf-8') in used):
                    
                    messages.info("sorry")
                    time.sleep(5)
                else:
                    pass"""
        

        
        
                
"""def qrscanner(request):
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    aid = None

    while aid is None:
        _, frame = cap.read()

        decodedObjects = pyzbar.decode(frame)

        for obj in decodedObjects:
            #aid = re.findall('/attendees/confirmation/([0-9]+)', str(obj.data))
            try:
                attendee = Attendee.objects.get(pk=str(aid[0]))
                attendee.present = True
                attendee.timestamp = timezone.now()
                attendee.activity.update_or_create(time_log=attendee.timestamp)
                attendee.save()
                context = {
                    'scan': 'QR Successfully Scanned',
                    #'attendee': attendee,
                }
            except:
                context = {
                    'noscan': 'QR Scan Unsuccessful'
                }


        cv2.imshow("QR Reader", frame)

        if aid is not None:
            cv2.destroyAllWindows()
            break

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            context = {
                'noscan': 'No QR Scanned',
            }
            cv2.destroyAllWindows()
            break

    return render(request, 'attendees/qrscanner.html', context)"""
